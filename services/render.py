import tempfile
import urllib.parse
import urllib.request
import datetime

from docxtpl import DocxTemplate
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from services import (hr_document_template_service, candidate_service, staff_unit_service,
                      profile_service, family_profile_service, family_relation_service,
                      family_service)
from models import (User, Profile, CandidateStageInfo, CandidateStageAnswer,
                    CandidateStageAnswerDefault, CandidateStageAnswerText, CandidateStageType,
                    CandidateStageQuestion)
from exceptions import NotFoundException


class RenderService:
    
    def generate(self, db: Session, candidate_id: str, template_id: str):
        candidate = candidate_service.get_by_id(db, candidate_id)

        candidate_staff_unit = staff_unit_service.get_by_id(db, candidate['staff_unit_id'])

        candidate_user: User = candidate_staff_unit.users[0]

        curator_staff_unit = staff_unit_service.get_by_id(db, candidate['staff_unit_curator_id'])

        curator_user: User = curator_staff_unit.users[0]

        profile: Profile = profile_service.get_by_user_id(db, candidate_user.id)

        family_profile = family_profile_service.get_by_profile_id(db, profile.id)

        father_relation = family_relation_service.get_by_name(db, "Отец")
        mother_relation = family_relation_service.get_by_name(db, "Мать")

        father = family_service.get_by_relation_id(db, father_relation.id)
        mother = family_service.get_by_relation_id(db, mother_relation.id)

        document_template = hr_document_template_service.get_by_id(
            db, template_id
        )

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            arr = document_template.path.rsplit(".")
            extension = arr[len(arr) - 1]
            temp_file_path = temp.name + "." + extension

            try:
                urllib.request.urlretrieve(document_template.path, temp_file_path)
            except Exception:
                raise NotFoundException(detail="Файл не найден!")

        template = DocxTemplate(temp_file_path)

        now = datetime.datetime.now()

        month_num = now.month

        month_names = [
            'Қаңтар', 'Ақпан', 'Наурыз', 'Сәуір', 'Мамыр', 'Маусым', 'Шілде', 'Тамыз', 'Қыркүйек', 'Қазан', 'Қараша', 'Желтоқсан'
        ]

        month_name = month_names[month_num - 1]

        context = {
            'candidate': candidate_user,
            'curator': curator_user,
            'year': now.year,
            'month': month_name,
            'day': now.day,
            'father': father,
            'mother': mother
        }

        template.render(context)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_name = temp_file.name + extension

            template.save(file_name)

        return FileResponse(
            path=file_name,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=document_template.name + "." + extension,
        )
    
    def generate_finish_candidate(self, db: Session, candidate_id: str, template_id: str):
        candidate = candidate_service.get_by_id(db, candidate_id)

        candidate_staff_unit = staff_unit_service.get_by_id(db, candidate['staff_unit_id'])

        candidate_user: User = candidate_staff_unit.users[0]

        curator_staff_unit = staff_unit_service.get_by_id(db, candidate['staff_unit_curator_id'])

        curator_user: User = curator_staff_unit.users[0]

        profile: Profile = profile_service.get_by_user_id(db, candidate_user.id)

        father_relation = family_relation_service.get_by_name(db, "Отец")
        mother_relation = family_relation_service.get_by_name(db, "Мать")

        father = family_service.get_by_relation_id(db, father_relation.id)
        mother = family_service.get_by_relation_id(db, mother_relation.id)

        document_template = hr_document_template_service.get_by_id(
            db, template_id
        )

        first_stage_type = db.query(CandidateStageType).filter(CandidateStageType.name == 'Первичная беседа').first()

        autobigoraphy_question = db.query(CandidateStageQuestion).filter(
            CandidateStageQuestion.question == "Краткие сведения из автобиографии"
        ).first()

        autobiography_answer = db.query(CandidateStageAnswerDefault).filter(
            CandidateStageAnswerDefault.candidate_id == candidate_id, 
            CandidateStageAnswerDefault.candidate_stage_question_id == autobigoraphy_question.id   
        ).first()

        reccommend_question = db.query(CandidateStageQuestion).filter(
            CandidateStageQuestion.question == "Кем подобран и кем рекомендован"
        ).first()

        recommend_answer = db.query(CandidateStageAnswerDefault).filter(
            CandidateStageAnswerDefault.candidate_id == candidate_id, 
            CandidateStageAnswerDefault.candidate_stage_question_id == reccommend_question.id   
        ).first()

        essay_stage_type = db.query(CandidateStageType).filter(CandidateStageType.name == 'Рецензия на эссе').first()

        essay_stage_question = db.query(CandidateStageQuestion).filter(
            CandidateStageQuestion.candidate_stage_type_id == essay_stage_type.id
        ).first()

        essay_answer = db.query(CandidateStageAnswerText).filter(
            CandidateStageAnswerText.candidate_id == candidate_id, 
            CandidateStageAnswerText.candidate_stage_question_id == essay_stage_question.id   
        ).first()
        
        print(1)

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            arr = document_template.path.rsplit(".")
            extension = arr[len(arr) - 1]
            temp_file_path = temp.name + "." + extension
            try:
                urllib.request.urlretrieve(document_template.path, temp_file_path)
            except Exception:
                raise NotFoundException(detail="Файл не найден!")

        template = DocxTemplate(temp_file_path)

        if autobiography_answer is not None:
            autobiography_text = autobiography_answer.answer_str
        else:
            autobiography_text = ""

        if essay_answer is not None:
            essay_answer_text = essay_answer.answer
        else:
            essay_answer_text = ""

        if recommend_answer is not None:
            recommend_answer_text = recommend_answer.answer_str
        else:
            recommend_answer_text = ""

        context = {
            'candidate': candidate_user,
            'candidate_sgo': candidate,
            'curator': curator_user,
            'father': father,
            'mother': mother,
            'autobiography': autobiography_text,
            'recommend': recommend_answer_text,
            'essay': essay_answer_text
        }

        template.render(context)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_name = temp_file.name + extension

            template.save(file_name)

        return FileResponse(
            path=file_name,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=document_template.name + extension,
        )


render_service = RenderService()
