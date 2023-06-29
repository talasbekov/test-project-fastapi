from models import Survey
from schemas import SurveyCreate, SurveyUpdate
from services.base import ServiceBase


class SurveyService(ServiceBase[Survey, SurveyCreate, SurveyUpdate]):
    pass


survey_service = SurveyService(Survey)
