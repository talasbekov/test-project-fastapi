from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import IdentificationCard
from schemas import IdentificationCardCreate, IdentificationCardUpdate
from services.base import ServiceBase


class IdentificationCardService(
        ServiceBase[IdentificationCard,
                    IdentificationCardCreate,
                    IdentificationCardUpdate]):

    def get_by_id(self, db: Session, id: str):
        identification_card = super().get(db, id)
        if identification_card is None:
            raise NotFoundException(
                detail=f"IdentificationCard with id: {id} is not found!")
        return identification_card


identification_card_service = IdentificationCardService(IdentificationCard)
