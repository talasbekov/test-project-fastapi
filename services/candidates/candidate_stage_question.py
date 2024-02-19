from sqlalchemy.orm import Session

from models import CandidateStageQuestion
from schemas import CandidateStageQuestionCreate, CandidateStageQuestionUpdate
from services import ServiceBase


class CandidateStageQuestionService(
        ServiceBase[CandidateStageQuestion,
                    CandidateStageQuestionCreate,
                    CandidateStageQuestionUpdate]):

    def get_multi(
            self, db: Session, skip: int = 0, limit: int = 100
    ):
        return db.query(self.model).order_by(
            self.model.id.asc()).offset(skip).limit(limit).all()


candidate_stage_question_service = CandidateStageQuestionService(
    CandidateStageQuestion)  # type: ignore
