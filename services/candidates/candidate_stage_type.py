import logging
import uuid
from models import CandidateStageType
from schemas import CandidateStageTypeCreate, CandidateStageTypeRead, CandidateStageTypeUpdate
from services import ServiceBase
from sqlalchemy.orm import Session

class CandidateStageTypeService(ServiceBase[CandidateStageType, CandidateStageTypeCreate, CandidateStageTypeUpdate]):
    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):
        candidates = super().get_multi(db, skip, limit)
        candidates = [CandidateStageTypeRead.from_orm(candidate).dict() for candidate in candidates]
        return candidates
    

    def create(self, db: Session, body: CandidateStageTypeCreate):
        candidate = super().create(db, body)
        return CandidateStageTypeRead.from_orm(candidate).dict()
    
    
    def get_by_id(self, db: Session, id: uuid.UUID):
        candidate = super().get_by_id(db, id)
        return CandidateStageTypeRead.from_orm(candidate).dict()
    

    def update(self, db: Session, id: uuid.UUID, body: CandidateStageTypeUpdate):
        candidate = super().update(db, db_obj=super().get_by_id(db, id), obj_in=body)
        return CandidateStageTypeRead.from_orm(candidate).dict()


    def remove(self, db: Session, id: uuid.UUID):
        super().get_by_id(db, id)
        super().remove(db, id)
        return {"message": f"{self.model.__name__} deleted successfully!"}

candidate_stage_type_service = CandidateStageTypeService(CandidateStageType) # type: ignore
