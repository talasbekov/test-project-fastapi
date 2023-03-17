import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import configs

SQLALCHEMY_DATABASE_URL = f"postgresql://{configs.POSTGRES_USER}:{configs.POSTGRES_PASSWORD}@{configs.POSTGRES_HOSTNAME}:{configs.DATABASE_PORT}/{configs.POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20
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
    #     if isinstance(e, HTTPException):
    #         raise e
    #     elif isinstance(e, ExpiredSignatureError):
    #         raise HTTPException(status_code=400, detail=f"Signature is expired!")
    #     else:
    #         logging.error("%s", e, exc_info=True)
    #         raise HTTPException(status_code=400, detail=str(e))
    finally:
        if db:
            db.close()
            logging.debug("Database connection closed.")
