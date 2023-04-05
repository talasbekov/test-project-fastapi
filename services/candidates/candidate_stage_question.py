from models import CandidateStageQuestion
from schemas import CandidateStageQuestionCreate, CandidateStageQuestionUpdate
from services import ServiceBase


class CandidateStageQuestionService(ServiceBase[CandidateStageQuestion, CandidateStageQuestionCreate, CandidateStageQuestionUpdate]):
    pass


candidate_stage_question_service = CandidateStageQuestionService(CandidateStageQuestion) # type: ignore
