import uuid
import json
import datetime

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import (ScheduleYear,
                    BspPlan,
                    StaffDivision,
                    Activity,
                    Month,)
from schemas import (ScheduleYearCreate,
                     ScheduleYearUpdate,
                     ScheduleYearCreateString,
                     ScheduleYearRead,)
from services.base import ServiceBase
from services import staff_division_service, user_service
from .month import month_service
from .schedule_month import schedule_month_service
from .exam import exam_service


class ScheduleYearService(ServiceBase[ScheduleYear,
                                      ScheduleYearCreate,
                                      ScheduleYearUpdate]):

    def set_has_schedule_month(self, db: Session, schedules):
        schedules = [ScheduleYearRead.from_orm(schedule).dict()
                     for schedule in schedules]
        for schedule in schedules:

            activity_months = schedule['activity_months']

            for activity_month in activity_months:
                schedule_month = schedule_month_service.get_by_month_and_schedule_year(
                    db, activity_month['month_order'], schedule['id'])

                if schedule_month is None:
                    activity_month['has_schedule_month'] = True
                else:
                    activity_month['has_schedule_month'] = False

            exam_months = schedule['exam_months']

            for exam_month in exam_months:
                schedule_months = exam_service.get_by_month_and_schedule_year(
                    db, exam_month['month_order'], schedule['id'])

                if schedule_months is None:
                    exam_month['has_schedule_month'] = True
                else:
                    exam_month['has_schedule_month'] = False

        return schedules

    def get_multi(
            self, db: Session, filter: str = '', skip: int = 0, limit: int = 100
    ):
        current_date = datetime.date.today()
        current_year_month = str(current_date.year) + str(current_date.month)

        total = (db.query(self.model)
                 .filter(ScheduleYear.is_active == True)
                 )
        schedules = (db.query(self.model)
                     .join(BspPlan)
                     .join(ScheduleYear.activity_months)
                     .filter(ScheduleYear.is_active == True,
                             func.concat(BspPlan.year, Month.month_order) >=
                             (current_year_month),
                             )
                     )

        if filter != '':
            total = self._add_filter_to_query(total, filter)
            schedules = self._add_filter_to_query(schedules, filter)

        total = total.count()
        schedules = (
            schedules
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        for schedule in schedules:
            for group in schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        schedules = self.set_has_schedule_month(db, schedules)

        return {'total': total, 'objects': schedules}

    def remove_staff_division_from_schedule(self, db: Session,
                                            schedule_id: str,
                                            division_id: str):
        staff_division_service.get_by_id(db, str(division_id))
        self.get_by_id(db, str(schedule_id))
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
                     .order_by(self.model.created_at.desc())
                     .offset(skip)
                     .limit(limit)
                     .all()
                     )
        total = (db.query(self.model)
                 .join(BspPlan, )
                 .filter(BspPlan.year == year,
                         ScheduleYear.is_active == True)
                 .count())

        for schedule in schedules:
            for group in schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return {'total': total, 'objects': schedules}

    def get_all_by_plan_id(self,
                           db: Session,
                           id: str):
        schedules = (db.query(ScheduleYear)
                     .join(BspPlan)
                     .filter(BspPlan.id == id,
                             ScheduleYear.is_active == True)
                     .order_by(self.model.created_at.desc())
                     .all()
                     )
        total = (db.query(self.model)
                 .join(BspPlan)
                 .filter(BspPlan.id == id,
                         ScheduleYear.is_active == True)
                 .count())

        for schedule in schedules:
            for group in schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return {'total': total, 'objects': schedules}

    def get_by_schedule_month_id(self,
                                 db: Session,
                                 month_id: str) -> ScheduleYearRead:
        month = schedule_month_service.get_by_id(db, str(month_id))
        year = (db.query(ScheduleYear)
                .filter(ScheduleYear.id == month.schedule_id,
                        ScheduleYear.is_active == True)
                .first()
                )
        total = (db.query(self.model)
                 .filter(ScheduleYear.id == month.schedule_id,
                         ScheduleYear.is_active == True)
                 .count())

        for group in year.staff_divisions:
            if isinstance(group.description, str):
                group.description = json.loads(group.description)

        return {'total': total, 'objects': year}

    def get_all_by_division_id(self,
                               db: Session,
                               id: str):
        staff_division_service.get_by_id(db, str(id))
        schedules = (db.query(ScheduleYear)
                     .join(ScheduleYear.staff_divisions)
                     .filter(StaffDivision.id == id,
                             ScheduleYear.is_active == True)
                     .order_by(self.model.created_at.desc())
                     .all()
                     )

        total = (db.query(self.model)
                 .join(ScheduleYear.staff_divisions)
                 .filter(StaffDivision.id == id,
                         ScheduleYear.is_active == True)
                 .count())

        for schedule in schedules:
            for group in schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

        return {'total': total, 'objects': schedules}


    def get_all_by_division_id_and_plan_id(self,
                               db: Session,
                               id: str,
                               plan_id: str):
        schedules = (db.query(ScheduleYear)
                     .join(ScheduleYear.staff_divisions)
                     .filter(StaffDivision.id == str(id),
                             ScheduleYear.plan_id == str(plan_id))
                     .order_by(self.model.created_at.desc())
                     .all()
                     )

        total = (db.query(ScheduleYear)
                 .join(ScheduleYear.staff_divisions)
                 .filter(StaffDivision.id == str(id),
                         ScheduleYear.plan_id == str(plan_id))
                 .count())

        for schedule in schedules:
            for group in schedule.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)

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
        staff_divisions = [staff_division_service.get_by_id(db, str(division_id))
                           for division_id in schedule.staff_division_ids]
        for group in staff_divisions:
            for staff_unit in group.staff_units:
                if isinstance(staff_unit.requirements, list):
                    staff_unit.requirements = json.dumps(staff_unit.requirements)
            if isinstance(group.description, dict):
                group.description = json.dumps(group.description)
        schedule_year.staff_divisions = staff_divisions

        users = []
        for staff_division in staff_divisions:
            users.extend(user_service.get_users_by_staff_division(db, staff_division))
        schedule_year.users = list(set(users))

        activity_months = month_service.get_months_by_names(db,
                                                            schedule.activity_months)
        schedule_year.activity_months = activity_months

        if schedule.is_exam_required:
            exam_months = month_service.get_months_by_names(db,
                                                            schedule.exam_months)
            schedule_year.exam_months = exam_months

        db.add(schedule_year)
        db.flush()
        db.commit()

        for group in schedule_year.staff_divisions:
            if isinstance(group.description, str):
                group.description = json.loads(group.description)

        return schedule_year

    def send_all_to_draft_by_plan(self, db: Session, plan_id: str):
        (db.query(ScheduleYear)
         .filter(ScheduleYear.plan_id == plan_id)
         .update({self.model.is_active: False}))

    def _add_filter_to_query(self, query, filter):
        key_words = [word + '%' for word in filter.lower().split()]
        
        filter_conditions = []
        
        for name in key_words:
            filter_conditions.append(func.lower(Activity.name).like(name))
            filter_conditions.append(func.lower(StaffDivision.name).like(name))
            filter_conditions.append(func.lower(Activity.nameKZ).like(name))
            filter_conditions.append(func.lower(StaffDivision.nameKZ).like(name))
        
        schedules = (
            query
            .join(self.model.activity)
            .join(self.model.staff_divisions)
            .filter(or_(*filter_conditions))
        )
        return schedules

    def get_by_id(self, db: Session, id: str):
        schedule_year = self.get(db, id)
        if schedule_year is None:
            raise NotFoundException(
                detail=f"{self.model.__name__} with id {id} not found!")

        for group in schedule_year.staff_divisions:
            if isinstance(group.description, str):
                group.description = json.loads(group.description)

        return schedule_year


schedule_year_service = ScheduleYearService(ScheduleYear)
