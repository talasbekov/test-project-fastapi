from sqlalchemy.orm import Session

from services.base import ServiceBase
from models import (StaffUnit, SurveyStatusEnum, SurveyJurisdictionTypeEnum,
                    SurveyStaffPositionEnum, PositionNameEnum,
                    Survey, Question, Option)
from services import (
    staff_division_service, staff_unit_service, user_service
)
from schemas import SurveyCreate, SurveyUpdate
from exceptions import BadRequestException


class SurveyService(ServiceBase[Survey, SurveyCreate, SurveyUpdate]):
    
    ALL_MANAGING_STRUCTURE = {
        PositionNameEnum.HEAD_OF_DEPARTMENT.value,
        PositionNameEnum.MANAGEMENT_HEAD.value,
        PositionNameEnum.HEAD_OF_OTDEL.value
    }
    
    def get_by_jurisdiction(self,
                            db: Session,
                            role_id: str,
                            skip: int = 0,
                            limit: int = 100):
        staff_unit = staff_unit_service.get_by_id(db, role_id)
        user = staff_unit.users[0]
        
        objects = self.__get_by_certaint_member(db, user.id, skip, limit)
        objects.extend(self.__get_by_staff_division(db, staff_unit, skip, limit))
        
        return objects

    def get_all_active(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.ACTIVE.value
        ).offset(skip).limit(limit).all()

    def get_count_actives(self, db: Session) -> int:
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.ACTIVE.value
        ).count()

    def get_all_archives(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.ARCHIVE.value
        ).offset(skip).limit(limit).all()
    
    def get_count_archives(self, db: Session) -> int:
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.ARCHIVE.value
        ).count()

    def get_all_draft(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.DRAFT.value
        ).offset(skip).limit(limit).all()
    
    def get_count_drafts(self, db: Session) -> int:
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.DRAFT.value
        ).count()

    def save_as_draft(self, db: Session, body: SurveyCreate):
        obj = Survey(**body.dict())
        
        obj.status = SurveyStatusEnum.DRAFT.value
        
        self.__set_jurisdiction(db, obj, body)

        db.add(obj)
        db.flush()

        return obj
    
    def create(self, db: Session, body: SurveyCreate):
        obj = Survey(**body.dict())
        
        self.__set_jurisdiction(db, obj, body)

        db.add(obj)
        db.flush()

        return obj
    
    def duplicate(self, db: Session, id: str):
        survey_from_db = self.get_by_id(db, id)
        
        self.__validate_duplicate_status(survey_from_db)
        
        new_survey = self.create(db, SurveyCreate(
            name=survey_from_db.name,
            nameKZ=survey_from_db.nameKZ,
            description=survey_from_db.description,
            start_date=survey_from_db.start_date,
            end_date=survey_from_db.end_date,
            jurisdiction_type=survey_from_db.jurisdiction_type,
            certain_member_id=survey_from_db.certain_member_id,
            staff_division_id=survey_from_db.staff_division_id,
            staff_position=survey_from_db.staff_position,
            is_kz_translate_required=survey_from_db.is_kz_translate_required,
            is_anonymous=survey_from_db.is_anonymous,
            type=survey_from_db.type
        ))
        
        for question in survey_from_db.questions:
            
            new_question = Question(
                text=question.text,
                textKZ=question.textKZ,
                is_required=question.is_required,
                question_type=question.question_type,
                survey_id=new_survey.id,
                diagram_description=question.diagram_description,
                report_description=question.report_description,
            )
            db.add(new_question)
            db.flush()
            
            for option in question.options:
                new_option = Option(
                    text=option.text,
                    textKZ=option.textKZ,
                    question_id=new_question.id,
                    score=option.score,
                )
                
                db.add(new_option)
        
        new_survey.status = survey_from_db.status
        db.add(new_survey)
        
        db.flush()

        return new_survey


    def __validate_jurisdiciton_type(self, jurisdiction_type: str):
        try:
            return SurveyJurisdictionTypeEnum(jurisdiction_type)
        except ValueError:
            raise BadRequestException(f"Invalid jurisdiction type {jurisdiction_type}")
        
    def __validate_staff_position(self, staff_position: str):
        try:
            return SurveyStaffPositionEnum(staff_position)
        except ValueError:
            raise BadRequestException(f"Invalid staff position {staff_position}")
        
    def __validate_status(self, status: str):
        try:
            return SurveyStatusEnum(status)
        except ValueError:
            raise BadRequestException(f"Invalid status: {status}")
    
    def __validate_duplicate_status(self, survey: Survey):
        if survey.status == SurveyStatusEnum.ACTIVE.value:
            raise BadRequestException("Duplicate is not allowed for active survey")
    
    def __set_jurisdiction(self, db: Session, obj: Survey, body):
        self.__validate_jurisdiciton_type(body.jurisdiction_type)
        self.__validate_staff_position(body.staff_position)
        
        if body.jurisdiction_type == SurveyJurisdictionTypeEnum.STAFF_DIVISION.value:
            staff_division = (
                staff_division_service.get_by_id(db, body.staff_division_id)
            )
            
            obj.staff_division_id = staff_division.id
        else:
            user = user_service.get_by_id(db, body.certain_member_id)
            
            obj.certain_member_id = user.id
            
        obj.staff_position = body.staff_position
        
        return obj
    
    def __get_by_certaint_member(self,
                                 db: Session,
                                 user_id: str,
                                 skip: int,
                                 limit: int):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.ACTIVE.value,
            self.model.jurisdiction_type == 
                SurveyJurisdictionTypeEnum.CERTAIN_MEMBER.value,
            self.model.certain_member_id == user_id
        ).offset(skip).limit(limit).all()
        
    def __get_by_staff_division(self,
                                db: Session,
                                staff_unit: StaffUnit,
                                skip: int,
                                limit: int):
        query = (
            db.query(self.model).filter(
                self.model.status == SurveyStatusEnum.ACTIVE.value,
                self.model.jurisdiction_type == 
                    SurveyJurisdictionTypeEnum.STAFF_DIVISION.value,
                self.model.staff_division_id == staff_unit.staff_division_id
            )
        )
        
        query = self.__filter_by_staff_position(staff_unit, query)
        
        return query.offset(skip).limit(limit).all()
    
    def __filter_by_staff_position(self, staff_unit: StaffUnit, query):
        if staff_unit.position.name in self.ALL_MANAGING_STRUCTURE:
            query = (
                query.filter(
                    (self.model.staff_position ==
                        SurveyStaffPositionEnum.ONLY_MANAGING_STRUCTURE.value) |
                    (self.model.staff_position ==
                        SurveyStaffPositionEnum.EVERYONE.value)
                )
            )
        else:
            query = (
                query.filter(
                    (self.model.staff_position ==
                        SurveyStaffPositionEnum.ONLY_PERSONNAL_STURCTURE.value) |
                    (self.model.staff_position ==
                        SurveyStaffPositionEnum.EVERYONE.value)
                )
            )
            
        return query

survey_service = SurveyService(Survey)
