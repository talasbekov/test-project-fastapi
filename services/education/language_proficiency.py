from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import LanguageProficiency
from schemas.education import LanguageProficiencyCreate, LanguageProficiencyUpdate
from services import ServiceBase


class LanguageProficiencyService(ServiceBase[LanguageProficiency, LanguageProficiencyCreate, LanguageProficiencyUpdate]):

    def get_by_id(self, db: Session, id: str):
        language_proficiency = super().get(db, id)
        if language_proficiency is None:
            raise NotFoundException(detail=f"LanguageProficiency with id: {id} is not found!")
        return language_proficiency


language_proficiency_service = LanguageProficiencyService(LanguageProficiency)
