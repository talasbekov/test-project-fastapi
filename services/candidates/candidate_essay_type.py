from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models import CandidateEssayType, Candidate
from schemas import (
    CandidateEssayTypeCreate,
    CandidateEssayTypeRead,
    CandidateEssayTypeUpdate,
    CandidateEssayTypeSetToCandidate)
from services import ServiceBase


class CandidateEssayTypeService(
        ServiceBase[CandidateEssayType,
                    CandidateEssayTypeCreate,
                    CandidateEssayTypeUpdate]):

    def set_to_candidate(self, db: Session, body: CandidateEssayTypeSetToCandidate,
                         candidate_id: str) -> CandidateEssayTypeRead:
        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_id
        ).first()
        
        if body.id is not None and body.name is None:
            essay = self.get_by_id(db, body.id)

            candidate.essay_id = essay.id

            db.add(candidate)
            db.flush()

            return CandidateEssayTypeRead.from_orm(essay)
        if body.id is None and body.name is not None:
            body_data = jsonable_encoder(body)
            essay = self.model(**body_data)

            db.add(essay)
            db.flush()

            candidate.essay_id = essay.id

            db.add(candidate)
            db.flush()

            return CandidateEssayTypeRead.from_orm(essay)

        return None


candidate_essay_type_service = CandidateEssayTypeService(
    CandidateEssayType)  # type: ignore
