import uuid

from sqlalchemy import text
from sqlalchemy.orm import Session

from models import ScheduleDay
from schemas import ScheduleDayCreate, ScheduleDayUpdate, ActivityDateCreate
from services.base import ServiceBase
from utils import get_iso_weekdays_between_dates
from .day import day_service
from .month import month_service
from .activity_date import activity_day_service


class ScheduleDayService(ServiceBase[ScheduleDay,
                                     ScheduleDayCreate,
                                     ScheduleDayUpdate]):
    def create_schedule_days(self, db: Session, schedule_month, days):
        for schedule_day in days:
            day = day_service.get_day_by_name(db, schedule_day.day)
            month_num = schedule_month.start_date.month
            activity_month = month_service.get_month_by_order(db, month_num)

            params = {'day_id': day.id,
                      'start_time': schedule_day.start_time.strftime('%H:%M:%S'),
                      'end_time': schedule_day.end_time.strftime('%H:%M:%S'),
                      'month_id': str(schedule_month.id),
                      'activity_month_id': str(activity_month.id),
                      'id': str(uuid.uuid4())}
            db.execute(text("""
                            INSERT INTO HR_ERP_SCHEDULE_DAYS
                            (day_id, start_time, end_time, month_id, activity_month_id, id)
                            VALUES(:day_id,
                                   TO_DATE(:start_time, 'HH24:MI:SS'),
                                   TO_DATE(:end_time, 'HH24:MI:SS'),
                                   :month_id,
                                   :activity_month_id,
                                   :id)
                            """),
                       params)

            new_schedule_day = schedule_day_service.get_by_id(db, params['id'])

            weekday_dates = get_iso_weekdays_between_dates(schedule_month.start_date,
                                                           schedule_month.end_date,
                                                           day.day_order)
            activity_dates = []
            for weekday_date in weekday_dates:
                activity_dates.append(
                    activity_day_service.create(db, ActivityDateCreate(
                        activity_date=weekday_date)
                    )
                )
            new_schedule_day.activity_dates = activity_dates
            db.add(new_schedule_day)
            db.flush()

schedule_day_service = ScheduleDayService(ScheduleDay)
