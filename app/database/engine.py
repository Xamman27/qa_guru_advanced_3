import os
import logging

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.testing.pickleable import User
from sqlmodel import create_engine, SQLModel, text
from sqlalchemy.orm import Session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
engine = create_engine(os.getenv("DATABASE_URL",
                                 'postgresql+psycopg2://postgres:example@localhost:5432/postgres'),
                       pool_size=os.getenv("DATABASE_POOL_SIZE", 10))

def create_database():
    SQLModel.metadata.create_all(engine)

def check_availability():
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        logger.error("Ошибка при подключении к базе данных: %s", e)
        return False