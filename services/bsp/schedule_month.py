import datetime
import uuid

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

    def get_schedule_by_day(self,
                            db: Session,
                            user_id: uuid.UUID,
                            date: datetime.date,
                            limit: int):
        today_weekday = date.isoweekday()

        schedule_days = (db.query(ScheduleDay.id)
                         .join(Day)
                         .filter(Day.order == today_weekday)
                         .order_by(Day.order, ScheduleDay.start_time)
                         .limit(limit)
                         .subquery()
                         )

        schedules = (db.query(ScheduleMonth)
                     .join(ScheduleMonth.days)
                     .join(ScheduleYear)
                     .join(ScheduleYear.users)
                     .filter(User.id == user_id,
                             ScheduleDay.id.in_(schedule_days),
                             ScheduleYear.is_active == True)
                     .all()
                     )

        return schedules


schedule_month_service = ScheduleMonthService(ScheduleMonth)
