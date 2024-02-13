from typing import List
from sqlalchemy.orm import Session

from services.base import ServiceBase
from models import (Option, QuestionTypeEnum, SurveyTypeEnum, Question)
from schemas import (OptionCreate, OptionUpdate)
from exceptions import BadRequestException
from .survey import survey_service


class OptionService(ServiceBase[Option, OptionCreate, OptionUpdate]):
    
    def get_count(self, db: Session) -> int:
        return db.query(self.model).count()

    def get_by_question(self, db: Session, question_id: str) -> List[Option]:
        return db.query(self.model).filter(
            self.model.question_id == question_id
        ).all()

    def create(self, db: Session, body: OptionCreate) -> Option:
        question = db.query(Question).filter(
            Question.id == str(body.question_id)
        ).first()
        
        survey = survey_service.get_by_id(db, str(question.survey_id))
        
        self.__validate_question_type(question.question_type)
        self.__validate_score(survey, body.score)
        self.__validate_kz_required(db, question.survey_id, body.textKZ)

        return super().create(db, body)
    
    def create_list(self, db: Session, body: List[OptionCreate]):
        res = []
        for option in body:
            res.append(self.create(db, option))
        
        return res
    
    def update(self, db: Session, obj_from_db: Option, body: OptionUpdate):
        question = db.query(Question).filter(
            Question.id == body.question_id
        ).first()
        
        survey = survey_service.get_by_id(db, str(question.survey_id))
        
        self.__validate_question_type(question.question_type)
        self.__validate_score(survey, body.score)
        self.__validate_kz_required(db, question.survey_id, body.textKZ)

        return super().update(db, obj_from_db, body)

    def __validate_score(self, survey, score: int):        
        if survey.type == SurveyTypeEnum.SURVEY.value and score is not None:
            raise BadRequestException(
                "Score is not allowed for survey")
        elif survey.type == SurveyTypeEnum.QUIZ.value and score is None:
            raise BadRequestException(
                "Score is required for quiz"
            )
    
    def __validate_question_type(self, question_type: str):
        if question_type == QuestionTypeEnum.TEXT.value:
            raise BadRequestException(
                "Text question does not allow options")

    def __validate_kz_required(self,
                               db: Session,
                               survey_id: str,
                               textKZ: str):        
        survey = survey_service.get_by_id(db, str(survey_id))

        if survey.is_kz_translate_required and textKZ is None:
            raise BadRequestException("Option KZ translation is required")
            

option_service = OptionService(Option)
