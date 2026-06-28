from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from db import Base, engine
from models.db_models import PollDB, OptionDB, VoteDB
from routes.poll_routes import router as poll_router

load_dotenv()

app = FastAPI()

origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(poll_router)

@app.on_event("startup")
def startup():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")

@app.get("/")
def root():
    return {"status": "ok"}