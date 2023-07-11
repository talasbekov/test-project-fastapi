from sqlalchemy.orm import Session
from typing import List

from models import (Answer, QuestionTypeEnum,
                    AnswerSingleSelection, AnswerScale, AnswerGrid,
                    AnswerCheckboxGrid, QuestionBase, Survey,
                    AnswerText, QuestionSurvey, QuestionQuiz)
from schemas import AnswerCreate, AnswerUpdate
from exceptions import BadRequestException
from services.base import ServiceBase
from .question import question_service
from .option import option_service
from .survey import survey_service
from .quiz import quiz_service


class AnswerService(ServiceBase[Answer, AnswerCreate, AnswerUpdate]):

    POSSIBLE_TYPES = {
        QuestionTypeEnum.TEXT.value: AnswerText,
        QuestionTypeEnum.MULTIPLE_SELECTION.value: Answer,
        QuestionTypeEnum.SINGLE_SELECTION.value: AnswerSingleSelection,
        QuestionTypeEnum.SCALE.value: AnswerScale,
        QuestionTypeEnum.GRID.value: AnswerGrid,
        QuestionTypeEnum.CHECKBOX_GRID.value: AnswerCheckboxGrid
    }
    
    def get_by_survey_id(self, db: Session, survey_id: str) -> List[Answer]:
        survey = survey_service.get_by_id(db, survey_id)
        
        survey_questions_ids = (
            question_id for (question_id,) in db.query(QuestionSurvey.id).filter(
                QuestionSurvey.survey_id == survey.id).all()
        )
        
        return db.query(self.model).filter(
            self.model.question_id.in_(survey_questions_ids)
        ).all()
        
    def get_by_quiz_id(self, db: Session, quiz_id: str) -> List[Answer]:
        quiz = quiz_service.get_by_id(db, quiz_id)
        
        quiz_questions_ids = (
            question_id for (question_id,) in db.query(QuestionQuiz.id).filter(
                QuestionQuiz.quiz_id == quiz.id).all()
        )
        
        return db.query(self.model).filter(
            self.model.question_id.in_(quiz_questions_ids)
        ).all()

    def create(self, db: Session, body: AnswerCreate, user_id: str) -> Answer:
        question = question_service.get_by_id(db, body.question_id)
        question_class = question_service.define_class(question)

        if question.question_type not in self.POSSIBLE_TYPES:
            raise BadRequestException(
                f"Invalid option type {question.question_type}")

        answer_class = self.POSSIBLE_TYPES[question.question_type]
        answer_kwargs = self.__update_kwargs(question, body)

        answer = answer_class(**answer_kwargs)

        if question.question_type == QuestionTypeEnum.MULTIPLE_SELECTION:
            options = [option_service.get_by_id(
                db, option_id) for option_id in body.option_ids]
            answer.options = options

        if question_class == QuestionSurvey:
            answer = self.__validate_anonymous(
                db, question.survey_id, user_id, answer)
        else:
            answer.score = self.__calculate_score(db, answer)

        db.add(answer)
        db.flush()

        return answer

    def __update_kwargs(self, question: QuestionBase, body: AnswerCreate):
        answer_kwargs = {"question_id": body.question_id}

        if question.question_type == QuestionTypeEnum.SINGLE_SELECTION:
            answer_kwargs.update(
                {"discriminator": "answer_single_choice",
                    "option_id": body.option_id}
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
                {"discriminator": "answer_checkbox_grid",
                    "checkbox_grid_values": body.checkbox_grid_values}
            )
        elif question.question_type == QuestionTypeEnum.TEXT:
            answer_kwargs.update({"text": body.text})

        return answer_kwargs

    def __validate_anonymous(self, db: Session, survey_id: str, user_id: str, answer):
        survey: Survey = survey_service.get_by_id(db, survey_id)

        if not survey.is_anonymous:
            answer.user_id = user_id

        return answer

    def __calculate_score(self, db: Session, answer):
        question = question_service.get_by_id(db, answer.question_id)

        if question.question_type == QuestionTypeEnum.SINGLE_SELECTION.value:
            option = option_service.get_by_id(db, answer.option_id)

            return option.score
        elif question.question_type == QuestionTypeEnum.MULTIPLE_SELECTION.value:
            options = [option_service.get_by_id(db, option_id)
                       for option_id in answer.options]

            return sum([option.score for option in options])


answer_service = AnswerService(Answer)
