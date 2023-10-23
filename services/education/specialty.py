from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from exceptions import NotFoundException
from models.education import Specialty
from schemas.education import SpecialtyCreate, SpecialtyUpdate
from services import ServiceBase


class SpecialtyService(
        ServiceBase[Specialty, SpecialtyCreate, SpecialtyUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Specialty]:
        return (db.query(Specialty)
                  .order_by(func.to_char(Specialty.name))
                  .offset(skip)
                  .limit(limit)
                  .all())

    def get_by_id(self, db: Session, id: str):
        specialty = super().get(db, id)
        if specialty is None:
            raise NotFoundException(
                detail=f"Specialty with id: {id} is not found!")
        return specialty


specialty_service = SpecialtyService(Specialty)
