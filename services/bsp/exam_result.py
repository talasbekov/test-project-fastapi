import datetime
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Session

from exceptions import BadRequestException
from models import ExamResult, ClassStatus
from schemas import (ExamResultCreate,
                     ExamResultUpdate,
                     ExamChangeResults,
                     ExamResultRead,)
from services.base import ServiceBase
from .exam import exam_service


class ExamResultService(ServiceBase[ExamResult, ExamResultCreate, ExamResultUpdate]):

    def get_users_results_by_exam(self, db: Session,
                                    exam_id: uuid.UUID):

        exam_schedule = exam_service.get_by_id(db, str(exam_id))

        users_results = (db.query(ExamResult)
                         .filter(ExamResult.exam_id == exam_id)
                         .all())

        exam_schedule.class_status = ClassStatus.STARTED

        db.add(exam_schedule)
        db.flush()

        return [ExamResultRead.from_orm(user_result) for user_result in users_results]


    def get_exam_results_by_user_id(self, db: Session,
                                    user_id: uuid.UUID,
                                    skip: int,
                                    limit: int):
        results = (db.query(ExamResult)
                   .filter(ExamResult.user_id == user_id,
                           ExamResult.is_active == True)
                   .order_by(ExamResult.exam_date.desc())
                   .offset(skip)
                   .limit(limit)
                   .all())
        total = (db.query(ExamResult)
                 .filter(ExamResult.user_id == user_id,
                                  ExamResult.is_active == True)
                 .count())
        return {'total': total, 'objects': results}

    def create_exam_results_by_exam(self, db: Session, exam_id: str, users):
        for user in users:
            # super().create(db, ExamResultCreate(exam_date=datetime.date.today(),
            #                                     grade=None,
            #                                     user_id=user.id,
            #                                     exam_id=exam_id,
            #                                     is_active=False)
            #                )
            params = {'exam_date': str(datetime.date.today()),
                      'grade': None,
                      'user_id': user.id,
                      'exam_id': exam_id,
                      'is_active': False,
                      'id': str(uuid.uuid4())}
            db.execute(text("""
                            INSERT INTO HR_ERP_EXAM_RESULTS
                            (exam_date, grade, user_id, exam_id, is_active, id)
                            VALUES(TO_DATE(:exam_date, 'YYYY-MM-DD'),
                                   :grade,
                                   :user_id,
                                   :exam_id,
                                   :is_active,
                                   :id)
                            """),
                       params)
            db.flush()

        db.commit()


    def change_exam_results(self, db: Session,
                                  body: ExamChangeResults):

        exam_schedule = exam_service.get_by_id(db, str(body.exam_id))

        if body.users_results is None:
            raise BadRequestException(
                detail=f"Got unexpected user_status {body}")
        for user_result in body.users_results:
            (
                db.query(ExamResult)
                .filter(ExamResult.exam_id == body.exam_id)
                .filter(ExamResult.user_id == user_result.user_id)
                .update(
                    {ExamResult.grade: user_result.grade,
                     ExamResult.results: user_result.results,
                     ExamResult.exam_date: datetime.date.today(),
                     ExamResult.is_active: True
                     }
                )
            )

        exam_schedule.class_status = ClassStatus.STARTED

        db.add(exam_schedule)
        db.flush()

        db.commit()
        return None

exam_result_service = ExamResultService(ExamResult)
