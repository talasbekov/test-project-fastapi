import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import StatusType, StatusEnum
from schemas import StatusTypeRead


class StatusLeaveService:
    def get_by_option(self,
                      db: Session,
                      type: str,
                      id: uuid.UUID,
                      skip: int,
                      limit: int):
        res = (
            db.query(StatusType)
            .filter(func.lower(StatusType.name).contains(StatusEnum.ROOT.value))
        )
        return [StatusTypeRead.from_orm(status).dict() for status in res]


status_leave_service = StatusLeaveService()
