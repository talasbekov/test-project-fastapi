from models import Quiz
from schemas import QuizCreate, QuizUpdate
from services.base import ServiceBase


class QuizService(ServiceBase[Quiz, QuizCreate, QuizUpdate]):
    pass


quiz_service = QuizService(Quiz)
