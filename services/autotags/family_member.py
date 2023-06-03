from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from schemas import FamilyRead
from services import family_profile_service


class FamilyMemberAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "family_member"

    def handle(self, db: Session, user_id: UUID):
        profile = family_profile_service.get_by_user_id(db, user_id)
        return [FamilyRead.from_orm(i) for i in profile.family]


handler = FamilyMemberAutoTagHandler()
