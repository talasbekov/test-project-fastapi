from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Passport(Model, Base):

    __tablename__ = "passports"

    document_number = Column(String)
    date_of_issue = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile", back_populates="passport")
