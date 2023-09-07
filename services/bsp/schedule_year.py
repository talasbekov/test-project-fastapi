import json
import datetime
import time

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

    def _filter_months(self, month: int, schedules):
        result = []
        for schedule in schedules:
            schedule_dict = ScheduleYearRead.from_orm(schedule).dict()

            activity_months = [item for item in schedule_dict['activity_months'] if
                               item['month_order'] == month]
            if activity_months:
                first_activity_month = activity_months[0]['month_order']
                for month_entry in schedule_dict['months']:
                    if month_entry['start_date'].month == first_activity_month:
                        activity_months[0]['has_schedule_month'] = False
                        break
                else:
                    activity_months[0]['has_schedule_month'] = True

            schedule_dict['activity_months'] = activity_months

            exam_months = [item for item in schedule_dict['exam_months'] if
                           item['month_order'] == month]
            if exam_months:
                first_exam_month = exam_months[0]['month_order']
                for exam_entry in schedule_dict['exams']:
                    if exam_entry['start_date'].month == first_exam_month:
                        exam_months[0]['has_schedule_month'] = False
                        break
                else:
                    exam_months[0]['has_schedule_month'] = True

                schedule_dict['exam_months'] = exam_months

            result.append(schedule_dict)

        return result

    def get_multi(
            self,
            db: Session,
            filter: str = '',
            filter_year: str = '',
            filter_month: str = '',
            skip: int = 0,
            limit: int = 100
    ):
        start_time = time.time()
        if filter_month == '':
            filter_month = str(datetime.date.today().month)
        if filter_year == '':
            filter_year = str(datetime.date.today().year)

        total = (db.query(self.model)
                 .join(BspPlan)
                 .join(ScheduleYear.activity_months)
                 .filter(ScheduleYear.is_active == True,
                         func.concat(BspPlan.year, Month.month_order) ==
                         (filter_year + filter_month))
                 )
        schedules = (db.query(self.model)
                     .join(BspPlan)
                     .join(ScheduleYear.activity_months)
                     .filter(ScheduleYear.is_active == True,
                             func.concat(BspPlan.year, Month.month_order) ==
                             (filter_year + filter_month)
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

        print('before _filter_months time: ', (time.time() - start_time))

        schedules = self._filter_months(int(filter_month), schedules)

        print('total time: ', (time.time() - start_time))
        return {'total': total, 'objects': schedules}

    def remove_schedule(self,
                        db: Session,
                        schedule_id: str):
        schedule_year = self.get_by_id(db, str(schedule_id))

        if schedule_year.months is not None:
            for schedule_month in schedule_year.months:
                schedule_month_service.remove(db, schedule_month.id)

        if schedule_year.exams is not None:
            for exam_month in schedule_year.exams:
                exam_service.remove(db, exam_month.id)
        schedule_year.exam_months.clear()
        schedule_year.activity_months.clear()
        schedule_year.months.clear()
        schedule_year.exams.clear()

        db.add(schedule_year)
        db.flush()
        db.delete(schedule_year)
        db.flush()
        db.commit()

        for group in schedule_year.staff_divisions:
            if isinstance(group.description, str):
                group.description = json.loads(group.description)

        return schedule_year

    def remove_division_from_schedule(self,
                                      db: Session,
                                      schedule_id: str,
                                      division_id: str):
        schedule_year = self.get_by_id(db, str(schedule_id))

        staff_division = staff_division_service.get_by_id(db, str(division_id))

        schedule_year.staff_divisions.remove(staff_division)
        db.flush()
        db.commit()

        for group in schedule_year.staff_divisions:
            if isinstance(group.description, str):
                group.description = json.loads(group.description)

        return schedule_year

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
        if year is not None:
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
