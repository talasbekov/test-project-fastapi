from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class PersonalProfile(Model, Base):

    __tablename__ = "personal_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)

    profile = relationship("Profile", back_populates="personal_profile")

    identification_cards = relationship("IdentificationCard", back_populates="profile", cascade="all,delete")
    biographic_infos = relationship("BiographicInfo", back_populates="profile", cascade="all,delete")
    driving_licences = relationship("DrivingLicence", back_populates="profile", cascade="all,delete")
    passports = relationship("Passport", back_populates="profile", cascade="all,delete")
    sport_achievements = relationship("SportAchievement", back_populates="profile", cascade="all,delete")
    sport_degrees = relationship("SportDegree", back_populates="profile", cascade="all,delete")
    tax_declarations = relationship("TaxDeclaration", back_populates="profile", cascade="all,delete")
    user_financial_infos = relationship("UserFinancialInfo", back_populates="profile", cascade="all,delete")
