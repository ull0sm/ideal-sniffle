"""Database utilities and connection management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from typing import Generator
import streamlit as st

from models.database import Base
from config.settings import settings


# Create engine
engine = create_engine(
    settings.DATABASE_URI if settings.DATABASE_URI else "sqlite:///./chatbot.db",
    poolclass=NullPool if "sqlite" in (settings.DATABASE_URI or "") else None,
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Get database session with context manager."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """Get database session for Streamlit."""
    return SessionLocal()
