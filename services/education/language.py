from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Language
from schemas.education import LanguageCreate, LanguageUpdate
from services import ServiceBase


class LanguageService(ServiceBase[Language, LanguageCreate, LanguageUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        languages = db.query(Language)

        if filter != '':
            languages = self._add_filter_to_query(languages, filter)

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

    def _add_filter_to_query(self, language_query, filter):
        key_words = filter.lower().split()
        languages = (
            language_query
            .filter(
                and_(func.concat(func.concat(func.lower(Language.name), ' '),
                                 func.concat(func.lower(Language.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return languages

language_service = LanguageService(Language)
