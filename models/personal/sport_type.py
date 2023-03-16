from sqlalchemy import (ARRAY, TEXT, TIMESTAMP, Boolean, Column, Enum,
                        ForeignKey, String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class SportType(NamedModel):

    __tablename__ = "sport_types"

    sport_degrees = relationship("SportDegree", back_populates="sport_type")
    sport_achievements = relationship("SportAchievement", back_populates="sport_type")
