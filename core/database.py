import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

import cx_Oracle

Base = declarative_base()

# Обновленный URL подключения
SQLALCHEMY_DATABASE_URL2 = "oracle+cx_oracle://hr:hr2025@192.168.1.86:1521/hrfree"


# Создание двигателя
engine = create_engine(
    SQLALCHEMY_DATABASE_URL2,
    pool_size=20,
    echo=False  # Лучше отключить избыточные логи
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail="Database operation failed.")
    finally:
        db.close()
        logging.debug("Database connection closed.")
