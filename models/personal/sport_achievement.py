from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Boolean, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel


class SportAchievement(NamedModel, Base):

    __tablename__ = "sport_achievements"

    assignment_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")
