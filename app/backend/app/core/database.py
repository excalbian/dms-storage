from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[sessionmaker, None, None]:
    try:
        db = SessionLocal()
        yield SessionLocal
    finally:
        db.close()