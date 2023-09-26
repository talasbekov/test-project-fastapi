from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from models import Model


class DrivingLicense(Model):

    __tablename__ = "hr_erp_driving_licenses"

    document_number = Column(String)
    category = Column(String)
    date_of_issue = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(
        String(),
        ForeignKey("hr_erp_personal_profiles.id"),
        nullable=False)

    profile = relationship("PersonalProfile", back_populates="driving_license")

# @listens_for(DrivingLicense, 'before_update')
# def description_set_listener(mapper, connection, target):
#     if isinstance(target.category, list):
#         target.category = str(target.category)
        
# @listens_for(DrivingLicense, 'before_insert')
# def description_set_listener(mapper, connection, target):
#     if isinstance(target.category, list):
#         target.category = str(target.category)