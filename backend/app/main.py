from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, progress
from app.db.database import Base, engine
from app.models.user import User

Base.metadata.create_all(bind=engine)   # Creates the users table if it doesn't exist

app = FastAPI()

app.include_router(progress.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)