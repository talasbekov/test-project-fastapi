from sqlalchemy import (TIMESTAMP, Boolean, Column, ForeignKey, Integer, String)
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship

from models import Model


class HrDocumentInfo(Model):

    __tablename__ = "hr_document_infos"

    hr_document_step_id = Column(
        String(),
        ForeignKey("hr_document_steps.id"),
        nullable=False)

    assigned_to_id = Column(
        String(),
        ForeignKey("users.id"),
        nullable=True)
    signed_by_id = Column(
        String(),
        ForeignKey("users.id"),
        nullable=True)

    comment = Column('DOCUMENT_COMMENT', TEXT())

    is_signed = Column(Boolean())

    signed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    order = Column('DOCUMENT_ORDER', Integer, default=1)

    hr_document_id = Column(
        String(),
        ForeignKey("hr_documents.id"),
        nullable=False)

    hr_document_step = relationship(
        "HrDocumentStep",
        back_populates="hr_document_infos")
    signed_by = relationship("User", foreign_keys=signed_by_id)
    assigned_to = relationship("User", foreign_keys=assigned_to_id)
    hr_document = relationship(
        "HrDocument",
        back_populates="hr_document_infos")
