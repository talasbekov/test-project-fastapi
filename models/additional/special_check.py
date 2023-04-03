from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import Model


class SpecialCheck(Model):

    __tablename__ = "special_checks"

    number = Column(String(255), nullable=False)
    issued_by = Column(String(255), nullable=False)
    date_of_issue = Column(TIMESTAMP(timezone=True), nullable=False)
    document_link = Column(String(255), nullable=False)

    profile_id = Column(UUID(as_uuid=True), ForeignKey("additional_profiles.id"))

    profile = relationship("AdditionalProfile", back_populates="special_checks")
