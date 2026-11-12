import hashlib
import logging
import secrets
import smtplib
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError
from pymongo.database import Database

from app.core.security import (create_access_token, get_current_user, hash_password, verify_password)
from app.db.database import get_db
from app.schemas.auth import TokenResponse, UserLogin, UserRegister, UserResponse
from app.schemas.password_reset import PasswordResetConfirmation, PasswordResetRequest
from app.services.email_service import EmailConfigurationError, send_password_reset_email

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


def serialize_user(document: dict) -> dict:
    return {
        "id": str(document["_id"]),
        "email": document["email"],
        "full_name": document["full_name"],
        "student_id": document.get("student_id"),
        "role": document["role"],
    }


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Database = Depends(get_db)):
    email = str(user_data.email).lower()
    users = db["users"]
    existing_user = users.find_one({"email": email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    now = datetime.now(timezone.utc)
    document = {
        "email": email,
        "hashed_password": hash_password(user_data.password),
        "full_name": user_data.full_name,
        "role": "student",
        "created_at": now,
        "updated_at": now,
    }
    if user_data.student_id is not None:
        document["student_id"] = user_data.student_id

    try:
        result = users.insert_one(document)
    except DuplicateKeyError as error:
        key_pattern = (error.details or {}).get("keyPattern", {})
        if "email" in key_pattern:
            detail = "Email already registered"
        elif "student_id" in key_pattern:
            detail = "Student ID already registered"
        else:
            raise
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        ) from error
    document["_id"] = result.inserted_id

    return serialize_user(document)

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Database = Depends(get_db)):
    user = db["users"].find_one({"email": str(user_data.email).lower()})

    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    access_token = create_access_token(data={"sub": str(user["_id"])})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": serialize_user(user),
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return serialize_user(current_user)


@router.post("/password-reset/request")
def request_password_reset(
    request: PasswordResetRequest,
    db: Database = Depends(get_db),
):
    generic_response = {
        "message": "If an account exists for that email, a password reset link will be sent."
    }
    email = str(request.email).lower()
    user = db["users"].find_one({"email": email})

    if user is None:
        return generic_response

    reset_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(reset_token.encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc)
    tokens = db["password_reset_tokens"]
    tokens.delete_many({"user_id": user["_id"]})
    tokens.insert_one(
        {
            "user_id": user["_id"],
            "token_hash": token_hash,
            "created_at": now,
            "expires_at": now + timedelta(minutes=30),
        }
    )

    try:
        send_password_reset_email(email, reset_token)
    except (EmailConfigurationError, smtplib.SMTPException, OSError) as error:
        tokens.delete_one({"token_hash": token_hash})
        logger.exception("Unable to send password reset email.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to send a password reset email. Please try again later.",
        ) from error

    return generic_response


@router.post("/password-reset/confirm")
def confirm_password_reset(
    confirmation: PasswordResetConfirmation,
    db: Database = Depends(get_db),
):
    token_hash = hashlib.sha256(
        confirmation.reset_token.encode("utf-8")
    ).hexdigest()
    now = datetime.now(timezone.utc)
    tokens = db["password_reset_tokens"]
    token_record = tokens.find_one_and_delete(
        {"token_hash": token_hash, "expires_at": {"$gt": now}}
    )
    if token_record is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The reset link is invalid or expired. Request a new link.",
        )

    user_id = token_record["user_id"]
    result = db["users"].update_one(
        {"_id": user_id},
        {
            "$set": {
                "hashed_password": hash_password(confirmation.new_password),
                "updated_at": now,
            }
        },
    )
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The reset link is invalid or expired. Request a new link.",
        )

    tokens.delete_many({"user_id": user_id})
    return {"message": "Password reset successfully."}
