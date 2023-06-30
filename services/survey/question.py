from sqlalchemy.orm import Session

from models import (QuestionBase, QuestionQuiz, QuestionSurvey)
from schemas import (QuestionCreate, QuestionUpdate)
from services.base import ServiceBase


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

        question = self.__define_class_and_create(body)

        db.add(question)
        db.flush()

        return question

    def __define_class_and_create(self, body: QuestionCreate):
        if body.survey_id:
            question = QuestionSurvey(
                text=body.text,
                is_required=body.is_required,
                question_type=body.question_type,
                survey_id=body.survey_id
            )
        else:
            question = QuestionQuiz(
                text=body.text,
                is_required=body.is_required,
                question_type=body.question_type,
                quiz_id=body.quiz_id,
                score=body.score
            )

        return question

question_service = QuestionService(QuestionBase)
