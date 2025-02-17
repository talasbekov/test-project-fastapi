from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from models import Family
from schemas import AutoTagRead
from services import family_profile_service


class FamilyMemberAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "family_member"

    def handle(self, db: Session, user_id: UUID):
        profile = family_profile_service.get_by_user_id(db, user_id)
        {

        }
        profile.family: list[Family]
        return [
            AutoTagRead(
                name=(f'{i.relation.name} - {i.last_name}'
                      f' {i.first_name  }{"" + i.father_name if i.father_name else None},'
                      f' {i.birthday.strftime("%Y-%m-%d")} г.р.'),
                nameKZ=(f'{i.relation.nameKZ} - {i.last_name}'
                        f' {i.first_name}{" "+ i.father_name},'
                        f' {i.birthday.strftime("%Y-%m-%d")} г.р.'),
            )
            for i in profile.family
        ]


handler = FamilyMemberAutoTagHandler()
