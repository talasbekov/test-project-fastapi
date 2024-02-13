import json

from sqlalchemy.orm import Session

from exceptions import BadRequestException
from models import SurveyJurisdiction, SurveyJurisdictionTypeEnum
from schemas import SurveyJurisdictionCreate, SurveyJurisdictionUpdate
from services import ServiceBase, staff_division_service, user_service


class SurveyJurisdictionService(ServiceBase[SurveyJurisdiction,
                                            SurveyJurisdictionCreate,
                                            SurveyJurisdictionUpdate]):
    
    def get_by_survey(self, db: Session, survey_id):
        return db.query(self.model).filter(
            self.model.survey_id == survey_id
        ).all()
    
    def create(self, db: Session, body: SurveyJurisdictionCreate):
        
        jurisdiction_type = body.jurisdiction_type
        
        if jurisdiction_type == SurveyJurisdictionTypeEnum.STAFF_DIVISION.value:
            if not body.staff_division_id and not body.staff_position:
                raise BadRequestException(
                    'Staff division id or staff position is required')
            if body.certain_member_id:
                raise BadRequestException(
                    'Certain member id is not allowed')
            staff_division = staff_division_service.get_by_id(db, str(body.staff_division_id))
            if isinstance(staff_division.description, dict):
                staff_division.description = json.dumps(staff_division.description)
            for staff_unit in staff_division.staff_units:
                if isinstance(staff_unit.requirements, list):
                    staff_unit.requirements = json.dumps(staff_unit.requirements)
            
        elif jurisdiction_type == SurveyJurisdictionTypeEnum.CERTAIN_MEMBER.value:
            if not body.certain_member_id:
                raise BadRequestException(
                    'Certain member id is required')
            if body.staff_division_id and body.staff_position:
                raise BadRequestException(
                    'Staff division id and staff position are not allowed')
            user_service.get_by_id(db, str(body.certain_member_id))
        
        return super().create(db, body)


survey_jurisdiction_service = SurveyJurisdictionService(SurveyJurisdiction)
