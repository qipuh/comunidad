"""
Database configuration for SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from typing import Generator

load_dotenv()

# Get database URL from environment, with SQLite fallback for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./comunidad.db"  # Development default
)

# Create engine with different configs for SQLite vs MySQL/PostgreSQL
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import Base from models after engine is created to avoid circular imports
from app.models.configuracion import Base

# Import all models to register them with Base
from app.models import factiliza, usuario, cobranza, eleccion, reunion, galeria


def get_db() -> Generator:
    """Dependency injection for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
