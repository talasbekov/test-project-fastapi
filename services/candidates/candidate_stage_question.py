import logging
import uuid
from models import CandidateStageQuestion
from schemas import CandidateStageQuestionCreate, CandidateStageQuestionRead, CandidateStageQuestionUpdate
from services import ServiceBase
from sqlalchemy.orm import Session

class CandidateStageQuestionService(ServiceBase[CandidateStageQuestion, CandidateStageQuestionCreate, CandidateStageQuestionUpdate]):
    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):
        candidates = super().get_multi(db, skip, limit)
        candidates = [CandidateStageQuestionRead.from_orm(candidate).dict() for candidate in candidates]
        return candidates
    

    def create(self, db: Session, body: CandidateStageQuestionCreate):
        candidate = super().create(db, body)
        return CandidateStageQuestionRead.from_orm(candidate).dict()
    
    
    def get_by_id(self, db: Session, id: uuid.UUID):
        candidate = super().get_by_id(db, id)
        return CandidateStageQuestionRead.from_orm(candidate).dict()
    

    def update(self, db: Session, id: uuid.UUID, body: CandidateStageQuestionUpdate):
        candidate = super().update(db, db_obj=super().get_by_id(db, id), obj_in=body)
        return CandidateStageQuestionRead.from_orm(candidate).dict()


    def remove(self, db: Session, id: uuid.UUID):
        super().get_by_id(db, id)
        super().remove(db, id)
        return {"message": f"{self.model.__name__} deleted successfully!"}

candidate_stage_question_service = CandidateStageQuestionService(CandidateStageQuestion) # type: ignore
