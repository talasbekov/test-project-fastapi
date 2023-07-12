from sqlalchemy.orm import Session

from exceptions import BadRequestException
from models import (QuestionBase, QuestionQuiz, QuestionSurvey,
                    QuestionTypeEnum)
from schemas import (QuestionCreate, QuestionUpdate)
from services.base import ServiceBase
from .survey import survey_service
from .quiz import quiz_service


class QuestionService(ServiceBase[QuestionBase, QuestionCreate, QuestionUpdate]):
    
    POSSIBLE_TYPES = {
        "question_survey": QuestionSurvey,
        "question_quiz": QuestionQuiz
    }

    def get_by_survey(self, db: Session, survey_id: str):
        return db.query(QuestionSurvey).filter(
            QuestionSurvey.survey_id == survey_id
        ).all()

    def get_by_quiz(self, db: Session, quiz_id: str):
        return db.query(QuestionQuiz).filter(
            QuestionQuiz.quiz_id == quiz_id
        ).all()

    def define_class(self, question: QuestionBase):
        return self.POSSIBLE_TYPES[question.discriminator]

    def create(self,
               db: Session,
               body: QuestionCreate) -> QuestionBase:
        self.__validate_question_type(body.question_type)
        self.__validate_kz_required(db, body)
        
        if body.survey_id:
            question = QuestionSurvey(
                text=body.text,
                is_required=body.is_required,
                question_type=body.question_type,
                survey_id=body.survey_id,
                diagram_description=body.diagram_description,
                report_description=body.report_description
            )
        else:
            question = QuestionQuiz(
                text=body.text,
                is_required=body.is_required,
                question_type=body.question_type,
                quiz_id=body.quiz_id,
                score=body.score,
                diagram_description=body.diagram_description,
                report_description=body.report_description
            )

        db.add(question)
        db.flush()

        return question

    def get_parent(self, db: Session, question_id: str):
        question = self.get_by_id(db, question_id)
        
        if question.survey_id:
            return survey_service.get_by_id(db, question.survey_id)
        else:
            return quiz_service.get_by_id(db, question.quiz_id)

    def __get_parent_by_body(self, db: Session, body):
        if body.survey_id:
            return survey_service.get_by_id(db, body.survey_id)
        elif body.quiz_id:
            return quiz_service.get_by_id(db, body.quiz_id)

    def __validate_kz_required(self, db: Session, body):
        parent = self.__get_parent_by_body(db, body)
        
        if parent.is_kz_translate_required and not body.textKZ:
            raise BadRequestException("KZ translation is required")

    def __validate_question_type(self, question_type: str):
        try:
            return QuestionTypeEnum(question_type)
        except ValueError:
            raise BadRequestException(f"Invalid question type {question_type}")

question_service = QuestionService(QuestionBase)
