import datetime
import uuid

from sqlalchemy.orm import Session
from models import BspPlan, PlanStatus
from schemas import BspPlanCreate, BspPlanUpdate
from services.base import ServiceBase

from .schedule_year import schedule_year_service

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

        return plan

    def sign(self, db: Session, id: uuid.UUID):
        plan = self.get_by_id(db, id)
        plan.status = PlanStatus.ACTIVE
        plan.signed_at = datetime.datetime.now()

        db.add(plan)
        db.flush()

        return plan
    
    def send_to_draft(self, db: Session, id: uuid.UUID):
        plan = self.get_by_id(db, id)
        plan.status = PlanStatus.DRAFT

        db.add(plan)
        db.flush()

        return plan
    
    def get_all_draft(self, db: Session, skip: int, limit:int):
        draft_plans = (db.query(BspPlan)
                       .filter(BspPlan.status == PlanStatus.DRAFT)
                       .offset(skip)
                       .limit(limit)
                       .all())
        total = db.query(self.model).filter(BspPlan.status == PlanStatus.DRAFT).count()
        return {'total': total, 'objects': draft_plans}

    def get_all_signed(self, db: Session, skip: int, limit:int):
        signed_plans = (db.query(BspPlan)
                       .filter(BspPlan.status == PlanStatus.ACTIVE)
                       .offset(skip)
                       .limit(limit)
                       .all())
        total = db.query(self.model).filter(BspPlan.status == PlanStatus.ACTIVE).count()
        return {'total': total, 'objects': signed_plans}
    
    def send_to_draft_full(self, db: Session, plan_id: uuid.UUID):
        plan = self.get_by_id(db, plan_id)

        plan.status = PlanStatus.DRAFT

        schedule_year_service.send_all_to_draft_by_plan(db, plan.id)

        return plan

plan_service = BspPlanService(BspPlan)
