from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import List
from b64uuid import B64UUID

from models import (Answer, QuestionTypeEnum, Question,
                    Survey, AnswerText,SurveyTypeEnum, 
                    Option, answers_options, User)
from core.database import engine
from schemas import AnswerCreate, AnswerUpdate
from exceptions import BadRequestException
from services.base import ServiceBase
from services import user_service
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
    
    def analyze_by_staff_division(self, survey_id: str):
        connection = engine.connect()
        
        query = text(
            """
            SELECT hr_erp_questions.id as question_id,
                    to_char(hr_erp_questions.text) as question_text,
                    to_char(hr_erp_questions.textkz) as question_textKZ,
                    hr_erp_options.id as option_id,
                    to_char(hr_erp_options.text) as option_text,
                    to_char(hr_erp_options.textkz) as option_textKZ,
                    count(*) as answer_count,
                    hr_erp_staff_divisions.name as division_name
            FROM hr_erp_questions
            JOIN hr_erp_options ON hr_erp_questions.id = hr_erp_options.question_id 
            JOIN hr_erp_answers_options ON hr_erp_answers_options.option_id = hr_erp_options.id
            JOIN hr_erp_answers ON hr_erp_answers.id = hr_erp_answers_options.answer_id
            JOIN hr_erp_users ON hr_erp_answers.user_id = hr_erp_users.id
            JOIN hr_erp_staff_units ON hr_erp_users.staff_unit_id = hr_erp_staff_units.id
            JOIN hr_erp_staff_divisions ON
                hr_erp_staff_units.staff_division_id = hr_erp_staff_divisions.id
            WHERE hr_erp_answers.question_id IN(
                SELECT id from hr_erp_questions where survey_id = :survey_id
            )
            GROUP BY
             		hr_erp_questions.id, to_char(hr_erp_questions.TEXT), to_char(hr_erp_questions.TEXTKZ),
             		hr_erp_options.id, to_char(hr_erp_options.text), to_char(hr_erp_options.TEXTKZ),
            		hr_erp_staff_divisions.name
            """
        )
        
        results = connection.execute(query, {"survey_id": survey_id})
        
        question_options_map = {}

        for row in results:
            question_id = str(row[0])
            question_text = row[1]
            question_textKZ = row[2]
            option_id = str(row[3])
            option_text = row[4]
            option_textKZ = row[5]
            count = row[6]
            division_name = row[7]

            if question_id not in question_options_map:
                question_options_map[question_id] = {
                    "question_id": question_id,
                    "question_text": question_text,
                    "question_textKZ": question_textKZ,
                    "options": []
                }

            option_found = False
            for option in question_options_map[question_id]["options"]:
                if option["option_id"] == option_id:
                    option_found = True
                    option["answers"].append({"name": division_name, "count": count})
                    break

            if not option_found:
                question_options_map[question_id]["options"].append({
                    "option_id": option_id,
                    "option_text": option_text,
                    "option_textKZ": option_textKZ,
                    "answers": [{"name": division_name, "count": count}]
                })
                
        connection.close()

        # Convert the dictionary to a list of values and return
        return list(question_options_map.values())


    def get_by_survey_id(self,
                         db: Session,
                         survey_id: str,
                         user_id: str) -> List[Answer]:        
        questions = question_service.get_by_survey(db, str(survey_id))
        
        answers = (
            db.query(self.model).filter(
                self.model.question_id.in_(question.id for question in questions)
            )
        )
        
        if not user_id:
            encoded_user_id = B64UUID(user_id).string
            return answers.filter(
                (self.model.user_id == user_id) |
                (self.model.encrypted_used_id == str(encoded_user_id))
            ).all()
        
        return answers.all()
    
    def get_responded_users(self,
                         db: Session,
                         survey_id: str):        
        survey = survey_service.get_by_id(db, str(survey_id))
        
        user_ids = (
            db.query(self.model.user_id)
            .join(answers_options, self.model.id == answers_options.c.answer_id)
            .join(Option, answers_options.c.option_id == Option.id)
            .join(Question, Option.question_id == Question.id)
            .filter(
                Question.survey_id == survey.id
            ).all()
        )
        
        users = {}
        
        for (user_id,) in user_ids:
            if user_id not in users:
                user = user_service.get_by_id(db, str(user_id))
                users[user_id] = {
                    "last_name": user.last_name,
                    "first_name": user.first_name,
                    "father_name": user.father_name
                }

        return users
    
    def analyze_by_question(self, db: Session, survey_id: str):      
        results = (
            db.query(Question.id.label("question_id"),
                     func.to_char(Question.text).label("question_text"),
                     func.to_char(Question.textKZ).label("question_textKZ"),
                     Option.id.label("option_id"),
                     func.to_char(Option.text).label("option_text"),
                     func.to_char(Option.textKZ).label("option_textKZ"),
                     func.count(Answer.id).label("answer_count"),
                     User.first_name, User.last_name, User.id)\
                .join(answers_options, self.model.id == answers_options.c.answer_id)
                .join(Option, answers_options.c.option_id == Option.id)
                .join(Question, Option.question_id == Question.id)
                .join(User, self.model.user_id == User.id)
                .filter(
                    Question.survey_id == survey_id
                )
                .group_by(Question.id, func.to_char(Question.text), func.to_char(Question.textKZ),
                          Option.id, func.to_char(Option.text), func.to_char(Option.textKZ),
                          User.first_name, User.last_name, User.id)
                .all()
        )

        organized_results = {}
        for result in results:
            question_id = result.question_id
            if question_id not in organized_results:
                organized_results[question_id] = {
                    "question_id": result.question_id,
                    "question_text": result.question_text,
                    "question_textKZ": result.question_textKZ,
                    "options": []
                }
            
            option = {
                "option_id": result.option_id,
                "option_text": result.option_text,
                "option_textKZ": result.option_textKZ,
                "answer_count": result.answer_count,
                "responded_users": []
            }

            organized_results[question_id]["options"].append(option)
            
            responded_users = {
                "id": result.id,
                "first_name": result.first_name,
                "last_name": result.last_name
            }
            
            organized_results[question_id]["options"][-1]["responded_users"].append(responded_users)

        return list(organized_results.values())

    def analyze_by_question_with_text_type(self, db: Session, question_id: str):      
        results = (
            db.query(Question.id.label("question_id"),
                     func.to_char(Question.text).label("question_text"),
                     func.to_char(Question.textKZ).label("question_textKZ"),
                     func.count(Answer.id).label("answer_count"),
                     func.to_char(AnswerText.text).label("answer_text"),
                     User.first_name, User.last_name, User.id)\
                .join(Question, Answer.question_id == Question.id)
                .join(User, self.model.user_id == User.id)
                .filter(
                    Question.id == question_id,
                    func.to_char(Question.question_type) == QuestionTypeEnum.TEXT.name
                )
                .group_by(Question.id, func.to_char(Question.text), func.to_char(Question.textKZ),
                          func.to_char(AnswerText.text),
                          User.first_name, User.last_name, User.id)
                .all()
        )

        organized_results = {}
        for result in results:
            question_id = result.question_id
            if question_id not in organized_results:
                organized_results[question_id] = {
                    "question_id": result.question_id,
                    "question_text": result.question_text,
                    "question_textKZ": result.question_textKZ,
                    "answers": []
                }
            
            answer = {
                "answer_text": result.answer_text,
                "answer_count": result.answer_count,
                "responded_users": []
            }

            organized_results[question_id]["answers"].append(answer)
            
            responded_users = {
                "id": result.id,
                "first_name": result.first_name,
                "last_name": result.last_name
            }
            
            organized_results[question_id]["answers"][-1]["responded_users"].append(responded_users)

        return list(organized_results.values())
    
    
    def create(self, db: Session, body: AnswerCreate, user_id: str) -> Answer:
        question = question_service.get_by_id(db, str(body.question_id))
        
        if self.__is_exists(db, user_id, str(body.question_id)):
            raise BadRequestException("Answer already exists")
        
        if question.question_type not in self.POSSIBLE_TYPES:
            raise BadRequestException(
                f"Invalid option type {question.question_type}")

        answer_class = self.POSSIBLE_TYPES[question.question_type]
        answer_kwargs = self.__update_kwargs(db, question, body)

        answer = answer_class(**answer_kwargs)
        
        survey = survey_service.get_by_id(db, str(question.survey_id))
        if survey.type == SurveyTypeEnum.QUIZ.value:
            answer.score = self.__calculate_score(db, answer)
        
        answer = self.__set_anonymous(
            survey, user_id, answer)

        db.add(answer)
        db.flush()

        return answer
    
    def create_list(self,
                    db: Session,
                    body: List[AnswerCreate],
                    user_id: str) -> List[Answer]:
        answers = []
        
        for answer in body:
            answers.append(self.create(db, answer, user_id))
        
        return answers

    def __update_kwargs(self, db: Session, question: Question, body: AnswerCreate):
        answer_kwargs = {"question_id": str(body.question_id)}
        
        if question.question_type == QuestionTypeEnum.SINGLE_SELECTION:
            option = option_service.get_by_id(db, str(body.option_ids[0]))
            
            answer_kwargs.update({"options": [option]})
        elif question.question_type == QuestionTypeEnum.TEXT:
            
            answer_kwargs.update({"text": body.text})
        elif question.question_type == QuestionTypeEnum.MULTIPLE_SELECTION:
            options = [option_service.get_by_id(
                db, str(option_id)) for option_id in body.option_ids]
            answer_kwargs.update({"options": options})

        return answer_kwargs

    def __set_anonymous(self, survey: Survey, user_id: str, answer):
        
        if survey.is_anonymous:
            answer.encrypted_used_id = B64UUID(user_id).string
        else:
            answer.user_id = user_id

        return answer

    def __calculate_score(self, db: Session, answer):
        question = question_service.get_by_id(db, str(answer.question_id))

        if question.question_type == QuestionTypeEnum.SINGLE_SELECTION.value:
            option = option_service.get_by_id(db, str(answer.options[0].id))

            return option.score
        elif question.question_type == QuestionTypeEnum.MULTIPLE_SELECTION.value:

            return sum([option.score for option in answer.options])
    
    def __is_exists(self, db: Session, user_id: str, question_id: str) -> bool:
        encoded_user_id = B64UUID(user_id).string
        
        answer = db.query(self.model).filter(
            self.model.question_id == question_id,
            (self.model.user_id == user_id) |
            (self.model.encrypted_used_id == encoded_user_id)
        ).first()
        
        return answer is not None

answer_service = AnswerService(Answer)
