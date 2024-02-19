from sqlalchemy.orm import relationship

from models import NamedModel


class SportType(NamedModel):

    __tablename__ = "hr_erp_sport_types"

    sport_degrees = relationship("SportDegree", back_populates="sport_type")
    sport_achievements = relationship(
        "SportAchievement",
        back_populates="sport_type")
