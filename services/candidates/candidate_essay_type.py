
import logging
import uuid
from models import CandidateEssayType
from schemas import CandidateEssayTypeCreate, CandidateEssayTypeRead, CandidateEssayTypeUpdate
from services import ServiceBase
from sqlalchemy.orm import Session

class CandidateEssayTypeService(ServiceBase[CandidateEssayType, CandidateEssayTypeCreate, CandidateEssayTypeUpdate]):
    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):
        candidates = super().get_multi(db, skip, limit)
        candidates = [CandidateEssayTypeRead.from_orm(candidate).dict() for candidate in candidates]
        return candidates
    

    def create(self, db: Session, body: CandidateEssayTypeCreate):
        candidate = super().create(db, body)
        return CandidateEssayTypeRead.from_orm(candidate).dict()
    
    
    def get_by_id(self, db: Session, id: uuid.UUID):
        candidate = super().get_by_id(db, id)
        return CandidateEssayTypeRead.from_orm(candidate).dict()
    

    def update(self, db: Session, id: uuid.UUID, body: CandidateEssayTypeUpdate):
        candidate = super().update(db, db_obj=super().get_by_id(db, id), obj_in=body)
        return CandidateEssayTypeRead.from_orm(candidate).dict()


    def remove(self, db: Session, id: uuid.UUID):
        super().get_by_id(db, id)
        super().remove(db, id)
        return {"message": f"{self.model.__name__} deleted successfully!"}

candidate_essay_type_service = CandidateEssayTypeService(CandidateEssayType) # type: ignore
