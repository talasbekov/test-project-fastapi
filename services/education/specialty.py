from sqlalchemy.orm import Session
from sqlalchemy import func

from exceptions import NotFoundException
from models.education import Specialty
from schemas.education import SpecialtyCreate, SpecialtyUpdate
from services import ServiceBase
from services.filter import add_filter_to_query


class SpecialtyService(
        ServiceBase[Specialty, SpecialtyCreate, SpecialtyUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        specialties = db.query(Specialty)

        if filter != '':
            specialties = add_filter_to_query(specialties, filter, Specialty)

        specialties = (specialties
                       .order_by(func.to_char(Specialty.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(Specialty).count()

        return {'total': total, 'objects': specialties}

    def get_by_id(self, db: Session, id: str):
        specialty = super().get(db, id)
        if specialty is None:
            raise NotFoundException(
                detail=f"Specialty with id: {id} is not found!")
        return specialty


specialty_service = SpecialtyService(Specialty)
