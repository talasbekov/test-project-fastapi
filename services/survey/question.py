from models import Question
from schemas import (QuestionCreate, QuestionUpdate)
from services.base import ServiceBase


class QuestionService(ServiceBase[Question, QuestionCreate, QuestionUpdate]):

    def get_by_survey(self, db, survey_id):
        return db.query(self.model).filter(
            self.model.survey_id == survey_id
        ).all()


question_service = QuestionService(Question)
