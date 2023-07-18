from sqlalchemy.orm import Session

from exceptions import BadRequestException
from models import Question, QuestionTypeEnum, SurveyBase
from schemas import (QuestionCreate, QuestionUpdate)
from services.base import ServiceBase
from .survey import survey_service

class QuestionService(ServiceBase[Question, QuestionCreate, QuestionUpdate]):
    
    def get_count(self, db: Session) -> int:
        return db.query(self.model).count()

    def get_by_survey(self, db: Session, survey_id: str):
        survey = survey_service.get_by_id(db, survey_id)
        
        return db.query(self.model).filter(
            self.model.survey_id == survey.id
        ).all()

    def create(self,
               db: Session,
               body: QuestionCreate):
        self.__validate_question_type(body.question_type)
        
        survey = survey_service.get_by_id(db, body.survey_id)
        self.__validate_kz_required(survey, body.textKZ)
        
        return super().create(db, body)

    def __validate_kz_required(self, survey: SurveyBase, textKZ: str):
        if survey.is_kz_translate_required and not textKZ:
            raise BadRequestException("KZ translation is required")

    def __validate_question_type(self, question_type: str):
        try:
            return QuestionTypeEnum(question_type)
        except ValueError:
            raise BadRequestException(f"Invalid question type {question_type}")

question_service = QuestionService(Question)
