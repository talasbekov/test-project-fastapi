from sqlalchemy.orm import Session

from exceptions import BadRequestException
from models import (Survey, SurveyStatusEnum, QuestionSurvey,
                    Option)
from schemas import (SurveyCreate, SurveyUpdate)
from .survey_base import SurveyBaseService

class SurveyService(SurveyBaseService[Survey, SurveyCreate, SurveyUpdate]):
    
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
        ))
        
        for question in survey_from_db.questions:
            # new_question = question_service.create(db, QuestionCreate(
                # text=question.text,
                # textKZ=question.textKZ,
                # is_required=question.is_required,
                # question_type=question.question_type,
                # survey_id=new_survey.id,
                # quiz_id=None,
                # score=question.score,
                # diagram_description=question.diagram_description,
                # report_description=question.report_description,
            # ))
            
            new_question = QuestionSurvey(
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
    
    def __validate_duplicate_status(self, survey: Survey):
        if survey.status == SurveyStatusEnum.ACTIVE.value:
            raise BadRequestException("Duplicate is not allowed for active survey")

survey_service = SurveyService(Survey)
