import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "degree_progress")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI must be set to connect to MongoDB Atlas.")

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
database = client[MONGODB_DB]


def get_db() -> Database:
    return database


def initialize_database() -> None:
    client.admin.command("ping")

    database["users"].create_index("email", unique=True)
    database["users"].create_index("student_id", unique=True, partialFilterExpression={"student_id": {"$type": "string"}})

    database["courses"].create_index("course_id", unique=True)
    database["degree_programs"].create_index("program_id", unique=True)
    database["degree_requirements"].create_index(
        [
            ("program_id", 1),
            ("requirement_id", 1)
        ],
        unique=True
    )
    database["student_completed_courses"].create_index(
        [
            ("user_id", 1),
            ("course_id", 1)
        ],
        unique=True
    )

    database["password_reset_tokens"].create_index("token_hash", unique=True)
    database["password_reset_tokens"].create_index("expires_at", expireAfterSeconds=300)