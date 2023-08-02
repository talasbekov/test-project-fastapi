from sqlalchemy import (TEXT, TIMESTAMP, Column, ForeignKey, String)
from sqlalchemy.orm import relationship

from models import NamedModel


class SportDegree(NamedModel):

    __tablename__ = "sport_degrees"

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

    sport_type = relationship("SportType", back_populates="sport_degrees")
    profile = relationship("PersonalProfile", back_populates="sport_degrees")
