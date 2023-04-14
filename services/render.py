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
from models import User, Profile


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

            urllib.request.urlretrieve(document_template.path, temp_file_path)

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
            filename=document_template.name + extension,
        )


render_service = RenderService()
