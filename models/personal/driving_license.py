from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, TEXT
from sqlalchemy.orm import relationship

from models import Model


class DrivingLicense(Model):

    __tablename__ = "hr_erp_driving_licenses"

    document_number = Column(String, nullable=True)
    category = Column(String, nullable=True)
    date_of_issue = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(
        String(),
        ForeignKey("hr_erp_personal_profiles.id"),
        nullable=False)

    profile = relationship("PersonalProfile", back_populates="driving_license")
