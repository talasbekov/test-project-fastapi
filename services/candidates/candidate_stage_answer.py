from typing import List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from models import (
    CandidateStageAnswer, CandidateStageAnswerChoice, 
    CandidateStageAnswerDocument, CandidateStageAnswerText, 
    CandidateEssayAnswer, CandidateStageAnswerDefault, CandidateSportAnswer,
)

from models.user_candidates import CandidateStageQuestionTypeEnum

from schemas import (
    CandidateStageAnswerCreate, CandidateStageAnswerRead, 
    CandidateStageAnswerUpdate, CandidateStageListAnswerCreate
)
from services import ServiceBase

from exceptions import NotFoundException

from fastapi.encoders import jsonable_encoder

 
class CandidateStageAnswerService(ServiceBase[CandidateStageAnswer, CandidateStageAnswerCreate, CandidateStageAnswerUpdate]):

    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):
        candidates = super().get_multi(db, skip, limit)
        candidates = [CandidateStageAnswerRead.from_orm(candidate).dict() for candidate in candidates]
        return candidates

    def create(self, db: Session, body: CandidateStageAnswerCreate) -> CandidateStageAnswerRead:
        body_data = jsonable_encoder(body)
        print(body_data)
        answer_type = body_data.get('type')
        db_obj = self._create_candidate_stage_answer_string(answer_type, body_data)        
        if db_obj is None:
            raise Exception(f"Invalid answer type {answer_type}, here is the body: {body_data}, types: [candidate_stage_answer_string, candidate_stage_answer_choice, candidate_stage_answer_text, candidate_stage_answer_document, candidate_essay_answer]")
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)  
        return {"id": db_obj.id, "type": answer_type}

    def _create_candidate_stage_answer_string(self, answer_type, body_data):
        db_obj = None
        if answer_type == CandidateStageQuestionTypeEnum.STRING_TYPE.value:
            db_obj = CandidateStageAnswerDefault(
                answer_str=body_data['answer_str'],
                candidate_stage_question_id=body_data['candidate_stage_question_id'],
                candidate_id=body_data['candidate_id']
            )
        elif answer_type == CandidateStageQuestionTypeEnum.CHOICE_TYPE.value:
            db_obj = CandidateStageAnswerChoice(
                answer_bool=body_data['answer_bool'],
                candidate_stage_question_id=body_data['candidate_stage_question_id'],
                candidate_id=body_data['candidate_id'],
                document_number=body_data['document_number']
            )
        elif answer_type == CandidateStageQuestionTypeEnum.TEXT_TYPE.value:
            db_obj = CandidateStageAnswerText(
                answer=body_data['answer'],
                candidate_stage_question_id=body_data['candidate_stage_question_id'],
                candidate_id=body_data['candidate_id']
            )
        elif answer_type == CandidateStageQuestionTypeEnum.DOCUMENT_TYPE.value:
            db_obj = CandidateStageAnswerDocument(
                document_link=body_data['document_link'],
                candidate_stage_question_id=body_data['candidate_stage_question_id'],
                candidate_id=body_data['candidate_id']
            )
        elif answer_type == CandidateStageQuestionTypeEnum.ESSAY_TYPE.value:
            db_obj = CandidateEssayAnswer(
                candidate_essay_type_id=body_data['candidate_essay_type_id'],
                candidate_stage_question_id=body_data['candidate_stage_question_id'],
                candidate_id=body_data['candidate_id'],
            )
        elif answer_type == CandidateStageQuestionTypeEnum.SPORT_SCORE_TYPE.value:
            score = body_data['sport_score']
            if score <= 50:
                db_obj = CandidateSportAnswer(
                    is_sport_passed=False,
                    candidate_stage_question_id=body_data['candidate_stage_question_id'],
                    candidate_id=body_data['candidate_id'],
                )
            else:
                db_obj = CandidateSportAnswer(
                    is_sport_passed=True,
                    candidate_stage_question_id=body_data['candidate_stage_question_id'],
                    candidate_id=body_data['candidate_id'],
                )
        return db_obj

    def create_list(self, db: Session, body: List[CandidateStageListAnswerCreate]) -> List[CandidateStageAnswerRead]:
        body_data = jsonable_encoder(body)
        db_obj_list = []
        for item in body_data:
            answer_type = item.get('type')
            db_obj = self._create_candidate_stage_answer_string(answer_type, item)        
            if db_obj is None:
                raise Exception(f"Invalid answer type {answer_type}, here is the body: {body_data}, types: [candidate_stage_answer_string, candidate_stage_answer_choice, candidate_stage_answer_text, candidate_stage_answer_document, candidate_essay_answer]")
            db.add(db_obj)
            db.flush()
            db.refresh(db_obj)  
            db_obj_list.append({"id": db_obj.id, "type": answer_type})
        return db_obj_list

    def update(self, db: Session, id: str, body: CandidateStageAnswerUpdate) -> CandidateStageAnswerRead:
        db_obj = db.query(CandidateStageAnswer).get(id)
        if db_obj is None:
            raise NotFoundException(f"{CandidateStageAnswer.__name__} with id {id} not found!")
        obj_data = jsonable_encoder(db_obj)
        update_data = body.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)

        return CandidateStageAnswerRead.from_orm(db_obj)

    def delete(self, db: Session, id: str) -> CandidateStageAnswerRead:
        db_obj = db.query(CandidateStageAnswer).get(id)
        if db_obj is None:
            raise NotFoundException(f"{CandidateStageAnswer.__name__} with id {id} not found!")
        db.delete(db_obj)
        db.flush()
        return CandidateStageAnswerRead.from_orm(db_obj)

candidate_stage_answer_service = CandidateStageAnswerService(CandidateStageAnswer)
