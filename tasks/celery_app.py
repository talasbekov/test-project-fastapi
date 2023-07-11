from celery import Celery
from services.staff_list import staff_list_service
from schemas.staff_list import StaffListUserCreate, StaffListRead
from core import configs

from fastapi import HTTPException

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


app = Celery('celery_app', backend='redis://redis:6379/', broker='amqp://rabbitmq:5672/')

SQLALCHEMY_DATABASE_URL = f"postgresql://{configs.POSTGRES_USER}:{configs.POSTGRES_PASSWORD}@{configs.POSTGRES_HOSTNAME}:{configs.DATABASE_PORT}/{configs.POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=configs.SQLALCHEMY_ECHO
)


@app.task
def task_create_draft(user_id: str,
                 obj_in: dict, 
                 current_user_role_id: str):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    staff_list = staff_list_service.create_by_user_id(db,
                                                      user_id,
                                                      StaffListUserCreate(**obj_in), 
                                                      current_user_role_id)
    staff_list = StaffListRead.from_orm(staff_list).dict()
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if db:
            db.close()
    return staff_list

@app.task
def task_apply_staff_list(
    id,
    signed_by,
    document_creation_date,
    current_user_id,
    role,
    rank,
    document_number,
    document_link
):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    staff_list = staff_list_service.apply_staff_list(db,
                                                     id,
                                                     signed_by,
                                                     document_creation_date,
                                                     current_user_id,
                                                     role,
                                                     rank,
                                                     document_number,
                                                     document_link)
    staff_list = StaffListRead.from_orm(staff_list).dict()
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if db:
            db.close()
    return staff_list
    