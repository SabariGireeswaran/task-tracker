import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

default_db_url = "sqlite:///./tasks.db"

# Render's filesystem is read-only except for /tmp unless a disk is attached.
# Fall back to /tmp when deployed there.
if os.getenv("RENDER"):
    default_db_url = "sqlite:////tmp/tasks.db"

DATABASE_URL = os.getenv("DATABASE_URL", default_db_url)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
