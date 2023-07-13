from models import ScheduleMonth
from schemas import ScheduleMonthCreate, ScheduleMonthUpdate
from services.base import ServiceBase


class ScheduleMonthService(ServiceBase[ScheduleMonth,
                                       ScheduleMonthCreate,
                                       ScheduleMonthUpdate]):
    pass

schedule_month_service = ScheduleMonthService(ScheduleMonth)
