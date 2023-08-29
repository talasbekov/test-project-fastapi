import datetime
import json
import uuid

from sqlalchemy import extract, or_, and_, func
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from utils import get_iso_weekdays_between_dates

from models import (ScheduleMonth,
                    ScheduleDay,
                    ScheduleYear,
                    User,
                    Day,
                    ActivityDate,)
from schemas import (ScheduleMonthCreate,
                     ScheduleMonthUpdate,
                     ScheduleMonthCreateWithDay,
                     ScheduleDayCreate,
                     ActivityDateCreate,)

from services.base import ServiceBase

from .schedule_day import schedule_day_service
from .activity_date import activity_day_service
from .day import day_service
from .month import month_service
from services import user_service


class ScheduleMonthService(ServiceBase[ScheduleMonth,
                                       ScheduleMonthCreate,
                                       ScheduleMonthUpdate]):
    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ):
        schedules = (db.query(self.model)
                     .join(ScheduleYear)
                     .filter(ScheduleYear.is_active == True)
                     .offset(skip)
                     .limit(limit)
                     .all())
        for schedule_month in schedules:
            for group in schedule_month.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return schedules

    def create(self, db: Session, body: ScheduleMonthCreateWithDay):
        params = {'start_date': str(body.start_date),
                  'end_date': str(body.end_date),
                  'place_id': str(body.place_id),
                  'schedule_id': str(body.schedule_id),
                  'id': str(uuid.uuid4())}
        db.execute(text("""
                        INSERT INTO HR_ERP_SCHEDULE_MONTHS
                        (start_date, end_date, place_id, schedule_id, id)
                        VALUES(TO_DATE(:start_date, 'YYYY-MM-DD'),
                               TO_DATE(:end_date, 'YYYY-MM-DD'),
                               :place_id,
                               :schedule_id,
                               :id)
                        """),
                   params)
        db.flush()
        schedule_month = self.get_by_id(db, params['id'])
        if body.instructor_ids != [] and body.instructor_ids is not None:
            instructors = [user_service.get_by_id(db, str(user_id))
                           for user_id in body.instructor_ids]
            schedule_month.instructors = instructors

        db.add(schedule_month)
        db.flush()

        schedule_day_service.create_schedule_days(db, schedule_month, body.days)

        db.commit()

        for group in schedule_month.schedule.staff_divisions:
            if isinstance(group.description, str):
                group.description = json.loads(group.description)

        return schedule_month

    def get_nearest_schedules(self,
                              db: Session,
                              user_id: str,
                              limit: int):
        current_time = datetime.datetime.now().time()
        current_date = datetime.date.today()

        closest_schedules = (db.query(ScheduleMonth)
                             .join(ScheduleMonth.days)
                             .join(ScheduleYear)
                             .join(ScheduleYear.users)
                             .join(ScheduleDay.activity_dates)
                             .join(Day)
                             .filter(or_((ActivityDate.activity_date > current_date),
                                     and_(ActivityDate.activity_date == current_date,
                                          func.to_char(ScheduleDay.start_time, 'HH24:MI:SS') > str(current_time)))
                                     )
                             .filter(ScheduleMonth.end_date >= current_date)
                             .filter(User.id == user_id,
                                     ScheduleYear.is_active == True)
                             .order_by(ActivityDate.activity_date,
                                       func.to_char(ScheduleDay.start_time, 'HH24:MI:SS'))
                             .limit(limit)
                             .all()
                             )

        for schedule_month in closest_schedules:
            for group in schedule_month.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return closest_schedules


    def get_schedules_by_month(self,
                              db: Session,
                              user_id: str,
                              month_number: int):
        current_year = datetime.date.today().year
        schedules = (
            db.query(ScheduleMonth)
            .join(ScheduleYear)
            .join(ScheduleYear.users)
            .filter(User.id == user_id,
                    extract('month', ScheduleMonth.start_date) == month_number,
                    extract('year', ScheduleMonth.start_date) == current_year,
                    ScheduleYear.is_active == True)
            .all()
        )

        for schedule_month in schedules:
            for group in schedule_month.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return schedules

    def get_by_month_and_schedule_year(self,
                              db: Session,
                              month_numbers: int,
                              schedule_id: str):
        schedule = (
            db.query(ScheduleMonth)
            .join(ScheduleYear)
            .filter(extract('month', ScheduleMonth.start_date) == month_numbers,
                    ScheduleMonth.schedule_id == schedule_id,
                    ScheduleYear.is_active == True)
            .first()
        )
        if schedule is not None and schedule.schedule is not None:
            for group in schedule.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return schedule


    def get_by_schedule_year_id(self,
                              db: Session,
                              schedule_id: str):
        schedules = (
            db.query(ScheduleMonth)
            .filter(ScheduleMonth.schedule_id == schedule_id)
            .all()
        )

        for schedule_month in schedules:
            for group in schedule_month.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return schedules


    def get_schedule_by_day(self,
                            db: Session,
                            user_id: str,
                            date: datetime.date,
                            limit: int):
        schedules = (db.query(ScheduleMonth)
                             .join(ScheduleMonth.days)
                             .join(ScheduleYear)
                             .join(ScheduleYear.users)
                             .join(ScheduleDay.activity_dates)
                             .join(Day)
                             .filter(ActivityDate.activity_date == date,
                                     ScheduleMonth.start_date <= date,
                                     ScheduleMonth.end_date >= date,
                                     )
                             .filter(User.id == user_id,
                                     ScheduleYear.is_active == True)
                             .order_by(ActivityDate.activity_date,
                                       func.to_char(ScheduleDay.start_time, 'HH24:MI:SS'))
                             .limit(limit)
                             .all()
                             )

        for schedule_month in schedules:
            for group in schedule_month.schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return schedules


schedule_month_service = ScheduleMonthService(ScheduleMonth)
