from sqlalchemy.orm import Session

from models import ScheduleMonth
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



schedule_month_service = ScheduleMonthService(ScheduleMonth)
