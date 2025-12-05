from sqlalchemy import create_engine, Column, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import enum
from app.core.config import settings
from app.core.logger import logger

# Create engine - use psycopg (version 3) instead of psycopg2
database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TransactionTypeEnum(str, enum.Enum):
    """Transaction type enum"""
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class TransactionModel(Base):
    """SQLAlchemy model for transactions"""
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True)
    type = Column(SQLEnum(TransactionTypeEnum), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    userId = Column("userId", String, nullable=False)
    createdAt = Column("createdAt", DateTime, nullable=False)
    updatedAt = Column("updatedAt", DateTime, nullable=False)


def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection() -> bool:
    """Test database connection"""
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False
