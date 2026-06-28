from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi import Cookie
import uuid, os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# FastAPI dependency
def get_db():
    if SessionLocal is None:
        raise RuntimeError("DB not initialized")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cookie voter ID handling
def get_or_create_voter_id(voter_id: str | None = Cookie(default=None)):
    if voter_id:
        return voter_id
    
    return str(uuid.uuid4())