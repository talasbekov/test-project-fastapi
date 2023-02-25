import json
import traceback
from functools import wraps

from fastapi import HTTPException
from jwt.exceptions import ExpiredSignatureError
from pydantic import BaseModel
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

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
        db.commit()
    # except Exception as e:
    #     db.rollback()
    #     traceback.print_exc()
    #     if isinstance(e, HTTPException):
    #         raise e
    #     elif isinstance(e, ExpiredSignatureError):
    #         raise HTTPException(status_code=400, detail=e.args)
    #     else:
    #         raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
