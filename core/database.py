import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from .config import configs
import cx_Oracle

# SQLALCHEMY_DATABASE_URL = f"oracle://system:Oracle123@172.20.0.2:1521/MORAL"

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = f"oracle://system:Oracle123@192.168.0.61:1521/MORAL"
# Create engine

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    echo=configs.SQLALCHEMY_ECHO
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        logging.debug(e)
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if db:
            db.close()
            logging.debug("Database connection closed.")
