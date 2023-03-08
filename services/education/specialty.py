from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Specialty
from schemas.education import SpecialtyCreate, SpecialtyRead, SpecialtyUpdate

from services import ServiceBase


class SpecialtyService(ServiceBase[Specialty, SpecialtyCreate, SpecialtyUpdate]):

    def get_by_id(self, db: Session, id: str):
        specialty = super().get(db, id)
        if specialty is None:
            raise NotFoundException(detail=f"Specialty with id: {id} is not found!")
        return specialty


specialty_service = SpecialtyService(Specialty)
