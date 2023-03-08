from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Science
from schemas.education import ScienceCreate, ScienceRead, ScienceUpdate

from services import ServiceBase


class ScienceService(ServiceBase[Science, ScienceCreate, ScienceUpdate]):

    def get_by_id(self, db: Session, id: str):
        science = super().get(db, id)
        if science is None:
            raise NotFoundException(detail=f"Science with id: {id} is not found!")
        return science


science_service = ScienceService(Science)
