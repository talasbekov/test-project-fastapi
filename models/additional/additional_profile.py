import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class AdditionalProfile(Model):

    __tablename__ = "additional_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    profile = relationship("Profile")
    
    polygraph_checks = relationship("PolygraphCheck", back_populates="profile", cascade="all, delete")
    violations = relationship("Violation", back_populates="profile", cascade="all, delete")
    abroad_travels = relationship("AbroadTravel", back_populates="profile", cascade="all, delete")
    psychological_checks = relationship("PsychologicalCheck", back_populates="profile", cascade="all, delete")
    special_checks = relationship("SpecialCheck", back_populates="profile", cascade="all, delete")
