from fastapi import FastAPI
from app.api.routes import progress
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(progress.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)