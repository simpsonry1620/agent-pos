"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.config import settings


# Create database engine
engine = create_engine(
    settings.database_url,
    # Connection pool settings
    pool_size=20,
    max_overflow=0,
    pool_recycle=3600,  # Recycle connections after 1 hour
    # Enable connection pooling
    poolclass=StaticPool if "sqlite" in settings.database_url else None,
    echo=settings.debug,  # Log SQL queries in debug mode
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False, 
    bind=engine
)


def get_db_session() -> Session:
    """
    Dependency function to get database session.
    Used with FastAPI's dependency injection system.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables.
    This should only be used for development/testing.
    Use Alembic migrations for production.
    """
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)


def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return result.scalar() == 1
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
