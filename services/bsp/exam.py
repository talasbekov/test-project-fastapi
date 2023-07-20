import uuid

from sqlalchemy import extract
from sqlalchemy.orm import Session
from models import ExamSchedule, ExamResult, ScheduleYear
from schemas import (ExamScheduleCreate,
                     ExamScheduleUpdate,
                     ExamScheduleCreateWithInstructors,)
from services import user_service
from services.base import ServiceBase


class ExamService(ServiceBase[ExamSchedule, ExamScheduleCreate, ExamScheduleUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ):
        exams = (db.query(self.model)
                 .join(ScheduleYear)
                 .filter(ScheduleYear.is_active == True)
                 .offset(skip)
                 .limit(limit)
                 .all())
        total = (db.query(self.model)
                 .join(ScheduleYear)
                 .filter(ScheduleYear.is_active == True)
                 .count())
        return {'total': total, 'objects': exams}

    def get_exam_results_by_user_id(self, db: Session,
                                    user_id: uuid.UUID,
                                    skip: int,
                                    limit: int):
        results = (db.query(ExamResult)
                   .filter(ExamResult.user_id == user_id)
                   .order_by(ExamResult.exam_date.desc())
                   .offset(skip)
                   .limit(limit)
                   .all())
        total = db.query(self.model).filter(ExamResult.user_id == user_id).count()
        return {'total': total, 'objects': results}

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

    def get_by_month_and_schedule_year(self,
                              db: Session,
                              month_numbers: int,
                              schedule_id: uuid.UUID):
        schedule = (
            db.query(ExamSchedule)
            .join(ScheduleYear)
            .filter(extract('month', ExamSchedule.start_date) == month_numbers,
                    ExamSchedule.schedule_id == schedule_id,
                    ScheduleYear.is_active == True)
            .first()
        )

        return schedule


exam_service = ExamService(ExamSchedule)
