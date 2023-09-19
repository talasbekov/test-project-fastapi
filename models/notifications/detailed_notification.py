from sqlalchemy import Column, TEXT, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class DetailedNotification(Model):
    __tablename__ = "hr_erp_detailed_notifications"

    hr_document_id = Column(
        String(),
        ForeignKey("hr_erp_hr_documents.id"),
        nullable=False)
    receiver_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"),
        nullable=False,
        index=True)
    survey_id = Column(
        String(),
        ForeignKey("hr_erp_surveys.id"),
        nullable=True)
    
    survey = relationship("Survey", foreign_keys=[survey_id])
    hr_document = relationship("HrDocument", foreign_keys=[hr_document_id])
