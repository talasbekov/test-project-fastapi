from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Language
from schemas.education import LanguageCreate, LanguageUpdate
from services import ServiceBase
from services.filter import add_filter_to_query


class LanguageService(ServiceBase[Language, LanguageCreate, LanguageUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        languages = db.query(Language)

        if filter != '':
            languages = add_filter_to_query(languages, filter, Language)

        languages = (languages
                       .order_by(func.to_char(Language.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(Language).count()

        return {'total': total, 'objects': languages}

    def get_by_id(self, db: Session, id: str):
        language = super().get(db, id)
        if language is None:
            raise NotFoundException(
                detail=f"Language with id: {id} is not found!")
        return language


language_service = LanguageService(Language)
