from models.user_candidates import CandidateCategory
from schemas.user_candidates import (
    CandidateCategoryCreate, 
    CandidateCategoryUpdate
)
from services import ServiceBase


class CandidateCategoryService(
        ServiceBase[CandidateCategory, 
                    CandidateCategoryCreate, 
                    CandidateCategoryUpdate]):
    pass


candidate_category_service = CandidateCategoryService(CandidateCategory)
