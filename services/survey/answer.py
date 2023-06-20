from sqlalchemy.orm import Session

from models import (Answer, QuestionTypeEnum, Answer,
                    AnswerSingleChoice, AnswerScale, AnswerGrid,
                    AnswerCheckboxGrid, Question)
from schemas import AnswerCreate, AnswerUpdate
from exceptions import BadRequestException
from services.base import ServiceBase
from .question import question_service
from .option import option_service

class AnswerService(ServiceBase[Answer, AnswerCreate, AnswerUpdate]):
    
    POSSIBLE_TYPES = {
        QuestionTypeEnum.TEXT.value: Answer,
        QuestionTypeEnum.MULTIPLE_CHOICE.value: Answer,
        QuestionTypeEnum.SINGLE_CHOICE.value: AnswerSingleChoice,
        QuestionTypeEnum.SCALE.value: AnswerScale,
        QuestionTypeEnum.GRID.value: AnswerGrid,
        QuestionTypeEnum.CHECKBOX_GRID.value: AnswerCheckboxGrid
    }
    
    def create(self, db: Session, body: AnswerCreate) -> Answer:
        question = question_service.get_by_id(db, body.question_id)
        
        if question.question_type not in self.POSSIBLE_TYPES:
            raise BadRequestException(f"Invalid option type {question.question_type}")
        
        answer_class = self.POSSIBLE_TYPES[question.question_type]
        
        answer_kwargs = {"question_id": body.question_id}
        answer_kwargs = self.__update_kwargs(question, body, answer_kwargs)

        answer = answer_class(**answer_kwargs)
        
        if question.question_type == QuestionTypeEnum.MULTIPLE_CHOICE:
            options = [option_service.get_by_id(db, option_id) for option_id in body.option_ids]
            print(f"options: {options}")
            answer.options = options
            
        db.add(answer)
        db.flush()

        return answer
    
    
    def __update_kwargs(self, question: Question, body: AnswerCreate, answer_kwargs):
        if question.question_type == QuestionTypeEnum.SINGLE_CHOICE:
            answer_kwargs.update(
                {"discriminator": "answer_single_choice", "option_id": body.option_id}
            ) 
        if question.question_type == QuestionTypeEnum.SCALE:
            answer_kwargs.update(
                {"discriminator": "answer_scale", "scale_value": body.scale_value}
            )
        elif question.question_type == QuestionTypeEnum.GRID:
            answer_kwargs.update(
                {"discriminator": "answer_grid", "grid_values": body.grid_values}
            )
        elif question.question_type == QuestionTypeEnum.CHECKBOX_GRID:
            answer_kwargs.update(
                {"discriminator": "answer_checkbox_grid", "checkbox_grid_values": body.checkbox_grid_values}
            )
        elif question.question_type == QuestionTypeEnum.TEXT:
            answer_kwargs.update({"text": body.text})
            
        return answer_kwargs


answer_service = AnswerService(Answer)
