from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class AdditionalProfile(Model):

    __tablename__ = "additional_profiles"

    profile_id = Column(String(), ForeignKey("profiles.id"))
    profile = relationship("Profile")

    polygraph_checks = relationship(
        "PolygraphCheck",
        back_populates="profile",
        cascade="all, delete")
    violations = relationship(
        "Violation",
        back_populates="profile",
        cascade="all, delete")
    abroad_travels = relationship(
        "AbroadTravel",
        back_populates="profile",
        cascade="all, delete")
    psychological_checks = relationship(
        "PsychologicalCheck",
        back_populates="profile",
        cascade="all, delete")
    special_checks = relationship(
        "SpecialCheck",
        back_populates="profile",
        cascade="all, delete")
    properties = relationship("Properties", back_populates="profile")
    service_housing = relationship("ServiceHousing", back_populates="profile")
    user_vehicles = relationship("Vehicle", back_populates="profile")
