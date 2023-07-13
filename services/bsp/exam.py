import uuid
from sqlalchemy.orm import Session
from models import ExamSchedule, ExamResult
from schemas import ExamScheduleCreate, ExamScheduleUpdate
from services.base import ServiceBase


class ExamService(ServiceBase[ExamSchedule, ExamScheduleCreate, ExamScheduleUpdate]):
    def get_exam_results_by_user_id(self, db: Session,
                                    user_id: uuid.UUID,
                                    skip: int,
                                    limit: int):
        results = (db.query(ExamResult)
                   .filter(ExamResult.user_id == user_id)
                   .offset(skip)
                   .limit(limit)
                   .order_by(ExamResult.exam_date.desc())
                   .all())

        return results

exam_service = ExamService(ExamSchedule)
