import uuid
from typing import List

from sqlalchemy.orm import Session

from models import (
    DocumentStaffFunction,
    HrDocumentStep,
)
from exceptions import NotSupportedException


class BaseCategory:
    __handler__ = 0

    def handle(self, db: Session, user_id: uuid.UUID) -> list[uuid.UUID]:
        raise NotSupportedException(
            f"Don't use this class: {self.__class__.__name__} directly")

    def get_templates(
        self,
        db: Session,
        role_id: uuid.UUID,
        user_id: uuid.UUID,
        handler: int
    ) -> List[uuid.UUID]:
        functions = (
            db.query(DocumentStaffFunction)
            .join(HrDocumentStep)
            .filter(
                DocumentStaffFunction.role_id == role_id,
                DocumentStaffFunction.hr_document_step != None,
                HrDocumentStep.category == handler,
            ).all()
        )
        return [function.hr_document_step.hr_document_template_id
                for function in functions]



handler = BaseCategory()
