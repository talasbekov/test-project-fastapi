import datetime

from celery import Celery
from celery.schedules import crontab
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from core import configs
from services import staff_list_service, survey_service
from schemas.staff_list import StaffListUserCreate, StaffListRead
from models import UserLoggingActivity, SurveyRepeatTypeEnum


app = Celery('celery_app', backend='redis://redis:6379/',
             broker='amqp://rabbitmq:5672/', timezone='Asia/Almaty',
             include=['tasks.celery_app'])


app.conf.beat_schedule = {
    'clear_user_logging_activities_table_every_3_days': {
        'task': 'tasks.celery_app.task_clear_user_'+
                    'logging_activities_table_every_3_days',
        'schedule': crontab(minute=0, hour=0, day_of_month='*/3')
    },
    'repeat_surveys_with_every_week_type': {
        'task': 'tasks.celery_app.task_repeat_surveys',
        'schedule': crontab(minute=10, hour=21, day_of_week='thu'),
        'args': (SurveyRepeatTypeEnum.EVERY_WEEK.value,)
    },
    'repeat_surveys_with_every_month_type': {
        'task': 'tasks.celery_app.task_repeat_surveys',
        'schedule': crontab(minute=0, hour=0, day_of_month='1'),
        'args': (SurveyRepeatTypeEnum.EVERY_MONTH.value,)
    },
    'repeat_surveys_with_every_year_type': {
        'task': 'tasks.celery_app.task_repeat_surveys',
        'schedule': crontab(minute=0, hour=0, day_of_month='1', month_of_year='1'),
        'args': (SurveyRepeatTypeEnum.EVERY_YEAR.value,)
    }
}

SQLALCHEMY_DATABASE_URL = f"postgresql://{configs.POSTGRES_USER}:{configs.POSTGRES_PASSWORD}@{configs.POSTGRES_HOSTNAME}:{configs.DATABASE_PORT}/{configs.POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=configs.SQLALCHEMY_ECHO
)


@app.task(bind=True)
def task_create_draft(self,
                      user_id: str,
                      obj_in: dict,
                      current_user_role_id: str):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    staff_list = staff_list_service.create_by_user_id(self, db,
                                                      user_id,
                                                      StaffListUserCreate(
                                                          **obj_in),
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


@app.task(bind=True)
def task_apply_staff_list(
    self,
    id,
    signed_by,
    document_creation_date,
    current_user_id,
    role,
    rank,
    document_number,
    document_link
):
    self.update_state(state=0)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    staff_list = staff_list_service.apply_staff_list(self, db,
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


@app.task
def task_clear_user_logging_activities_table_every_3_days():
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        now_date = datetime.datetime.now()
        delete_objects = (
            db.query(UserLoggingActivity).filter(
                UserLoggingActivity.signed_at < now_date - datetime.timedelta(days=3)
            ).all()
        )
        
        for obj in delete_objects:
            db.delete(obj)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if db:
            db.close()
    
    return True

@app.task
def task_repeat_surveys(status: str):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        expired_surveys = (
            survey_service.get_expired_by_repeat_type(db, status)
        )
        
        for survey in expired_surveys:
            survey_service.repeat(db, survey.id)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if db:
            db.close()
    
    return True
