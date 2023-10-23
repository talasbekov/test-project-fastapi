from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Institution
from schemas.education import InstitutionCreate, InstitutionUpdate
from services import ServiceBase


class InstitutionService(
        ServiceBase[Institution, InstitutionCreate, InstitutionUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Institution]:
        return (db.query(Institution)
                  .order_by(func.to_char(Institution.name))
                  .offset(skip)
                  .limit(limit)
                  .all())

    def get_by_id(self, db: Session, id: str):
        institution = super().get(db, id)
        if institution is None:
            raise NotFoundException(
                detail=f"Institution with id: {id} is not found!")
        return institution


institution_service = InstitutionService(Institution)
