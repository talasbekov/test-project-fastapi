import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, String, text, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON, TEXT
from sqlalchemy.orm import relationship, backref

from core import Base

class HrDocumentStep(Base):
        
    __tablename__ = "hr_document_steps"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    hr_document_template_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_templates.id"), nullable=False)
    position_id = Column(UUID(as_uuid=True), ForeignKey('positions.id'), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    previous_step_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_steps.id"))

    previous_step = relationship("HrDocumentStep")
    role = relationship("Role", cascade="all,delete")
    position = relationship("Position",  cascade="all,delete")
    hr_document_type = relationship("HrDocumentTemplate", cascade="all,delete")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
