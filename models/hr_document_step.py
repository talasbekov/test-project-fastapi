import enum
import uuid

from sqlalchemy import (TIMESTAMP, Boolean, Column, Enum, ForeignKey, String,
                        text)
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import backref, relationship

from core import Base


class HrDocumentStep(Base):
        
    __tablename__ = "hr_document_steps"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    hr_document_template_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_templates.id"), nullable=False)
    position_id = Column(UUID(as_uuid=True), ForeignKey('positions.id'), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    previous_step_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_steps.id"))

    next_step = relationship("HrDocumentStep", foreign_keys=previous_step_id)
    role = relationship("Role", cascade="all,delete")
    position = relationship("Position",  cascade="all,delete")
    hr_document_type = relationship("HrDocumentTemplate", cascade="all,delete")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
