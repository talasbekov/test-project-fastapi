from typing import List
from sqlalchemy.orm import Session

from models import (Option, QuestionTypeEnum, OptionScale,
                    OptionCheckboxGrid, OptionGrid, Question)
from schemas import (OptionCreate, OptionUpdate,
                     OptionRead)
from exceptions import BadRequestException
from services.base import ServiceBase
from .question import question_service


class OptionService(ServiceBase[Option, OptionCreate, OptionUpdate]):
    
    POSSIBLE_TYPES = {
        QuestionTypeEnum.TEXT.value: Option,
        QuestionTypeEnum.SINGLE_CHOICE.value: Option,
        QuestionTypeEnum.MULTIPLE_CHOICE.value: Option,
        QuestionTypeEnum.SCALE.value: OptionScale,
        QuestionTypeEnum.GRID.value: OptionGrid,
        QuestionTypeEnum.CHECKBOX_GRID.value: OptionCheckboxGrid
    }
    
    
    def get_by_question(self, db: Session, question_id: str) -> List[Option]:
        return db.query(self.model).filter(
            self.model.question_id == question_id
        ).all()
    
    
    def create(self, db: Session, body: OptionCreate) -> Option:
        question = question_service.get_by_id(db, body.question_id)
        
        if question.question_type not in self.POSSIBLE_TYPES:
            raise BadRequestException(f"Invalid option type {question.question_type}")
        
        option_class = self.POSSIBLE_TYPES[question.question_type]
        option_kwargs = {"question_id": body.question_id}
        option_kwargs = self.__update_kwargs(question, body, option_kwargs)

        option = option_class(**option_kwargs)
        db.add(option)
        db.flush()

        return option
    
    
    def __update_kwargs(self, question: Question, body: OptionCreate, option_kwargs):
        if question.question_type == QuestionTypeEnum.SCALE:
            option_kwargs.update(
                {"discriminator": "option_scale", "min_value": body.min_value, "max_value": body.max_value}
            )
        elif question.question_type == QuestionTypeEnum.GRID:
            option_kwargs.update(
                {"discriminator": "option_grid", "row_position": body.row_position, "column_position": body.column_position}
            )
        elif question.question_type == QuestionTypeEnum.CHECKBOX_GRID:
            option_kwargs.update(
                {"discriminator": "option_checkbox_grid", "row_position": body.row_position, "column_position": body.column_position, "is_checked": body.is_checked}
            )
        else:
            option_kwargs.update({"text": body.text})
            
        return option_kwargs


option_service = OptionService(Option)