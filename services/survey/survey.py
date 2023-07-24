import datetime
import pytz

from sqlalchemy.orm import Session

from services.base import ServiceBase
from models import (StaffUnit, SurveyStatusEnum, SurveyJurisdictionTypeEnum,
                    SurveyStaffPositionEnum, PositionNameEnum,
                    Survey, SurveyRepeatTypeEnum)
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
        
    def get_expired_by_repeat_type(self, db: Session, repeat_type: str):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.ACTIVE.value,
            self.model.repeat_type == repeat_type,
            self.model.end_date < datetime.datetime.now()
        ).all()

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
    
    def duplicate(self, db: Session, id: str) -> Survey:
        survey_from_db = self.get_by_id(db, id)
        
        new_survey = survey_from_db.clone()
        
        new_questions = []
        new_options = []
        for question in survey_from_db.questions:
            
            new_question = question.clone(survey_id=new_survey.id)
            
            for option in question.options:
                new_option = option.clone(question_id=new_question.id)
                
                new_options.append(new_option)
            
            new_questions.append(new_question)
        
        db.add(new_survey)
        db.add_all(new_questions)
        db.add_all(new_options)
        
        db.flush()

        return new_survey
    
    def repeat(self, db: Session, id: str) -> Survey:
        survey_from_db = self.get_by_id(db, id)
        
        self.__check_survey_eligibility_for_repeat(survey_from_db)
        
        new_survey = self.duplicate(db, id)
        
        time_difference = self.__calculate_new_dates_for_repeat(survey_from_db)
        
        new_survey.start_date += time_difference
        new_survey.end_date += time_difference
        
        survey_from_db.status = SurveyStatusEnum.ARCHIVE.value
        
        db.add(survey_from_db)
        db.add(new_survey)
        db.flush()
        
        return new_survey
    
    def __check_survey_eligibility_for_repeat(self, survey: Survey):
        if survey.status != SurveyStatusEnum.ACTIVE.value:
            raise BadRequestException(
                "Repeat is not allowed for survey with status 'Draft' or 'Archive'"
            )
        
        if survey.repeat_type == SurveyRepeatTypeEnum.NEVER.value:
            raise BadRequestException(
                "Repeat is not allowed for survey with repeat type 'Never'"
            )
        
        if survey.end_date > datetime.datetime.now(pytz.UTC):
            raise BadRequestException(
                "Repeat is not allowed for survey with end date less than now"
            )
    
    def __calculate_new_dates_for_repeat(self, survey: Survey):
        repeat_deltas = {
            SurveyRepeatTypeEnum.EVERY_WEEK.value: datetime.timedelta(days=7),
            SurveyRepeatTypeEnum.EVERY_MONTH.value: datetime.timedelta(days=30),
            SurveyRepeatTypeEnum.EVERY_YEAR.value: datetime.timedelta(days=365),
        }

        time_difference = repeat_deltas.get(survey.repeat_type)
        
        return time_difference
    
    def __set_jurisdiction(self, db: Session, obj: Survey, body):
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
        query = (
            db.query(self.model).filter(
                self.model.status == SurveyStatusEnum.ACTIVE.value,
                self.model.jurisdiction_type == 
                    SurveyJurisdictionTypeEnum.CERTAIN_MEMBER.value,
                self.model.certain_member_id == user_id
            )
        )
        
        query = self.__filter_by_date(query)
        
        return query.offset(skip).limit(limit).all()
        
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
        
        query = self.__filter_by_date(query)
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
    
    def __filter_by_date(self, query):
        query = (
            query.filter(
                self.model.start_date <= datetime.datetime.now(),
                self.model.end_date >= datetime.datetime.now()
            )
        )
        
        return query

survey_service = SurveyService(Survey)
