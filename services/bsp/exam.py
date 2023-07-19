import uuid
from sqlalchemy.orm import Session
from models import ExamSchedule, ExamResult
from schemas import (ExamScheduleCreate,
                     ExamScheduleUpdate,
                     ExamScheduleCreateWithInstructors,)
from services import user_service
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

    def create(self, db: Session, body: ExamScheduleCreateWithInstructors):
        exam_schedule = super().create(db,
                                        ExamScheduleCreate(
                                            start_date=body.start_date,
                                            end_date=body.end_date,
                                            start_time=body.start_time,
                                            end_time=body.end_time,
                                            place_id=body.place_id,
                                        ))

        instructors = [user_service.get_by_id(db, user_id)
                       for user_id in body.instructor_ids]
        exam_schedule.instructors = instructors

        db.add(exam_schedule)
        db.flush()

        return exam_schedule

exam_service = ExamService(ExamSchedule)
