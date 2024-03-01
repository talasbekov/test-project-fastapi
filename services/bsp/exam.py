import json
import uuid
import datetime

from sqlalchemy import extract, text, func, and_, or_
from sqlalchemy.orm import Session
from models import ExamSchedule, ScheduleYear, User, ExamResult
from schemas import (ExamScheduleCreate,
                     ExamScheduleUpdate,
                     ExamScheduleCreateWithInstructors)
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
        if exams is not None or exams != []:
            for exam_schedule in exams:
                for group in exam_schedule.schedule.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return {'total': total, 'objects': exams}

    def get_for_tablet(
        self, db: Session, skip: int = 0, limit: int = 100
    ):
        exams = (db.query(self.model)
                 .join(ScheduleYear)
                 .filter(ScheduleYear.is_active == True)
                 .offset(skip)
                 .limit(limit)
                 .all())
        results = []
        for exam in exams:
            results.extend(db.query(ExamResult)
                           .filter(ExamResult.exam_id == str(exam.id))
                           .all())
        if exams is not None or exams != []:
            for exam_schedule in exams:
                for group in exam_schedule.schedule.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return {'exams': exams, 'results': results}

    def get_users_by_exam(self,
                          db: Session,
                          exam_id: str):
        users = (db.query(User.id)
                   .join(ScheduleYear.users)
                   .join(ScheduleYear.exams)
                   .filter(ExamSchedule.id == exam_id)
                   .all())
        return users

    def get_exam_results_by_user_id(self, db: Session,
                                    user_id: str,
                                    skip: int,
                                    limit: int):
        results = (db.query(ExamResult)
                   .filter(ExamResult.user_id == user_id)
                   .order_by(ExamResult.exam_date.desc())
                   .offset(skip)
                   .limit(limit)
                   .all())
        total = db.query(self.model).filter(ExamResult.user_id == user_id).count()
        if results is not None or results != []:
            for exam_schedule in results:
                for group in exam_schedule.schedule.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return {'total': total, 'objects': results}


    def create(self, db: Session, body: ExamScheduleCreateWithInstructors):
        params = {'start_date': str(body.start_date),
                  'end_date': str(body.end_date),
                  'start_time': str(body.start_time),
                  'end_time': str(body.end_time),
                  'place_id': str(body.place_id),
                  'schedule_id': str(body.schedule_id),
                  'id': str(uuid.uuid4())}
        db.execute(text("""
                        INSERT INTO HR_ERP_EXAM_SCHEDULES
                        (start_date, end_date, start_time, end_time, place_id, schedule_id, id)
                        VALUES(TO_DATE(:start_date, 'YYYY-MM-DD'),
                               TO_DATE(:end_date, 'YYYY-MM-DD'),
                               TO_DATE(:start_time, 'HH24:MI:SS'),
                               TO_DATE(:end_time, 'HH24:MI:SS'),
                               :place_id,
                               :schedule_id,
                               :id)
                        """),
                   params)
        db.flush()
        exam_schedule = self.get_by_id(db, params['id'])

        if body.instructor_ids != [] and body.instructor_ids is not None:
            instructors = [user_service.get_by_id(db, str(user_id))
                           for user_id in body.instructor_ids]
            exam_schedule.instructors = instructors

        db.add(exam_schedule)
        db.flush()

        return exam_schedule

    def get_by_month_and_schedule_year(self,
                                       db: Session,
                                       month_numbers: int,
                                       schedule_id: str):
        schedule = (
            db.query(ExamSchedule)
            .join(ScheduleYear)
            .filter(extract('month', ExamSchedule.start_date) == month_numbers,
                    ExamSchedule.schedule_id == schedule_id,
                    ScheduleYear.is_active == True)
            .first()
        )
        if schedule is not None:
            for group in schedule.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return schedule

    def get_nearest_exams(self,
                              db: Session,
                              user_id: str,
                              limit: int):
        current_time = datetime.datetime.now().time()
        current_date = datetime.date.today()

        closest_schedules = (db.query(ExamSchedule)
                             .join(ScheduleYear)
                             .join(ScheduleYear.users)
                             .filter(or_((ExamSchedule.start_date > current_date),
                                     and_(ExamSchedule.start_date == current_date,
                                          func.to_char(ExamSchedule.start_time,
                                                       'HH24:MI:SS')
                                          > str(current_time)))
                                     )
                             .filter(ExamSchedule.end_date >= current_date)
                             .filter(User.id == user_id,
                                     ScheduleYear.is_active == True)
                             .order_by(ExamSchedule.start_date,
                                       func.to_char(ExamSchedule.start_time, 'HH24:MI:SS'))
                             .limit(limit)
                             .all()
                             )

        for schedule_month in closest_schedules:
            for group in schedule_month.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return closest_schedules


    def get_exams_by_month(self,
                              db: Session,
                              user_id: str,
                              month_number: int):
        current_year = datetime.date.today().year
        schedules = (
            db.query(ExamSchedule)
            .join(ScheduleYear)
            .join(ScheduleYear.users)
            .filter(User.id == user_id,
                    extract('month', ExamSchedule.start_date) == month_number,
                    extract('year', ExamSchedule.start_date) == current_year,
                    ScheduleYear.is_active == True)
            .all()
        )

        for schedule_month in schedules:
            for group in schedule_month.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return schedules

    def get_exams_by_day(self,
                            db: Session,
                            user_id: str,
                            date: datetime.date,
                            limit: int):
        schedules = (db.query(ExamSchedule)
                             .join(ScheduleYear)
                             .filter(ExamSchedule.start_date <= date,
                                     ExamSchedule.end_date >= date,
                                     )
                             .filter(User.id == user_id,
                                     ScheduleYear.is_active == True)
                             .order_by(ExamSchedule.start_date,
                                       func.to_char(ExamSchedule.start_time, 'HH24:MI:SS'))
                             .limit(limit)
                             .all()
                             )

        for schedule_month in schedules:
            for group in schedule_month.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return schedules

    def get_by_schedule_year_id(self,
                                db: Session,
                                schedule_id: str):
        schedules = (
            db.query(ExamSchedule)
            .filter(ExamSchedule.schedule_id == schedule_id)
            .all()
        )
        if schedules is not None:
            for exam in schedules:
                for group in exam.schedule.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return schedules

    def remove(self, db: Session, id: str):
        exam = self.get(db, id)
        if exam is not None:
            db.delete(exam)
            db.flush()
            if exam.schedule is not None:
                for group in exam.schedule.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)
        return exam



exam_service = ExamService(ExamSchedule)
