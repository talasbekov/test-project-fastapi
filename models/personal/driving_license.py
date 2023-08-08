from sqlalchemy import ARRAY, TIMESTAMP, Column, ForeignKey, String, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class DrivingLicense(Model):

    __tablename__ = "hr_erp_driving_licenses"

    document_number = Column(String)
    category = Column(ARRAY(String))
    date_of_issue = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(
        String(),
        ForeignKey("hr_erp_personal_profiles.id"),
        nullable=False)

    profile = relationship("PersonalProfile", back_populates="driving_license")
