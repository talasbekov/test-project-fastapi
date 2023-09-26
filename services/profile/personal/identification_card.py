from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import IdentificationCard, PersonalProfile, Profile
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
    
    def get_by_user_id(self, db: Session, user_id: str):
        identification_card = (db.query(IdentificationCard)
                                .join(PersonalProfile)
                                .join(Profile)
                                .filter(Profile.user_id == user_id)
                                .first())
        if identification_card is None:
            raise NotFoundException(
                detail=f"IdentificationCard with user id: {id} is not found!")
        return identification_card


identification_card_service = IdentificationCardService(IdentificationCard)
