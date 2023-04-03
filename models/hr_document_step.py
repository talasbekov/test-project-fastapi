from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class HrDocumentStep(Model):

    __tablename__ = "hr_document_steps"

    hr_document_template_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_templates.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    staff_function_id = Column(UUID(as_uuid=True), ForeignKey("staff_functions.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    staff_function = relationship("DocumentStaffFunction", back_populates='hr_document_step', cascade="all,delete")
    hr_document_template = relationship("HrDocumentTemplate")
    hr_document_infos = relationship("HrDocumentInfo", back_populates="hr_document_step", cascade="all,delete")
