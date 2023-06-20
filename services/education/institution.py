from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Institution
from schemas.education import InstitutionCreate, InstitutionUpdate
from services import ServiceBase


class InstitutionService(
        ServiceBase[Institution, InstitutionCreate, InstitutionUpdate]):

    def get_by_id(self, db: Session, id: str):
        institution = super().get(db, id)
        if institution is None:
            raise NotFoundException(
                detail=f"Institution with id: {id} is not found!")
        return institution


institution_service = InstitutionService(Institution)
