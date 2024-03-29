from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.orm import relationship

from models import Model


class HrDocumentStep(Model):

    __tablename__ = "hr_erp_hr_document_steps"

    # Properties
    hr_document_template_id = Column(
        String(),
        ForeignKey(
            "hr_erp_hr_document_templates.id",
            ondelete='CASCADE',
            onupdate='CASCADE'),
        nullable=False)
    staff_function_id = Column(
        String(),
        ForeignKey(
            "hr_erp_staff_functions.id",
            ondelete='CASCADE',
            onupdate='CASCADE'),
        nullable=False)
    is_direct_supervisor = Column(Boolean, default=None)
    category = Column(Integer, default=None)

    # Relationships
    staff_function = relationship("DocumentStaffFunction",
                                  back_populates='hr_document_step',
                                  cascade="all,delete")
    hr_document_template = relationship("HrDocumentTemplate",
                                         back_populates='steps')
    hr_document_infos = relationship("HrDocumentInfo",
                                     back_populates="hr_document_step",
                                     cascade="all,delete")
