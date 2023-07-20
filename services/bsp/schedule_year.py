import uuid

from sqlalchemy.orm import Session

from models import ScheduleYear, BspPlan, StaffDivision
from schemas import (ScheduleYearCreate,
                     ScheduleYearUpdate,
                     ScheduleYearCreateString,
                     ScheduleYearRead, )
from services.base import ServiceBase
from services import staff_division_service
from .month import month_service
from .schedule_month import schedule_month_service


class ScheduleYearService(ServiceBase[ScheduleYear,
                                      ScheduleYearCreate,
                                      ScheduleYearUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ):
        return (db.query(self.model)
                .filter(ScheduleYear.is_active == True)
                .offset(skip)
                .limit(limit)
                .all())

    def get_all_by_plan_year(self,
                             db: Session,
                             year: int,
                             skip: int,
                             limit: int):
        schedules = (db.query(ScheduleYear)
                     .join(BspPlan, )
                     .filter(BspPlan.year == year,
                             ScheduleYear.is_active == True)
                     .offset(skip)
                     .limit(limit)
                     )
        return schedules


    def get_all_by_plan_id(self,
                           db: Session,
                           id: uuid.UUID):
        schedules = (db.query(ScheduleYear)
                     .join(BspPlan)
                     .filter(BspPlan.id == id,
                             ScheduleYear.is_active == True)
                     .all()
                     )
        return schedules

    def get_by_schedule_month_id(self,
                                 db: Session,
                                 month_id: uuid.UUID) -> ScheduleYearRead:
        month = schedule_month_service.get_by_id(db, month_id)
        year = (db.query(ScheduleYear)
                .filter(ScheduleYear.id == month.schedule_id,
                        ScheduleYear.is_active == True)
                .first()
                )
        return year

    def get_all_by_division_id(self,
                               db: Session,
                               id: uuid.UUID):
        staff_division_service.get_by_id(db, id)
        schedules = (db.query(ScheduleYear)
                     .join(ScheduleYear.staff_divisions)
                     .filter(StaffDivision.id == id,
                             ScheduleYear.is_active == True)
                     .all()
                     )
        return schedules

    def create_schedule(self, db: Session,
                        schedule: ScheduleYearCreateString):
        res = super().create(db, ScheduleYearCreate(
            is_exam_required=schedule.is_exam_required,
            retry_count=schedule.retry_count,
            plan_id=schedule.plan_id,
            activity_id=schedule.activity_id,
        ))
        staff_divisions = [staff_division_service.get_by_id(db, division_id)
                           for division_id in schedule.staff_division_ids]
        res.staff_divisions = staff_divisions

        activity_months = month_service.get_months_by_names(db,
                                                            schedule.activity_months)
        res.activity_months = activity_months

        if schedule.is_exam_required:
            exam_months = month_service.get_months_by_names(db,
                                                            schedule.exam_months)
            res.exam_months = exam_months

        db.add(res)
        db.flush()

        return res

    def send_all_to_draft_by_plan(self, db: Session, plan_id: uuid.UUID):
        (db.query(ScheduleYear)
         .filter(ScheduleYear.plan_id == plan_id)
         .update({self.model.is_active: False}))



schedule_year_service = ScheduleYearService(ScheduleYear)
