from pydantic import BaseModel, EmailStr, Field, field_validator


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirmation(BaseModel):
    reset_token: str = Field(min_length=1, max_length=512)
    new_password: str = Field(min_length=12, max_length=72)

    @field_validator("reset_token")
    @classmethod
    def reset_token_must_not_be_whitespace(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Reset token must not be blank.")
        return value

    @field_validator("new_password")
    @classmethod
    def new_password_must_match_policy(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 UTF-8 bytes.")
        if not (
            any(character.isupper() for character in value)
            and any(character.islower() for character in value)
            and any(character.isdigit() for character in value)
            and any(not character.isalnum() for character in value)
        ):
            raise ValueError(
                "Password must include uppercase and lowercase letters, a number, and a special character."
            )
        return value