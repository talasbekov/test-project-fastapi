from models import ScheduleDay
from schemas import ScheduleDayCreate, ScheduleDayUpdate
from services.base import ServiceBase


class ScheduleDayService(ServiceBase[ScheduleDay,
                                     ScheduleDayCreate,
                                     ScheduleDayUpdate]):
    pass

schedule_day_service = ScheduleDayService(ScheduleDay)
