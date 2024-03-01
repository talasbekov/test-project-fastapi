import datetime
import pytz

from b64uuid import B64UUID
from sqlalchemy.orm import Session
from sqlalchemy import func

from services.base import ServiceBase
from models import (StaffUnit, SurveyStatusEnum, SurveyJurisdictionTypeEnum,
                    SurveyStaffPositionEnum, PositionNameEnum,
                    Survey, SurveyRepeatTypeEnum, Answer,
                    Question, Option, SurveyJurisdiction,
                    QuestionTypeEnum, SurveyTypeEnum)
from services import (
    staff_division_service, staff_unit_service
)
from .survey_jurisdiction import survey_jurisdiction_service
from schemas import SurveyCreate, SurveyUpdate, SurveyCreateWithJurisdiction
from schemas.survey.survey_jurisdiction import SurveyJurisdictionCreate
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
        staff_unit = staff_unit_service.get_by_id(db, str(role_id))
        user = staff_unit.users[0]
        
        participated_surveys_ids = self.__get_participated_surveys(db, str(user.id))
        certaint_member_query = self.__get_by_certaint_member(db, str(user.id))
        staff_division_query = self.__get_by_staff_division(db, staff_unit)
        
        return (
            certaint_member_query.union_all(staff_division_query)
            .filter(
                func.to_char(self.model.status) == SurveyStatusEnum.ACTIVE.name,
                self.model.start_date <= func.current_date(),
                self.model.end_date >= func.current_date(),
                self.model.id.notin_(participated_surveys_ids)
            )
            .offset(skip).limit(limit).all()
        )

    def get_all_by_status(self,
                          db: Session,
                          status: SurveyStatusEnum,
                          skip: int = 0,
                          limit: int = 100):
        return db.query(self.model).filter(
            func.to_char(self.model.status) == status.name
        ).offset(skip).limit(limit).all()
    
    def get_count(self, db: Session, status: SurveyStatusEnum) -> int:
        return db.query(func.count(self.model.id)).filter(
            func.to_char(self.model.status) == status.name
        ).scalar()
    
    def get_expired_by_repeat_type(self, db: Session, repeat_type: str):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.ACTIVE.value,
            self.model.repeat_type == repeat_type,
            self.model.end_date < datetime.datetime.now()
        ).all()
    
    def get_expired(self, db: Session):
        return db.query(self.model).filter(
            self.model.status == SurveyStatusEnum.ACTIVE.value,
            self.model.end_date < datetime.datetime.now()
        ).all()

    def save_as_draft(self, db: Session, body: SurveyCreateWithJurisdiction):
        survey = self.model(**body.dict())
        
        survey.status = SurveyStatusEnum.DRAFT.value
        
        db.add(survey)
        db.flush()
        
        return survey
    
    def create(self, db: Session, body: SurveyCreateWithJurisdiction):
        survey = self.model(**body.dict())
        db.add(survey)
        db.flush()
        
        for jurisdiction in body.jurisdictions:
            survey_jurisdiction_service.create(db,
                                               SurveyJurisdictionCreate(
                                                   survey_id=str(survey.id),
                                                   jurisdiction_type=jurisdiction.jurisdiction_type,
                                                   staff_position=jurisdiction.staff_position,
                                                   staff_division_id=str(jurisdiction.staff_division_id),
                                                   certain_member_id=jurisdiction.certain_member_id
                                               ))
        
        return survey
    
    def duplicate(self, db: Session, id: str) -> Survey:
        survey_from_db = self.get_by_id(db, str(id))
        
        new_survey = survey_from_db.clone()
        
        new_questions = []
        new_options = []
        for question in survey_from_db.questions:
            
            new_question = question.clone(survey_id=new_survey.id)
            
            for option in question.options:
                new_option = option.clone(question_id=new_question.id)
                
                new_options.append(new_option)
            
            new_questions.append(new_question)
        
        new_jurisdictions = []
        for jurisdiction in survey_from_db.jurisdictions:
            new_jurisdiction = jurisdiction.clone(survey_id=new_survey.id)
            
            new_jurisdictions.append(new_jurisdiction)
        
        db.add(new_survey)
        db.add_all(new_questions)
        db.add_all(new_options)
        db.add_all(new_jurisdictions)
        
        db.flush()

        return new_survey
    
    def repeat(self, db: Session, id: str) -> Survey:
        survey_from_db = self.get_by_id(db, str(id))
        
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
        
        if survey.end_date > datetime.datetime.now():
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
    
    def __get_by_certaint_member(self,
                                 db: Session,
                                 user_id: str):
        query = (
            db.query(self.model)
                .join(SurveyJurisdiction, SurveyJurisdiction.survey_id == self.model.id)
                .filter(
                    func.to_char(self.model.type) != SurveyTypeEnum.COMPETENCE_FORM.name,
                    func.to_char(SurveyJurisdiction.jurisdiction_type) == 
                        SurveyJurisdictionTypeEnum.CERTAIN_MEMBER.name,
                    SurveyJurisdiction.certain_member_id == user_id
                )
        )
        
        return query
        
    def __get_by_staff_division(self,
                                db: Session,
                                staff_unit: StaffUnit):
        staff_division_id = staff_unit.staff_division_id
        
        parent_groups = staff_division_service.get_parent_ids(db, staff_division_id)
        query = (
            db.query(self.model)
                .join(SurveyJurisdiction, SurveyJurisdiction.survey_id == self.model.id)
                .filter(
                    func.to_char(self.model.type) != SurveyTypeEnum.COMPETENCE_FORM.name,
                    (func.to_char(SurveyJurisdiction.jurisdiction_type) == 
                        SurveyJurisdictionTypeEnum.STAFF_DIVISION.name),
                    (SurveyJurisdiction.staff_division_id == str(staff_division_id)) |
                    (SurveyJurisdiction.staff_division_id.in_(parent_groups))
                )
        )
        
        query = self.__filter_by_staff_position(staff_unit, query)
        
        return query
    
    def __filter_by_staff_position(self, staff_unit: StaffUnit, query):
        if staff_unit.position.name in self.ALL_MANAGING_STRUCTURE:
            query = (
                query.filter(
                    (func.to_char(SurveyJurisdiction.staff_position) ==
                        SurveyStaffPositionEnum.ONLY_MANAGING_STRUCTURE.name) |
                    (func.to_char(SurveyJurisdiction.staff_position) ==
                        SurveyStaffPositionEnum.EVERYONE.name)
                )
            )
        else:
            query = (
                query.filter(
                    (func.to_char(SurveyJurisdiction.staff_position) ==
                        SurveyStaffPositionEnum.ONLY_PERSONNAL_STURCTURE.name) |
                    (func.to_char(SurveyJurisdiction.staff_position) ==
                        SurveyStaffPositionEnum.EVERYONE.name)
                )
            )
            
        return query
    
    def __get_participated_surveys(self, db: Session, user_id: str):
        encoded_user_id = B64UUID(user_id).string
        
        participated_surveys_ids = [
            i.id for i in (
                db.query(self.model.id)\
                    .join(Question, Survey.id == Question.survey_id)
                    .join(Option, Question.id == Option.question_id)
                    .join(Answer, Option.answers)
                    .filter(
                        func.to_char(self.model.type) != SurveyTypeEnum.COMPETENCE_FORM.name,
                        (Answer.user_id == str(user_id)) |
                        (Answer.encrypted_used_id == str(encoded_user_id))
                    ).all()
            )
        ]
        
        participated_surveys_ids.extend(
            [
                i.id for i in (
                    db.query(self.model.id)
                    .join(Question, Survey.id == Question.survey_id)
                    .join(Answer, Answer.question_id == Question.id)
                    .filter(
                        func.to_char(self.model.type) != SurveyTypeEnum.COMPETENCE_FORM.name,
                        func.to_char(Question.question_type) == QuestionTypeEnum.TEXT.name,
                        (Answer.user_id == str(user_id)) |
                        (Answer.encrypted_used_id == str(encoded_user_id))
                    ).all()
                )
            ]
        )
        
        return participated_surveys_ids

survey_service = SurveyService(Survey)
