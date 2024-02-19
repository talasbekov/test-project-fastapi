from typing import List

from sqlalchemy.orm import Session

from exceptions import BadRequestException
from models import Question, SurveyTypeEnum, Survey
from schemas import (QuestionCreate, QuestionUpdate, OptionCreate,
                     QuestionCreateList)
from services.base import ServiceBase
from .survey import survey_service
from .option import option_service

class QuestionService(ServiceBase[Question, QuestionCreate, QuestionUpdate]):
    
    def get_count(self, db: Session) -> int:
        return db.query(self.model).count()

    def get_by_survey(self, db: Session, survey_id: str):
        survey = survey_service.get_by_id(db, str(survey_id))
        
        return db.query(self.model).filter(
            self.model.survey_id == survey.id
        ).all()

    def create(self,
               db: Session,
               body: QuestionCreate):
        survey = survey_service.get_by_id(db, str(body.survey_id))
        self.__validate_score(survey, body.score)
        self.__validate_kz_required(survey, body.textKZ)
        
        return super().create(db, body)
    
    def create_list(self,
                    db: Session,
                    body: List[QuestionCreateList]):
        
        res = []
        for question in body:
            question_obj = self.create(db, QuestionCreate(
                text=question.text,
                textKZ=question.textKZ,
                is_required=question.is_required,
                question_type=question.question_type,
                survey_id=str(question.survey_id),
                score=question.score
            ))

            if question.options is not None:
                for option in question.options:
                    option_service.create(db, OptionCreate(
                        text=option.text,
                        textKZ=option.textKZ,
                        question_id=str(question_obj.id),
                        score=option.score,
                        diagram_description=option.diagram_description,
                        diagram_descriptionKZ=option.diagram_descriptionKZ,
                        report_description=option.report_description,
                        report_descriptionKZ=option.report_descriptionKZ
                    ))

            
            res.append(question_obj)
            
        return res
    
    def update(self, db: Session, obj_from_db: Question, body: QuestionUpdate):
        survey = survey_service.get_by_id(db, str(body.survey_id))
        self.__validate_score(survey, body.score)
        self.__validate_kz_required(survey, body.textKZ)
        
        return super().update(db, obj_from_db, body)

    def __validate_kz_required(self, survey: Survey, textKZ: str):
        if survey.is_kz_translate_required and not textKZ:
            raise BadRequestException("Question KZ translation is required")
    
    def __validate_score(self, survey: Survey, score: int):
        if survey.type == SurveyTypeEnum.SURVEY.value and score:
            raise BadRequestException(
                "Score is not allowed for survey"
            )
        elif survey.type == SurveyTypeEnum.QUIZ.value and not score:
            raise BadRequestException(
                "Score is required for quiz"
            )

question_service = QuestionService(Question)
