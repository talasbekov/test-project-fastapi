from typing import List

from fastapi.encoders import jsonable_encoder
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
from exceptions import NotFoundException
from services import ServiceBase
from exceptions import SgoErpException

class CandidateStageAnswerService(ServiceBase[CandidateStageAnswer, CandidateStageAnswerCreate, CandidateStageAnswerUpdate]):

    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):
        candidates = super().get_multi(db, skip, limit)
        candidates = [CandidateStageAnswerRead.from_orm(candidate).dict() for candidate in candidates]

        return candidates

    def create(self, db: Session, body: CandidateStageAnswerCreate) -> CandidateStageAnswerRead:
        body_data = jsonable_encoder(body)
        answer_type = body_data.get('type')

        db_obj = self._create_candidate_stage_answer_string(answer_type, body_data)        

        if db_obj is None:
            raise Exception(f"Invalid answer type {answer_type}!")

        db.add(db_obj)
        db.flush()

        return CandidateStageAnswerRead.from_orm(db_obj)

    def create_list(self, db: Session, body: List[CandidateStageListAnswerCreate]) -> List[CandidateStageAnswerRead]:
        body_data = jsonable_encoder(body)
        db_obj_list = []
         
        for item in body_data.get('candidate_stage_answers', []):
            answer_type = item.get('type')
            if not item.get('answer_id'):
                
                answer = db.query(CandidateStageAnswer).filter(CandidateStageAnswer.candidate_id == item.get('candidate_id'), CandidateStageAnswer.candidate_stage_question_id == item.get('candidate_stage_question_id')).first()
                if answer:
                    raise SgoErpException(detail=f"Answer with id {answer.id} already exists!", status_code=400)
                print(1)
                db_obj = self._create_candidate_stage_answer_string(answer_type, item)
                print(db_obj)
                if db_obj is None:
                    raise Exception(f"Invalid answer type {answer_type}!")
                db.add(db_obj)
                db.flush() 
                db_obj_list.append(CandidateStageAnswerRead.from_orm(db_obj))
            else: 
                answer_id = item.pop('answer_id')
                item.pop('sport_score')
                print(item)
                chosen_class = self._get_chosen_class(answer_type)

                item_update_obj = db.query(
                    chosen_class
                ).filter(
                    CandidateStageAnswerText.id == answer_id
                ).first()

                print(item_update_obj)
                if item_update_obj is None:
                    raise NotFoundException(f"Answer with id {item.get('answer_id')} not found!")
                 
                if item['type'] == 'Dropdown':
                    item['type'] = 'String'
                print(1) 
                item_update = CandidateStageAnswerUpdate(**item)
                print(item_update)
                db_obj = super().update(db, db_obj=item_update_obj, obj_in=item_update)
                 
                db_obj_list.append(db_obj)
               
        return db_obj_list
    def _get_chosen_class(self, type):
        if type == CandidateStageQuestionTypeEnum.STRING_TYPE.value:
            return CandidateStageAnswerDefault
        elif type == CandidateStageQuestionTypeEnum.CHOICE_TYPE.value:
            return CandidateStageAnswerChoice
        elif type == CandidateStageQuestionTypeEnum.TEXT_TYPE.value:
            return CandidateStageAnswerText
        elif type == CandidateStageQuestionTypeEnum.DOCUMENT_TYPE.value:
            return CandidateStageAnswerDocument
        elif type == CandidateStageQuestionTypeEnum.ESSAY_TYPE.value:
            return CandidateEssayAnswer
        elif type == CandidateStageQuestionTypeEnum.SPORT_SCORE_TYPE.value:
            return CandidateSportAnswer
        elif type == CandidateStageQuestionTypeEnum.DROPDOWN_TYPE.value:
            return CandidateStageAnswerDefault
        else:
            return None
    
    def _create_candidate_stage_answer_string(self, answer_type, body_data):
        db_obj = None
        if answer_type == CandidateStageQuestionTypeEnum.STRING_TYPE.value:
            db_obj = CandidateStageAnswerDefault(
                answer_str=body_data['answer_str'],
                candidate_stage_question_id=body_data['candidate_stage_question_id'],
                candidate_id=body_data['candidate_id']
            )
            print(db_obj)
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
        elif answer_type == CandidateStageQuestionTypeEnum.DROPDOWN_TYPE.value:
            db_obj = CandidateStageAnswerDefault(
                answer_str=body_data['answer_str'],
                candidate_stage_question_id=body_data['candidate_stage_question_id'],
                candidate_id=body_data['candidate_id']
            )
        print('success')
        return db_obj

    
     

candidate_stage_answer_service = CandidateStageAnswerService(CandidateStageAnswer)
