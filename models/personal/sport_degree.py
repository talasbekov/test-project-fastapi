from sqlalchemy import (TEXT, TIMESTAMP, Column, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class SportDegree(NamedModel):

    __tablename__ = "sport_degrees"

    assignment_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(TEXT)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)
    sport_type_id = Column(UUID(as_uuid=True), ForeignKey("sport_types.id"), nullable=False)

    sport_type = relationship("SportType", back_populates="sport_degrees")
    profile = relationship("PersonalProfile", back_populates="sport_degrees")
