import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model
"""
 polygraph_checks: Optional[List[PolygraphCheckRead]] = []
    violations: Optional[List[ViolationRead]] = []
    abroad_travels: Optional[List[AbroadTravelRead]] = []
    psychological_checks: Optional[List[PsychologicalCheckRead]] = []
"""

class AdditionalProfile(Model):

    __tablename__ = "additional_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    profile = relationship("Profile")
    
    polygraph_checks = relationship("PolygraphCheck", cascade="all, delete")
    violations = relationship("Violation", cascade="all, delete")
    abroad_travels = relationship("AbroadTravel", cascade="all, delete")
    psychological_checks = relationship("PsychologicalCheck", cascade="all, delete")
