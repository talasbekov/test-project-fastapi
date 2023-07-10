from sqlalchemy.orm import Session

from models import Quiz, SurveyStatusEnum, SurveyJurisdictionTypeEnum
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
        
        self.__set_jurisdiction(db, quiz, body)

        db.add(quiz)
        db.flush()

        return quiz
    
    def create(self, db: Session, body: QuizCreate):
        quiz = Quiz(**body.dict())
        
        self.__set_jurisdiction(db, quiz, body)

        db.add(quiz)
        db.flush()

        return quiz

    def __validate_jurisdiciton_type(self, jurisdiction_type: str):
        try:
            return SurveyJurisdictionTypeEnum(jurisdiction_type)
        except ValueError:
            raise ValueError("Invalid jurisdiction type")
    
    def __set_jurisdiction(self, quiz: Quiz, body):
        self.__validate_jurisdiciton_type(body.jurisdiction_type)
        
        if body.jurisdiction_type == SurveyJurisdictionTypeEnum.STAFF_DIVISION.value:
            quiz.staff_division_id = body.staff_division_id
        else:
            quiz.certain_member_id = body.certain_member_id
        
        return quiz

quiz_service = QuizService(Quiz)
