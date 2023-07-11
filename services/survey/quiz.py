from models import Quiz
from schemas import QuizCreate, QuizUpdate
from .survey_base import SurveyBaseService


class QuizService(SurveyBaseService[Quiz, QuizCreate, QuizUpdate]):
    pass

quiz_service = QuizService(Quiz)
