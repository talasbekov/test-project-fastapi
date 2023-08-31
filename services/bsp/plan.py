import datetime
import json
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import func

from exceptions import NotFoundException
from models import BspPlan, PlanStatus, ScheduleYear
from schemas import (BspPlanCreate,
                     BspPlanUpdate,
                     ScheduleYearCreateString,
                     ScheduleMonthCreateWithDay,
                     ScheduleDayCreateWithString,
                     ExamScheduleCreate, )
from services.base import ServiceBase

from .schedule_year import schedule_year_service
from .schedule_month import schedule_month_service
from .exam import exam_service


class BspPlanService(ServiceBase[BspPlan, BspPlanCreate, BspPlanUpdate]):

    def create(self, db: Session, plan: BspPlanCreate):
        plan = super().create(db, BspPlanCreate(
            year=plan.year,
            creator_id=plan.creator_id,
            signed_at=None,
        ))
        plan.status = None

        db.add(plan)
        db.flush()

        db.commit()

        if plan.schedule_years != [] or plan.schedule_years is not None:
            for year in plan.schedule_years:
                for group in year.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return plan

    def create_exam_schedules_by_schedule_year(self, db: Session,
                                               schedule_year: ScheduleYear):
        exam_schedules = exam_service.get_by_schedule_year_id(db,
                                                              schedule_year.id)
        for exam_schedule in exam_schedules:
            exam_service.create(db,
                ExamScheduleCreate(
                    start_date=exam_schedule.start_date,
                    end_date=exam_schedule.end_date,
                    start_time=exam_schedule.start_time,
                    end_time=exam_schedule.end_time,
                    place_id=exam_schedule.place_id,
                )
            )


    def create_schedule_months_by_schedule_year(self,
                                                db: Session,
                                                schedule_year: ScheduleYear,
                                                new_schedule_year: ScheduleYear):
        schedule_months = schedule_month_service.get_by_schedule_year_id(db,
                                                                         schedule_year.id)
        for schedule_month in schedule_months:
            days = [ScheduleDayCreateWithString(
                day=schedule_day.day.name,
                start_time=schedule_day.start_time,
                end_time=schedule_day.end_time
            ) for schedule_day in schedule_month.days]

            instructor_ids = [instructor.id for instructor in
                              schedule_month.instructors]

            schedule_month_service.create(db,
                  ScheduleMonthCreateWithDay(
                      start_date=schedule_month.start_date,
                      end_date=schedule_month.end_date,
                      place_id=schedule_month.place_id,
                      schedule_id=new_schedule_year.id,
                      days=days,
                      instructor_ids=instructor_ids
                  )
            )

    def create_schedule_years_by_plan(self,
                                      db: Session,
                                      plan: BspPlan,
                                      new_plan: BspPlan):
        for schedule_year in plan.schedule_years:
            activity_months = [activity.name for activity in
                               schedule_year.activity_months]
            exam_months = [exam.name for exam in schedule_year.exam_months]
            staff_division_ids = [division.id for division in
                                  schedule_year.staff_divisions]
            new_schedule_year = schedule_year_service.create_schedule(db,
                  ScheduleYearCreateString(
                      is_exam_required=schedule_year.is_exam_required,
                      retry_count=schedule_year.retry_count,
                      plan_id=new_plan.id,
                      activity_id=schedule_year.activity_id,
                      activity_months=activity_months,
                      exam_months=exam_months,
                      staff_division_ids=staff_division_ids
                  )
            )

            self.create_schedule_months_by_schedule_year(db,
                                                         schedule_year,
                                                         new_schedule_year)

            self.create_exam_schedules_by_schedule_year(db,
                                                        schedule_year)

    def duplicate(self, db: Session, plan_id: str):
        plan = self.get_by_id(db, str(plan_id))
        new_plan = super().create(db, BspPlanCreate(
            year=plan.year,
            creator_id=plan.creator_id,
            signed_at=None,
        ))
        new_plan.status = plan.status

        self.create_schedule_years_by_plan(db, plan, new_plan)

        db.add(new_plan)
        db.flush()

        db.commit()

        if plan.schedule_years != [] or plan.schedule_years is not None:
            for year in plan.schedule_years:
                for group in year.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return new_plan

    def sign(self, db: Session, id: str):
        plan = self.get_by_id(db, str(id))
        plan.status = PlanStatus.ACTIVE.name
        plan.signed_at = datetime.datetime.now()
        if plan.schedule_years != [] or plan.schedule_years is not None:
            for schedule_year in plan.schedule_years:
                for group in schedule_year.staff_divisions:
                    for staff_unit in group.staff_units:
                        if isinstance(staff_unit.requirements, list):
                            staff_unit.requirements = json.dumps(
                                staff_unit.requirements)
                    if isinstance(group.description, dict):
                        group.description = json.dumps(group.description)

        db.add(plan)
        db.flush()

        db.commit()

        if plan.schedule_years != [] or plan.schedule_years is not None:
            for year in plan.schedule_years:
                for group in year.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return plan

    def send_to_draft(self, db: Session, id: str):
        plan = self.get_by_id(db, str(id))
        plan.status = PlanStatus.DRAFT.name

        db.add(plan)
        db.flush()

        db.commit()

        if plan.schedule_years != [] or plan.schedule_years is not None:
            for year in plan.schedule_years:
                for group in year.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return plan

    def get_all_draft(self, db: Session, skip: int, limit: int):
        draft_plans = (db.query(BspPlan)
                       .filter(func.to_char(BspPlan.status) == PlanStatus.DRAFT.name)
                       .offset(skip)
                       .limit(limit)
                       .all())
        total = db.query(self.model).filter(func.to_char(BspPlan.status) == PlanStatus.DRAFT.name).count()

        for plan in draft_plans:
            if plan.schedule_years != [] or plan.schedule_years is not None:
                for year in plan.schedule_years:
                    for group in year.staff_divisions:
                        if isinstance(group.description, str):
                            group.description = json.loads(group.description)

        return {'total': total, 'objects': draft_plans}

    def get_all_signed(self, db: Session, skip: int, limit: int):
        signed_plans = (db.query(BspPlan)
                        .filter(func.to_char(BspPlan.status) == PlanStatus.ACTIVE.name)
                        .offset(skip)
                        .limit(limit)
                        .all())
        total = db.query(self.model).filter(func.to_char(BspPlan.status) == PlanStatus.ACTIVE.name).count()

        for plan in signed_plans:
            if plan.schedule_years != [] or plan.schedule_years is not None:
                for year in plan.schedule_years:
                    for group in year.staff_divisions:
                        if isinstance(group.description, str):
                            group.description = json.loads(group.description)

        return {'total': total, 'objects': signed_plans}

    def send_to_draft_full(self, db: Session, plan_id: str):
        plan = self.get_by_id(db, str(plan_id))

        plan.status = PlanStatus.DRAFT.name

        for year in plan.schedule_years:
            for group in year.staff_divisions:
                for staff_unit in group.staff_units:
                    if isinstance(staff_unit.requirements, list):
                        staff_unit.requirements = json.dumps(staff_unit.requirements)
                if isinstance(group.description, dict):
                    group.description = json.dumps(group.description)

        schedule_year_service.send_all_to_draft_by_plan(db, plan.id)

        db.add(plan)
        db.flush()

        db.commit()

        if plan.schedule_years != [] or plan.schedule_years is not None:
            for year in plan.schedule_years:
                for group in year.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return plan

    def get_by_id(self, db: Session, id: str):
        res = self.get(db, id)
        if res is None:
            raise NotFoundException(
                detail=f"{self.model.__name__} with id {id} not found!")

        if res.schedule_years != [] or res.schedule_years is not None:
            for year in res.schedule_years:
                for group in year.staff_divisions:
                    if isinstance(group.description, str):
                        group.description = json.loads(group.description)

        return res

    def remove(self, db: Session, id: str):
        obj = self.get_by_id(db, id)

        for schedule_year in obj.schedule_years:

            for group in schedule_year.staff_divisions:
                for staff_unit in group.staff_units:
                    if isinstance(staff_unit.requirements, list):
                        staff_unit.requirements = json.dumps(
                            staff_unit.requirements)
                if isinstance(group.description, dict):
                    group.description = json.dumps(group.description)

            schedule_year_service.remove_schedule_with_staff_divisions(db,
                                                                       schedule_year.id)

        db.delete(obj)
        db.flush()
        for schedule_year in obj.schedule_years:
            for group in schedule_year.staff_divisions:
                if isinstance(group.description, str):
                    group.description = json.loads(group.description)
        return obj




plan_service = BspPlanService(BspPlan)
