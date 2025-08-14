"""
PostgreSQL database connection management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import config
from .base import Base


class DatabaseManager:
    """Database connection manager"""
    
    def __init__(self):
        self.engine = create_engine(
            config.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=config.DATABASE_POOL_SIZE,
            max_overflow=config.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,
            echo=config.DEBUG_MODE
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


# Global database manager instance
db_manager = DatabaseManager()
get_db = db_manager.get_session
