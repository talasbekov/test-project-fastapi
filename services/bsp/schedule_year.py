import uuid

from sqlalchemy.orm import Session

from models import ScheduleYear, BspPlan, StaffDivision
from schemas import (ScheduleYearCreate,
                     ScheduleYearUpdate,
                     ScheduleYearCreateString,
                     ScheduleYearRead, )
from services.base import ServiceBase
from services import staff_division_service, user_service
from .month import month_service
from .schedule_month import schedule_month_service
from .exam import exam_service


class ScheduleYearService(ServiceBase[ScheduleYear,
                                      ScheduleYearCreate,
                                      ScheduleYearUpdate]):

    def get_multi(
            self, db: Session, skip: int = 0, limit: int = 100
    ):
        total = (db.query(self.model)
                 .filter(ScheduleYear.is_active == True)
                 .count())
        schedules = (db.query(self.model)
                     .filter(ScheduleYear.is_active == True)
                     .offset(skip)
                     .limit(limit)
                     .all())

        schedules = [ScheduleYearRead.from_orm(schedule).dict()
                     for schedule in schedules]
        for schedule in schedules:

            activity_months = schedule['activity_months']

            for activity_month in activity_months:
                schedule_months = schedule_month_service.get_by_month_and_schedule_year(
                    db, activity_month['order'], schedule['id'])

                if schedule_months is None:
                    activity_month['has_schedule_month'] = True
                else:
                    activity_month['has_schedule_month'] = False

            exam_months = schedule['exam_months']

            for exam_month in exam_months:
                schedule_months = exam_service.get_by_month_and_schedule_year(
                    db, exam_month['order'], schedule['id'])

                if schedule_months is None:
                    exam_month['has_schedule_month'] = True
                else:
                    exam_month['has_schedule_month'] = False

        return {'total': total, 'objects': schedules}

    def remove_staff_division_from_schedule(self, db: Session,
                                            schedule_id: uuid.UUID,
                                            division_id: uuid.UUID):
        staff_division_service.get_by_id(db, division_id)
        self.get_by_id(db, schedule_id)
        obj = (db.query(ScheduleYear)
               .join(ScheduleYear.staff_divisions)
               .filter(ScheduleYear.id == schedule_id,
                       StaffDivision.id == division_id)
               .first()
               )
        if obj.staff_divisions is None:
            super().remove(db, str(schedule_id))

        db.delete(obj)
        db.flush()

        return obj

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
        total = (db.query(self.model)
                 .join(BspPlan, )
                 .filter(BspPlan.year == year,
                         ScheduleYear.is_active == True)
                 .count())
        return {'total': total, 'objects': schedules}

    def get_all_by_plan_id(self,
                           db: Session,
                           id: uuid.UUID):
        schedules = (db.query(ScheduleYear)
                     .join(BspPlan)
                     .filter(BspPlan.id == id,
                             ScheduleYear.is_active == True)
                     .all()
                     )
        total = (db.query(self.model)
                 .join(BspPlan)
                 .filter(BspPlan.id == id,
                         ScheduleYear.is_active == True)
                 .count())
        return {'total': total, 'objects': schedules}

    def get_by_schedule_month_id(self,
                                 db: Session,
                                 month_id: uuid.UUID) -> ScheduleYearRead:
        month = schedule_month_service.get_by_id(db, month_id)
        year = (db.query(ScheduleYear)
                .filter(ScheduleYear.id == month.schedule_id,
                        ScheduleYear.is_active == True)
                .first()
                )
        total = (db.query(self.model)
                 .filter(ScheduleYear.id == month.schedule_id,
                         ScheduleYear.is_active == True)
                 .count())
        return {'total': total, 'objects': year}

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

        total = (db.query(self.model)
                 .join(ScheduleYear.staff_divisions)
                 .filter(StaffDivision.id == id,
                         ScheduleYear.is_active == True)
                 .count())
        return {'total': total, 'objects': schedules}

    def create_schedule(self, db: Session,
                        schedule: ScheduleYearCreateString):
        schedule_year = super().create(db, ScheduleYearCreate(
            is_exam_required=schedule.is_exam_required,
            retry_count=schedule.retry_count,
            plan_id=schedule.plan_id,
            activity_id=schedule.activity_id,
            is_active=True,
        ))
        staff_divisions = [staff_division_service.get_by_id(db, division_id)
                           for division_id in schedule.staff_division_ids]
        schedule_year.staff_divisions = staff_divisions

        users = []
        for staff_division in staff_divisions:
            users.extend(user_service.get_users_by_staff_division(db, staff_division))
        schedule_year.users = users


        activity_months = month_service.get_months_by_names(db,
                                                            schedule.activity_months)
        schedule_year.activity_months = activity_months

        if schedule.is_exam_required:
            exam_months = month_service.get_months_by_names(db,
                                                            schedule.exam_months)
            schedule_year.exam_months = exam_months

        db.add(schedule_year)
        db.flush()

        return schedule_year

    def send_all_to_draft_by_plan(self, db: Session, plan_id: uuid.UUID):
        (db.query(ScheduleYear)
         .filter(ScheduleYear.plan_id == plan_id)
         .update({self.model.is_active: False}))


schedule_year_service = ScheduleYearService(ScheduleYear)
