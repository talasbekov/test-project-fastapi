from sqlalchemy.orm import Session

from models import CandidateEssayType
from schemas import CandidateEssayTypeCreate, CandidateEssayTypeRead, CandidateEssayTypeUpdate
from services import ServiceBase


class CandidateEssayTypeService(ServiceBase[CandidateEssayType, CandidateEssayTypeCreate, CandidateEssayTypeUpdate]):
    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):
        candidates = super().get_multi(db, skip, limit)
        candidates = [CandidateEssayTypeRead.from_orm(candidate).dict() for candidate in candidates]
        return candidates


candidate_essay_type_service = CandidateEssayTypeService(CandidateEssayType) # type: ignore
