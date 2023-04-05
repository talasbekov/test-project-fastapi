from sqlalchemy.orm import Session

from models import CandidateEssayType
from schemas import CandidateEssayTypeCreate, CandidateEssayTypeRead, CandidateEssayTypeUpdate
from services import ServiceBase


class CandidateEssayTypeService(ServiceBase[CandidateEssayType, CandidateEssayTypeCreate, CandidateEssayTypeUpdate]):
    pass


candidate_essay_type_service = CandidateEssayTypeService(CandidateEssayType) # type: ignore
