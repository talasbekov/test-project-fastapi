from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from services import personal_profile_service


class RegistrationAddressAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "registration-address-city-name-area-name"

    def handle(self, db: Session, user_id: UUID):
        profile = personal_profile_service.get_by_user_id(db, user_id)
        return profile.biographic_info.address


handler = RegistrationAddressAutoTagHandler()
