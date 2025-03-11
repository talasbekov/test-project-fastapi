from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class AdditionalProfile(Model):

    __tablename__ = "hr_erp_additional_profiles"

    profile_id = Column(String(), ForeignKey("hr_erp_profiles.id"))
    profile = relationship("Profile")

    polygraph_checks = relationship(
        "PolygraphCheck",
        back_populates="profile",
        )
    violations = relationship(
        "Violation",
        back_populates="profile",
        )
    abroad_travels = relationship(
        "AbroadTravel",
        back_populates="profile",
        )
    psychological_checks = relationship(
        "PsychologicalCheck",
        back_populates="profile",
        )
    special_checks = relationship(
        "SpecialCheck",
        back_populates="profile",
        )
    properties = relationship("Properties", back_populates="profile")
    service_housing = relationship("ServiceHousing", back_populates="profile")
    user_vehicles = relationship("Vehicle", back_populates="profile")
