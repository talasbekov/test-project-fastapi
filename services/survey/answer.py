from sqlalchemy.orm import Session
from typing import List
from b64uuid import B64UUID

from models import (Answer, QuestionTypeEnum, Question,
                    Survey, AnswerText,
                    SurveyTypeEnum)
from schemas import AnswerCreate, AnswerUpdate
from exceptions import BadRequestException
from services.base import ServiceBase
from .question import question_service
from .option import option_service
from .survey import survey_service


class AnswerService(ServiceBase[Answer, AnswerCreate, AnswerUpdate]):

    POSSIBLE_TYPES = {
        QuestionTypeEnum.TEXT.value: AnswerText,
        QuestionTypeEnum.MULTIPLE_SELECTION.value: Answer,
        QuestionTypeEnum.SINGLE_SELECTION.value: Answer
    }
    
    def get_count(self, db: Session) -> int:
        return db.query(self.model).count()
    
    def get_by_survey_id(self, db: Session, survey_id: str) -> List[Answer]:        
        questions = question_service.get_by_survey(db, survey_id)
        
        question_ids = [question.id for question in questions]

        return db.query(self.model).filter(
            self.model.question_id.in_(question_ids)
        ).all()

    def create(self, db: Session, body: AnswerCreate, user_id: str) -> Answer:
        question = question_service.get_by_id(db, body.question_id)
        
        if self.__is_exists(db, user_id, body.question_id):
            raise BadRequestException("Answer already exists")
        
        if question.question_type not in self.POSSIBLE_TYPES:
            raise BadRequestException(
                f"Invalid option type {question.question_type}")

        answer_class = self.POSSIBLE_TYPES[question.question_type]
        answer_kwargs = self.__update_kwargs(db, question, body)

        answer = answer_class(**answer_kwargs)
        
        survey = survey_service.get_by_id(db, question.survey_id)
        if survey.type == SurveyTypeEnum.QUIZ.value:
            answer.score = self.__calculate_score(db, answer)
        
        answer = self.__set_anonymous(
            survey, user_id, answer)

        db.add(answer)
        db.flush()

        return answer

    def __update_kwargs(self, db: Session, question: Question, body: AnswerCreate):
        answer_kwargs = {"question_id": body.question_id}

        if question.question_type == QuestionTypeEnum.SINGLE_SELECTION:
            option = option_service.get_by_id(db, body.option_ids[0])
            
            answer_kwargs.update({"options": [option]})
        elif question.question_type == QuestionTypeEnum.TEXT:
            
            answer_kwargs.update({"text": body.text})
        elif question.question_type == QuestionTypeEnum.MULTIPLE_SELECTION:
            options = [option_service.get_by_id(
                db, option_id) for option_id in body.option_ids]
            answer_kwargs.update({"options": options})

        return answer_kwargs

    def __set_anonymous(self, survey: Survey, user_id: str, answer):
        
        if survey.is_anonymous:
            answer.encrypted_used_id = B64UUID(user_id).string
        else:
            answer.user_id = user_id

        return answer

    def __calculate_score(self, db: Session, answer):
        question = question_service.get_by_id(db, answer.question_id)

        if question.question_type == QuestionTypeEnum.SINGLE_SELECTION.value:
            option = option_service.get_by_id(db, answer.options[0].id)

            return option.score
        elif question.question_type == QuestionTypeEnum.MULTIPLE_SELECTION.value:
            options = [option_service.get_by_id(db, option_id)
                       for option_id in answer.options]

            return sum([option.score for option in options])
    
    def __is_exists(self, db: Session, user_id: str, question_id: str) -> bool:
        encoded_user_id = B64UUID(user_id).string
        
        answer = db.query(self.model).filter(
            self.model.question_id == question_id,
            (self.model.user_id == user_id) |
            (self.model.encrypted_used_id == encoded_user_id)
        ).first()
        
        return answer is not None

answer_service = AnswerService(Answer)
