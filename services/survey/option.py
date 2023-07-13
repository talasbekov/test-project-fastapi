from typing import List, Type
from sqlalchemy.orm import Session

from models import (Option, QuestionTypeEnum, QuestionSurvey,
                    OptionText, QuestionBase)
from schemas import (OptionCreate, OptionUpdate)
from exceptions import BadRequestException
from services.base import ServiceBase
from .question import question_service


class OptionService(ServiceBase[Option, OptionCreate, OptionUpdate]):

    POSSIBLE_TYPES = {
        QuestionTypeEnum.SINGLE_SELECTION.value: OptionText,
        QuestionTypeEnum.MULTIPLE_SELECTION.value: OptionText
    }
    
    def get_count(self, db: Session) -> int:
        return db.query(self.model).count()

    def get_by_question(self, db: Session, question_id: str) -> List[Option]:
        return db.query(self.model).filter(
            self.model.question_id == question_id
        ).all()

    def create(self, db: Session, body: OptionCreate) -> Option:
        question = question_service.get_by_id(db, body.question_id)
        self.__validate_kz_required(db, question, body.textKZ)
        self.__validate_score(question, body.score)

        option = OptionText(
            question_id=body.question_id,
            score=body.score,
            text=body.text,
            textKZ=body.textKZ
        )
        
        db.add(option)
        db.flush()

        return option

    def __validate_score(self, question: Type[QuestionBase], score: int):
        if score is not None and question == QuestionSurvey:
            raise BadRequestException(
                "Score is not allowed for survey")

    def __validate_kz_required(self,
                               db: Session,
                               question: Type[QuestionBase],
                               textKZ: str):        
        parent = question_service.get_parent(db, question.id)

        if parent.is_kz_translate_required and not textKZ:
            raise BadRequestException("KZ translation is required")
            

option_service = OptionService(Option)
