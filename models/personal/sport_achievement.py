from sqlalchemy import (TIMESTAMP, Column, ForeignKey,
                        TEXT, String)
from sqlalchemy.orm import relationship

from models import NamedModel


class SportAchievement(NamedModel):

    __tablename__ = "sport_achievements"

    assignment_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(
        String(),
        ForeignKey("personal_profiles.id"),
        nullable=False)
    sport_type_id = Column(
        String(),
        ForeignKey("sport_types.id"),
        nullable=False)

    sport_type = relationship("SportType", back_populates="sport_achievements")
    profile = relationship(
        "PersonalProfile",
        back_populates="sport_achievements")
