from sqlalchemy.orm import Session

from models import Quiz, SurveyStatusEnum
from schemas import QuizCreate, QuizUpdate
from services.base import ServiceBase


class QuizService(ServiceBase[Quiz, QuizCreate, QuizUpdate]):
    
    def get_all_active(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.ACTIVE.value
        ).offset(skip).limit(limit).all()

    def get_all_not_active(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.NOT_ACTIVE.value
        ).offset(skip).limit(limit).all()

    def get_all_draft(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.DRAFT.value
        ).offset(skip).limit(limit).all()

    def save_as_draft(self, db: Session, body: QuizCreate):
        quiz = Quiz(**body.dict())
        quiz.status = SurveyStatusEnum.DRAFT.value

        db.add(quiz)
        db.flush()

        return quiz

quiz_service = QuizService(Quiz)
