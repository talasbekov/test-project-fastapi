from functools import wraps

from fastapi import HTTPException
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .config import configs

SQLALCHEMY_DATABASE_URL = f"postgresql://{configs.POSTGRES_USER}:{configs.POSTGRES_PASSWORD}@{configs.POSTGRES_HOSTNAME}:{configs.DATABASE_PORT}/{configs.POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = next(get_db())
        try:
            kwargs["db"] = session
            res = await func(*args, **kwargs)
            print(res)
            session.commit()
            return res
        except Exception as e:
            session.rollback()
            if isinstance(e, HTTPException):
                raise e
            else:
                raise HTTPException(status_code=400, detail=str(e))

    return wrapper
