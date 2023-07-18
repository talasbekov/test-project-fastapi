from sqlalchemy.orm import Session

from exceptions import BadRequestException
from models import (Quiz, SurveyStatusEnum,
                    QuestionQuiz, Option)
from schemas import (QuizCreate, QuizUpdate)
from .survey_base import SurveyBaseService


class QuizService(SurveyBaseService[Quiz, QuizCreate, QuizUpdate]):
    
    def duplicate(self, db: Session, id: str):
        quiz_from_db = self.get_by_id(db, id)
        
        self.__validate_duplicate_status(quiz_from_db)
        
        new_quiz = self.create(db, QuizCreate(
            name=quiz_from_db.name,
            nameKZ=quiz_from_db.nameKZ,
            description=quiz_from_db.description,
            start_date=quiz_from_db.start_date,
            end_date=quiz_from_db.end_date,
            jurisdiction_type=quiz_from_db.jurisdiction_type,
            certain_member_id=quiz_from_db.certain_member_id,
            staff_division_id=quiz_from_db.staff_division_id,
            staff_position=quiz_from_db.staff_position,
            is_kz_translate_required=quiz_from_db.is_kz_translate_required
        ))
        
        for question in quiz_from_db.questions:
            new_question = QuestionQuiz(
                text=question.text,
                textKZ=question.textKZ,
                is_required=question.is_required,
                question_type=question.question_type,
                quiz_id=new_quiz.id,
                score=question.score,
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
        
        new_quiz.status = quiz_from_db.status
        db.add(new_quiz)
        
        db.flush()

        return new_quiz
    
    def __validate_duplicate_status(self, quiz: Quiz):
        if quiz.status == SurveyStatusEnum.ACTIVE.value:
            raise BadRequestException("Duplicate is not allowed for active quiz")


quiz_service = QuizService(Quiz)
