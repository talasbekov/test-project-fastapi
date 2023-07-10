from sqlalchemy.orm import Session

from models import Survey, SurveyStatusEnum, SurveyJurisdictionTypeEnum
from schemas import SurveyCreate, SurveyUpdate
from services.base import ServiceBase
from services import (
    staff_division_service, staff_unit_service, user_service
)


class SurveyService(ServiceBase[Survey, SurveyCreate, SurveyUpdate]):
    
    def get_by_jurisdiction(self,
                            db: Session,
                            role_id: str,
                            skip: int = 0,
                            limit: int = 100):
        staff_unit = staff_unit_service.get_by_id(db, role_id)
        user = staff_unit.users[0]
        
        return db.query(self.model).filter(
            (self.model.certain_member_id ==  user.id) |
            (self.model.staff_division_id == staff_unit.staff_division_id)
        ).offset(skip).limit(limit).all()

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

    def save_as_draft(self, db: Session, body: SurveyCreate):
        survey = Survey(**body.dict())
        survey.status = SurveyStatusEnum.DRAFT.value
        
        self.__set_jurisdiction(db, survey, body)

        db.add(survey)
        db.flush()

        return survey
    
    def create(self, db: Session, body: SurveyCreate):
        survey = Survey(**body.dict())
        
        self.__set_jurisdiction(db, survey, body)

        db.add(survey)
        db.flush()

        return survey

    def __validate_jurisdiciton_type(self, jurisdiction_type: str):
        try:
            return SurveyJurisdictionTypeEnum(jurisdiction_type)
        except ValueError:
            raise ValueError("Invalid jurisdiction type")
    
    def __set_jurisdiction(self, db: Session, survey: Survey, body):
        self.__validate_jurisdiciton_type(body.jurisdiction_type)
        
        if body.jurisdiction_type == SurveyJurisdictionTypeEnum.STAFF_DIVISION.value:
            staff_division = (
                staff_division_service.get_by_id(db, body.staff_division_id)
            )
            
            survey.staff_division_id = staff_division.id
        else:
            user = user_service.get_by_id(db, body.certain_member_id)
            
            survey.certain_member_id = user.id
        
        return survey
    
survey_service = SurveyService(Survey)
