from sqlalchemy import (TEXT, TIMESTAMP, Column, ForeignKey, String)
from sqlalchemy.orm import relationship

from models import Model


class SportDegree(Model):

    __tablename__ = "hr_erp_sport_degrees"

    assignment_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT, nullable=True)
    profile_id = Column(
        String(),
        ForeignKey("hr_erp_personal_profiles.id"),
        nullable=False)
    sport_type_id = Column(
        String(),
        ForeignKey("hr_erp_sport_types.id"),
        nullable=False)
    sport_degree_type_id = Column(
        String(),
        ForeignKey("hr_erp_sport_degree_types.id"),
        nullable=False)

    sport_degree_type = relationship(
        "SportDegreeType", back_populates="sport_degrees")
    sport_type = relationship("SportType", back_populates="sport_degrees")
    profile = relationship("PersonalProfile", back_populates="sport_degrees")
