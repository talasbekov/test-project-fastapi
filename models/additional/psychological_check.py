from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from models import Model


class PsychologicalCheck(Model):

    __tablename__ = "hr_erp_psychological_checks"

    issued_by = Column(String(255), nullable=False)
    date_of_issue = Column(TIMESTAMP(timezone=True), nullable=False)
    document_link = Column(String(255), nullable=False)
    document_number = Column(String(255), nullable=True)

    profile_id = Column(String(),
                        ForeignKey("hr_erp_additional_profiles.id"))

    profile = relationship(
        "AdditionalProfile",
        back_populates="psychological_checks")
