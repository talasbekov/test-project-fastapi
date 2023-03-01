import enum
import uuid

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship

from core import Base
from models import Model


class HrDocumentStep(Model, Base):

    __tablename__ = "hr_document_steps"

    hr_document_template_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_templates.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    staff_function_id = Column(UUID(as_uuid=True), ForeignKey("staff_functions.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    jurisdiction_id = Column(UUID(as_uuid=True), ForeignKey("jurisdictions.id"))
    priority = Column(Integer, nullable=False)

    staff_function = relationship("StaffFunction")
    jurisdiction = relationship("Jurisdiction")
    hr_document_template = relationship("HrDocumentTemplate")
