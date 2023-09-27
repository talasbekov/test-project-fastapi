from models import StatusType
from schemas import StatusTypeCreate, StatusTypeUpdate
from .base import ServiceBase
from typing import List

from sqlalchemy.orm import Session

class StatusTypeService(
        ServiceBase[StatusType, StatusTypeCreate, StatusTypeUpdate]):
    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[StatusType]:
        status_types = db.query(self.model).order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()
        count = db.query(self.model).count()
        return {"total": count, "objects": status_types}


status_type_service = StatusTypeService(StatusType)
