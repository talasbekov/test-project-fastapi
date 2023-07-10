from sqlalchemy.orm import Session

from models import (Quiz, SurveyStatusEnum, SurveyJurisdictionTypeEnum,
                    SurveyStaffPosition, StaffUnit)
from schemas import QuizCreate, QuizUpdate
from services.base import ServiceBase
from services import (
    staff_division_service, staff_unit_service, user_service
)


class QuizService(ServiceBase[Quiz, QuizCreate, QuizUpdate]):
    
    def get_by_jurisdiction(self,
                            db: Session,
                            role_id: str,
                            skip: int = 0,
                            limit: int = 100):
        staff_unit = staff_unit_service.get_by_id(db, role_id)
        user = staff_unit.users[0]
        
        query = (
            db.query(self.model).filter(
                (self.model.certain_member_id ==  user.id) |
                (self.model.staff_division_id == staff_unit.staff_division_id),
                self.model.staff_position == SurveyStaffPosition.EVERYONE.value
            )
        )
        
        query = self.__filter_by_staff_position(db, staff_unit, query)
        
        return query.offset(skip).limit(limit).all()

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
    
    def __set_jurisdiction(self, db: Session, quiz: Quiz, body):
        self.__validate_jurisdiciton_type(body.jurisdiction_type)
        
        if body.jurisdiction_type == SurveyJurisdictionTypeEnum.STAFF_DIVISION.value:
            staff_division = (
                staff_division_service.get_by_id(db, body.staff_division_id)
            )
            
            quiz.staff_division_id = staff_division.id
        else:
            user = user_service.get_by_id(db, body.certain_member_id)
            
            quiz.certain_member_id = user.id
        
        return quiz
    
    def __filter_by_staff_position(self, db: Session, staff_unit: StaffUnit, query):
        if staff_unit.position.name in self.ALL_MANAGING_STRUCTURE:
            query = (
                db.query(self.model).filter(
                    self.model.staff_position ==
                        SurveyStaffPosition.ONLY_MANAGING_STRUCTURE.value
                )
            )
        else:
            query = (
                db.query(self.model).filter(
                    self.model.staff_position ==
                        SurveyStaffPosition.ONLY_PERSONNAL_STURCTURE.value
                )
            )
            
        return query

quiz_service = QuizService(Quiz)
