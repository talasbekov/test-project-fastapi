from models import CandidateStageType
from schemas import CandidateStageTypeCreate, CandidateStageTypeUpdate
from services import ServiceBase


class CandidateStageTypeService(ServiceBase[CandidateStageType, CandidateStageTypeCreate, CandidateStageTypeUpdate]):
    pass


candidate_stage_type_service = CandidateStageTypeService(CandidateStageType) # type: ignore
