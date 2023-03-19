from sqlalchemy import (TIMESTAMP, Column, ForeignKey,
                        TEXT)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel


class SportAchievement(NamedModel, Base):

    __tablename__ = "sport_achievements"

    assignment_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)
    sport_type_id = Column(UUID(as_uuid=True), ForeignKey("sport_types.id"), nullable=False)

    sport_type = relationship("SportType", back_populates="sport_achievements")
    profile = relationship("PersonalProfile", back_populates="sport_achievements")
