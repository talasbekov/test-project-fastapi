from sqlalchemy import Column, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class HrDocumentStep(Model):

    __tablename__ = "hr_document_steps"

    # Properties
    hr_document_template_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey(
            "hr_document_templates.id",
            ondelete='CASCADE',
            onupdate='CASCADE'),
        nullable=False)
    staff_function_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey(
            "staff_functions.id",
            ondelete='CASCADE',
            onupdate='CASCADE'),
        nullable=False)
    is_direct_supervisor = Column(Boolean, default=None)
    category = Column(Integer, default=None)

    # Relationships
    staff_function = relationship("DocumentStaffFunction", back_populates='hr_document_step', cascade="all,delete")
    hr_document_template = relationship("HrDocumentTemplate", back_populates='steps')
    hr_document_infos = relationship("HrDocumentInfo", back_populates="hr_document_step", cascade="all,delete")
