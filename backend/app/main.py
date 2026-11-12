from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, progress
from app.db.database import client, initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        initialize_database()
        yield
    finally:
        client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(progress.router)
app.include_router(auth.router)

origins = [
    "https://nataliel359.github.io",  # Your frontend URL
    "http://localhost:3000",          # Local testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)