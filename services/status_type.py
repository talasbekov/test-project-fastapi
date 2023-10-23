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
        status_types = (db.query(StatusType)
                        .order_by(StatusType.name)
                        .offset(skip)
                        .limit(limit)
                        .all())
        count = db.query(StatusType).count()

        return {"total": count, "objects": status_types}


status_type_service = StatusTypeService(StatusType)
