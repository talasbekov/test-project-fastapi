import uuid

from sqlalchemy.orm import Session

from models import ScheduleYear, BspPlan, StaffDivision
from schemas import (ScheduleYearCreate,
                     ScheduleYearUpdate,
                     ScheduleYearCreateString,
                     ScheduleYearRead, )
from services.base import ServiceBase
from services import staff_division_service
from .plan import plan_service
from .month import month_service
from .schedule_month import schedule_month_service


class ScheduleYearService(ServiceBase[ScheduleYear,
                                      ScheduleYearCreate,
                                      ScheduleYearUpdate]):
    def get_all_by_plan_year(self,
                             db: Session,
                             year: int,
                             skip: int,
                             limit: int):
        schedules = (db.query(ScheduleYear)
                     .join(BspPlan, )
                     .filter(BspPlan.year == year)
                     .offset(skip)
                     .limit(limit)
                     )
        return schedules

    def get_all_by_plan_id(self,
                           db: Session,
                           id: uuid.UUID):
        plan_service.get_by_id(db, id)
        schedules = (db.query(ScheduleYear)
                     .join(BspPlan)
                     .filter(BspPlan.id == id)
                     .all()
                     )
        return schedules

    def get_by_schedule_month_id(self,
                                 db: Session,
                                 month_id: uuid.UUID) -> ScheduleYearRead:
        month = schedule_month_service.get_by_id(db, month_id)
        year = (db.query(ScheduleYear)
                .filter(ScheduleYear.id == month.schedule_id)
                .first()
                )
        return year

    def get_all_by_division_id(self,
                               db: Session,
                               id: uuid.UUID):
        staff_division_service.get_by_id(db, id)
        schedules = (db.query(ScheduleYear)
                     .join(ScheduleYear.staff_divisions)
                     .filter(StaffDivision.id == id)
                     .all()
                     )
        return schedules

    def create_schedule(self, db: Session,
                        schedule: ScheduleYearCreateString):
        activity_months = month_service.get_months_by_names(db,
                                                            schedule.activity_months)
        exam_months = month_service.get_months_by_names(db,
                                                        schedule.exam_months)
        res = super().create(db, ScheduleYearCreate(
            is_exam_required=schedule.is_exam_required,
            retry_count=schedule.retry_count,
            plan_id=schedule.plan_id,
            activity_id=schedule.activity_id,
        ))

        res.activity_months = activity_months
        res.exam_months = exam_months

        db.add(res)
        db.flush()

        return res


schedule_year_service = ScheduleYearService(ScheduleYear)
