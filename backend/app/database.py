"""
Database / session setup — owned by Member 2 per Team Build Guide.

Member 1 (API) imports SessionLocal / get_db / Base from here
but does not redefine schema. This file provides the contract
Member 1 codes against.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use DATABASE_URL if provided (for hosted PostgreSQL), else local SQLite.
# Render/Railway provide postgres:// or postgresql://
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kanban.db")

# Normalize postgres:// -> postgresql:// for SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite needs check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """FastAPI dependency — yields a DB session and closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Create tables and seed the three MVP columns if missing.
    Called on app startup in main.py
    """
    # Import models here to ensure they are registered on Base
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # Seed columns
    from .models import BoardColumn
    db = SessionLocal()
    try:
        existing = {c.id for c in db.query(BoardColumn).all()}
        defaults = [
            {"id": "todo", "title": "To Do", "position": 0},
            {"id": "doing", "title": "In Progress", "position": 1},
            {"id": "done", "title": "Done", "position": 2},
        ]
        for col in defaults:
            if col["id"] not in existing:
                db.add(BoardColumn(**col))
        db.commit()
    finally:
        db.close()
