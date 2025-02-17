from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class PersonalProfile(Model):
    __tablename__ = "hr_erp_personal_profiles"

    profile_id = Column(
        String(),
        ForeignKey("hr_erp_profiles.id"),
        nullable=False)

    profile = relationship("Profile", back_populates="personal_profile")

    identification_card = relationship(
        "IdentificationCard",
        back_populates="profile",
        cascade="all,delete",
        uselist=False)
    biographic_info = relationship(
        "BiographicInfo",
        back_populates="profile",
        cascade="all,delete",
        uselist=False)
    driving_license = relationship(
        "DrivingLicense",
        back_populates="profile",
        cascade="all,delete",
        uselist=False,
        lazy="joined")
    passport = relationship(
        "Passport",
        back_populates="profile",
        cascade="all,delete",
        uselist=False)
    sport_achievements = relationship(
        "SportAchievement",
        back_populates="profile",
        cascade="all,delete")
    sport_degrees = relationship(
        "SportDegree",
        back_populates="profile",
        cascade="all,delete")
    tax_declarations = relationship(
        "TaxDeclaration",
        back_populates="profile",
        cascade="all,delete")
    user_financial_infos = relationship(
        "UserFinancialInfo",
        back_populates="profile",
        cascade="all,delete")
