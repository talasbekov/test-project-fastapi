from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class PersonalProfile(Model):

    __tablename__ = "personal_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)

    profile = relationship("Profile", back_populates="personal_profile")

    identification_card = relationship("IdentificationCard", back_populates="profile", cascade="all,delete", uselist=False)
    biographic_info = relationship("BiographicInfo", back_populates="profile", cascade="all,delete", uselist=False)
    driving_license = relationship("DrivingLicense", back_populates="profile", cascade="all,delete", uselist=False)
    passport = relationship("Passport", back_populates="profile", cascade="all,delete", uselist=False)
    sport_achievements = relationship("SportAchievement", back_populates="profile", cascade="all,delete")
    sport_degrees = relationship("SportDegree", back_populates="profile", cascade="all,delete")
    tax_declarations = relationship("TaxDeclaration", back_populates="profile", cascade="all,delete")
    user_financial_infos = relationship("UserFinancialInfo", back_populates="profile", cascade="all,delete")
