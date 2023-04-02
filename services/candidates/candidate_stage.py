import logging
import uuid
from models import CandidateStage
from schemas import CandidateStageCreate, CandidateStageRead, CandidateStageUpdate
from services import ServiceBase
from sqlalchemy.orm import Session

class CandidateStageService(ServiceBase[CandidateStage, CandidateStageCreate, CandidateStageUpdate]):
    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):
        candidates = super().get_multi(db, skip, limit)
        candidates = [CandidateStageRead.from_orm(candidate).dict() for candidate in candidates]
        return candidates
    

    def create(self, db: Session, body: CandidateStageCreate):
        candidate = super().create(db, body)
        return CandidateStageRead.from_orm(candidate).dict()
    
    
    def get_by_id(self, db: Session, id: uuid.UUID):
        candidate = super().get_by_id(db, id)
        return CandidateStageRead.from_orm(candidate).dict()
    

    def update(self, db: Session, id: uuid.UUID, body: CandidateStageUpdate):
        candidate = super().update(db, db_obj=super().get_by_id(db, id), obj_in=body)
        return CandidateStageRead.from_orm(candidate).dict()


    def remove(self, db: Session, id: uuid.UUID):
        super().get_by_id(db, id)
        super().remove(db, id)
        return {"message": f"{self.model.__name__} deleted successfully!"}

candidate_stage_service = CandidateStageService(CandidateStage) # type: ignore
