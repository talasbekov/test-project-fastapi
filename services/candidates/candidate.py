import logging
import uuid

from models import Candidate, CandidateStageInfo, CandidateStage, CandidateStageType
from schemas import CandidateCreate, CandidateRead, CandidateUpdate
from services import ServiceBase, staff_unit_service
import json
from typing import Any
from sqlalchemy.orm import Session
from schemas import CandidateRead
from sqlalchemy.sql import func

class CandidateService(ServiceBase[Candidate, CandidateCreate, CandidateUpdate]):
    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):
        candidates = super().get_multi(db, skip, limit)     
        candidates = [CandidateRead.from_orm(candidate).dict() for candidate in candidates]
        for candidate in candidates:
            print(candidate['id'])
            candidate_stage_id = candidate['candidate_stage_id']
            # count number of CandidateStageInfo
            candidate_stage_info_count = db.query(CandidateStageType).count()
            candidate_stage_info_success_count = db.query(
                CandidateStageInfo).filter(
                CandidateStageInfo.candidate_stage_id == candidate_stage_id, 
                CandidateStageInfo.status == 'Одобрен'
            ).count()
            candidate['progress'] = candidate_stage_info_success_count / candidate_stage_info_count * 100
            current_stage_info = db.query(CandidateStageInfo).filter(
                CandidateStageInfo.candidate_stage_id == candidate_stage_id,
                CandidateStageInfo.status == 'В ожидании'
            ).order_by(CandidateStageInfo.created_at.desc()).first()
            if current_stage_info:
                candidate['current_stage'] = current_stage_info.id
            candidate_obj = super().get_by_id(db, candidate['id'])
            if candidate_obj.candidate_stage_answers:
                # get first on date
                candidate['last_edit_date'] = candidate_obj.candidate_stage_answers[0].created_at
        return candidates
    

    def create(self, db: Session, body: CandidateCreate):
        staff_unit_service.get_by_id(db, body.staff_unit_curator_id)
        staff_unit_service.get_by_id(db, body.staff_unit_id)
        candidate = super().create(db, body)
        return CandidateRead.from_orm(candidate).dict()
    
    
    def get_by_id(self, db: Session, id: uuid.UUID):
        candidate = super().get_by_id(db, id)
        return CandidateRead.from_orm(candidate).dict()
    

    def update(self, db: Session, id: uuid.UUID, body: CandidateUpdate):
        staff_unit_service.get_by_id(db, body.staff_unit_curator_id)
        staff_unit_service.get_by_id(db, body.staff_unit_id)
        candidate = super().update(db, db_obj=super().get_by_id(db, id), obj_in=body)
        return CandidateRead.from_orm(candidate).dict()


    def remove(self, db: Session, id: uuid.UUID):
        super().get_by_id(db, id)
        super().remove(db, id)
        return {"message": f"{self.model.__name__} deleted successfully!"}

candidate_service = CandidateService(Candidate) # type: ignore
