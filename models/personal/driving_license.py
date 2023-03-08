from sqlalchemy import ARRAY, TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class DrivingLicense(Model, Base):

    __tablename__ = "driving_licenses"

    document_number = Column(String)
    category = Column(ARRAY(String))
    date_of_issue = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
    document_link = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile", back_populates="driving_licenses")
