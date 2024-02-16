import datetime
import pickle
import logging
import asyncio

from celery import Celery
from celery.schedules import crontab
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from core import configs
from schemas import HrDocumentRead
from services import staff_list_service, survey_service, hr_document_service, history_service
from schemas.staff_list import StaffListUserCreate, StaffListRead
from models import UserLoggingActivity, SurveyRepeatTypeEnum


app = Celery('celery_app', backend='redis://redis:6379/',
             broker='amqp://rabbitmq:5672/', timezone='Asia/Almaty',
             include=['tasks.celery_app'])


app.conf.beat_schedule = {
    'clear_user_logging_activities_table_every_3_days': {
        'task': 'tasks.celery_app.task_clear_user_' +
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
    },
    # 'send_expiring_documents_notifications': {
    #     'task': 'tasks.celery_app.check_expiring_documents',
    #     'schedule': crontab(minute='*'),
    # }

}

# SQLALCHEMY_DATABASE_URL = f"oracle://system:Oracle123@172.20.0.2:1521/MORAL"
SQLALCHEMY_DATABASE_URL = f"oracle://system:Oracle123@192.168.0.61:1521/MORAL"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL2,
    echo=configs.SQLALCHEMY_ECHO,
    pool_size=10
)


@app.task(bind=True)
def task_create_draft(self,
                      user_id: str,
                      obj_in: dict,
                      current_user_role_id: str):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    db = SessionLocal()
    staff_list = staff_list_service.apply_staff_list(self, db,
                                                     str(id),
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
    db = SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)
    try:
        now_date = datetime.datetime.now()
        delete_objects = (
            db.query(UserLoggingActivity).filter(
                UserLoggingActivity.signed_at < now_date -
                datetime.timedelta(days=3)
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
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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


@app.task(bind=True)
def task_sign_document_with_certificate(
    self,
    byte_body,
    user_id,
    access_token,
):
    print("what")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    body = pickle.loads(byte_body)
    state_counter = 0
    self.update_state(state=state_counter)
    print("wtfffff")
    # hr_documents = []
    percent_per_document = 100/len(body.document_ids)
    for document_id in body.document_ids:
        
        state_counter += percent_per_document
        hr_document_service.sign_with_certificate(
            db,
            document_id,
            body,
            user_id,
            access_token)
        # hr_document_service._create_notification_for_subject(db, document_id)
        # hr_documents.append(HrDocumentRead.from_orm(hr_document).dict())
        self.update_state(state=state_counter)
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if db:
            db.close()
    # return hr_documents
            

async def check_expiring_documents():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    contracts = history_service.get_expiring_contracts(db)
    print(contracts)
    for contract in contracts:
        await hr_document_service.send_expiring_notification(db, contract.user_id, contract.id)
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if db:
            db.close()

async def minimal_async_operation():
    # Simulate an async operation, e.g., fetching data
    await asyncio.sleep(1)  # Simulate async I/O operation
    return {'data': 'example'}


@app.task(bind=True)
def check_expiring_documents(self):
    try:
        res = asyncio.run(minimal_async_operation())
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
