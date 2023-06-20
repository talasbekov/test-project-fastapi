from sqlalchemy.orm import Session

from exceptions import client
from models.medical import Liberation
from schemas.medical import LiberationCreate, LiberationUpdate
from services import ServiceBase


class LiberationService(
        ServiceBase[Liberation, LiberationUpdate, LiberationCreate]):
    def get_by_id(self, db: Session, id: str):
        liberation = super().get(db, id)
        if liberation is None:
            raise client.NotFoundException(detail="Liberation is not found!")
        return liberation


liberation_service = LiberationService(Liberation)
