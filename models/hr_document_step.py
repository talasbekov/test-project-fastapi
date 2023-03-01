import enum
import uuid

from sqlalchemy import (TIMESTAMP, Boolean, Column, Enum, ForeignKey, String,
                        text)
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import backref, relationship

from core import Base
from models import Model


class HrDocumentStep(Model, Base):

    __tablename__ = "hr_document_steps"

    hr_document_template_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_templates.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    staff_unit_id = Column(UUID(as_uuid=True), ForeignKey('staff_units.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    staff_function_id = Column(UUID(as_uuid=True), ForeignKey("staff_functions.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    previous_step_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_steps.id"))
    jurisdiction_id = Column(UUID(as_uuid=True), ForeignKey("jurisdictions.id"))
    next_step = relationship("HrDocumentStep", foreign_keys=previous_step_id)
    staff_function = relationship("StaffFunction")
    staff_unit = relationship("StaffUnit")
    hr_document_template = relationship("HrDocumentTemplate")
