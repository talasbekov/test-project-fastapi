from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from hr_document import HrDocument
# from ..core.config import configs

Base = declarative_base()
SQLALCHEMY_DATABASE_URL2 = f"oracle://system:Oracle123@172.20.0.4:1521/MORAL"
# SQLALCHEMY_DATABASE_URL2 = f"oracle://system:Oracle123@192.168.0.61:1521/MORAL"
# Create engine

engine = create_engine(
    SQLALCHEMY_DATABASE_URL2,
    pool_size=20,
    # echo=configs.SQLALCHEMY_ECHO
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal.query(HrDocument).delete(synchronize_session=False)