from sqlalchemy.orm import Session

from models import Survey, SurveyStatusEnum
from schemas import SurveyCreate, SurveyUpdate
from services.base import ServiceBase


class SurveyService(ServiceBase[Survey, SurveyCreate, SurveyUpdate]):

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

        db.add(survey)
        db.flush()

        return survey
    
    # def __set_jurisdiction(self, db: Session, jurisdiction_id: str):
    #     jurisdiction = jurisdiction_service.get_by_id(db, jurisdiction_id)
        
        
    
survey_service = SurveyService(Survey)
