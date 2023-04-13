import tempfile
import urllib.parse
import urllib.request

from docxtpl import DocxTemplate
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from services import (hr_document_template_service, candidate_service, staff_unit_service)


class RenderService:
    
    def generate(self, db: Session, candidate_id: str, template_id: str):
        candidate = candidate_service.get_by_id(db, candidate_id)

        candidate_staff_unit = staff_unit_service.get_by_id(db, candidate['staff_unit_id'])

        candidate_user = candidate_staff_unit.users[0]

        curator_staff_unit = staff_unit_service.get_by_id(db, candidate['staff_unit_curator_id'])

        curator_user = curator_staff_unit.users[0]

        document_template = hr_document_template_service.get_by_id(
            db, template_id
        )

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            arr = document_template.path.rsplit(".")
            extension = arr[len(arr) - 1]
            temp_file_path = temp.name + "." + extension

            urllib.request.urlretrieve(document_template.path, temp_file_path)

        template = DocxTemplate(temp_file_path)

        context = {
            'candidate': candidate_user,
            'curator': curator_user,
            'year': 2023,
            'month': 'December',
            'day': 1
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
