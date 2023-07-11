from models import Survey
from schemas import SurveyCreate, SurveyUpdate
from .survey_base import SurveyBaseService


class SurveyService(SurveyBaseService[Survey, SurveyCreate, SurveyUpdate]):
    pass

survey_service = SurveyService(Survey)
