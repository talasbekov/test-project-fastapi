from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class FamilyProfile(Model):

    __tablename__ = "hr_erp_family_profiles"

    profile_id = Column(String(), ForeignKey("hr_erp_profiles.id"))

    profile = relationship("Profile", back_populates="family_profile")
    family = relationship(
        "Family",
        back_populates="profile",
        cascade="all, delete")
