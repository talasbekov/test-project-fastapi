import datetime
import uuid

from sqlalchemy import extract
from sqlalchemy.orm import Session

from models import ScheduleMonth, ScheduleDay, ScheduleYear, User, Day
from schemas import (ScheduleMonthCreate,
                     ScheduleMonthUpdate,
                     ScheduleMonthCreateWithDay,
                     ScheduleDayCreate)
from services.base import ServiceBase
from .schedule_day import schedule_day_service
from .day import day_service
from .. import user_service


class ScheduleMonthService(ServiceBase[ScheduleMonth,
                                       ScheduleMonthCreate,
                                       ScheduleMonthUpdate]):
    from datetime import datetime, timedelta

    def _get_dates_of_weekday(start_date, end_date, weekday):
        # Convert the weekday input to lowercase and get the corresponding weekday number
        weekdays = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }
        weekday_number = weekdays.get(weekday.lower(), None)

        if weekday_number is None:
            raise ValueError(
                "Invalid weekday. Please choose from: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday.")

        dates = []
        current_date = start_date

        # Iterate through the date range and find the dates that match the specified weekday
        while current_date <= end_date:
            if current_date.weekday() == weekday_number:
                dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

        return dates

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ):
        schedules = (db.query(self.model)
                     .join(ScheduleYear)
                     .filter(ScheduleYear.is_active == True)
                     .offset(skip)
                     .limit(limit)
                     .all())

        return schedules

    def create(self, db: Session, body: ScheduleMonthCreateWithDay):
        schedule_month = super().create(db,
                                        ScheduleMonthCreate(
                                            start_date=body.start_date,
                                            end_date=body.end_date,
                                            place_id=body.place_id,
                                            schedule_id=body.schedule_id
                                        ))

        instructors = [user_service.get_by_id(db, user_id)
                       for user_id in body.instructor_ids]
        schedule_month.instructors = instructors

        for schedule_day in body.days:
            day = day_service.get_day_by_name(db, schedule_day.day)
            schedule_day_service.create(db,
                                        ScheduleDayCreate(
                                            day_id=day.id,
                                            start_time=schedule_day.start_time,
                                            end_time=schedule_day.end_time,
                                            month_id=schedule_month.id
                                        ))

        db.add(schedule_month)
        db.flush()

        return schedule_month

    def get_nearest_schedules(self,
                              db: Session,
                              user_id: uuid.UUID,
                              limit: int):
        current_time = datetime.datetime.now().time()
        today_weekday = datetime.date.today().isoweekday()

        schedule_days = (db.query(ScheduleDay.id)
                         .join(Day)
                         .filter(Day.order >= today_weekday,
                                 ScheduleDay.start_time > current_time)
                         .order_by(Day.order, ScheduleDay.start_time)
                         .limit(limit)
                         .subquery()
                         )

        closest_schedules = (db.query(ScheduleMonth)
                             .join(ScheduleMonth.days)
                             .join(ScheduleYear)
                             .join(ScheduleYear.users)
                             .filter(User.id == user_id,
                                     ScheduleDay.id.in_(schedule_days),
                                     ScheduleYear.is_active == True)
                             .all()
                             )

        return closest_schedules


    def get_schedules_by_month(self,
                              db: Session,
                              user_id: uuid.UUID,
                              month_number: int):
        schedules = (
            db.query(ScheduleMonth)
            .join(ScheduleYear)
            .join(ScheduleYear.users)
            .filter(User.id == user_id,
                    extract('month', ScheduleMonth.start_date) == month_number,
                    ScheduleYear.is_active == True)
            .all()
        )

        return schedules

    def get_by_month_and_schedule_year(self,
                              db: Session,
                              month_numbers: int,
                              schedule_id: uuid.UUID):
        schedule = (
            db.query(ScheduleMonth)
            .join(ScheduleYear)
            .filter(extract('month', ScheduleMonth.start_date) == month_numbers,
                    ScheduleMonth.schedule_id == schedule_id,
                    ScheduleYear.is_active == True)
            .first()
        )

        return schedule


    def get_by_schedule_year_id(self,
                              db: Session,
                              schedule_id: uuid.UUID):
        schedules = (
            db.query(ScheduleMonth)
            .filter(ScheduleMonth.schedule_id == schedule_id)
            .all()
        )

        return schedules


    def get_schedule_by_day(self,
                            db: Session,
                            user_id: uuid.UUID,
                            date: datetime.date,
                            limit: int):
        date_weekday = date.isoweekday()

        schedule_days = (db.query(ScheduleDay.id)
                         .join(Day)
                         .filter(Day.order == date_weekday)
                         .order_by(ScheduleDay.start_time)
                         .limit(limit)
                         .subquery()
                         )

        schedules = (db.query(ScheduleMonth)
                     .join(ScheduleMonth.days)
                     .join(ScheduleYear)
                     .join(ScheduleYear.users)
                     .filter(User.id == user_id,
                             ScheduleDay.id.in_(schedule_days),
                             ScheduleYear.is_active == True,
                             ScheduleMonth.start_date <= date,
                             ScheduleMonth.end_date >= date)
                     .all()
                     )

        return schedules


schedule_month_service = ScheduleMonthService(ScheduleMonth)
