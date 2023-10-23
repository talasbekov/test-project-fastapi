from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Language
from schemas.education import LanguageCreate, LanguageUpdate
from services import ServiceBase


class LanguageService(ServiceBase[Language, LanguageCreate, LanguageUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Language]:
        return (db.query(Language)
                  .order_by(func.to_char(Language.name))
                  .offset(skip)
                  .limit(limit)
                  .all())

    def get_by_id(self, db: Session, id: str):
        language = super().get(db, id)
        if language is None:
            raise NotFoundException(
                detail=f"Language with id: {id} is not found!")
        return language


language_service = LanguageService(Language)
