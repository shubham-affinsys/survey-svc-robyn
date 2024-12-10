import uuid
from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine, Column, String, DateTime, JSON, Integer, ForeignKey, Boolean
import sys
from log import logger

from sqlalchemy.future import select
import asyncio
load_dotenv()

Base = declarative_base()

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker


class Helper:
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

def generate_uuid():
    return str(uuid.uuid4())



class Survey(Base, Helper):
    __tablename__ = 'surveys'

    survey_id = Column(String, primary_key=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    survey_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    tenant = Column(String, nullable=True)

    responses = relationship('UserResponse', back_populates='survey', cascade="all, delete-orphan")

class UserResponse(Base, Helper):
    __tablename__ = 'user_responses'

    response_id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    survey_id = Column(String, ForeignKey('surveys.survey_id', ondelete='CASCADE'))
    user_id = Column(String, nullable=False)
    response_data = Column(JSON) 
    tenant = Column(String, nullable=False)
    channel_id = Column(String, nullable=False)  
    status = Column(String, nullable=False)  
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    survey = relationship('Survey', back_populates='responses')

DB_URL = getenv("RAILWAY_PG_URL")
try:
    logger.info("creating engine...")
    engine = create_engine(DB_URL, pool_size=20, max_overflow=10)
    logger.info(f"engine: {engine}")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("engine created!!!")

    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine,checkfirst=True)
    
    logger.info("Tables created!!!")

except Exception as e:
    logger.error(f"error cannot connect to DB {e}")


