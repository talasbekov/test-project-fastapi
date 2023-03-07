import enum

from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Boolean, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model, NamedModel


class FamilyStatusEnum(str, enum.Enum):
    MARRIED = "Married"
    WIDOWED = "Widowed"
    SEPARATED = "Separated"
    DIVORCED = "Divorced"
    SINGLE = "Single"


class PersonalProfile(Model, Base):

    __tablename__ = "personal_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)

    profile = relationship("Profile", cascade="all, delete")


class BiographicInfo(Model, Base):

    __tablename__ = "biographic_infos"

    place_birth = Column(TIMESTAMP(timezone=True))
    gender = Column(Boolean)
    citizenship = Column(String)
    nationality = Column(String)
    family_status = Column(Enum(FamilyStatusEnum))
    address = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")


class UserFinancialInfo(Model, Base):

    __tablename__ = "user_financial_infos"

    iban = Column(String)
    housing_payments_iban = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")


class TaxDeclaration(Model, Base):

    __tablename__ = "tax_declarations"

    year = Column(String)
    is_paid = Column(Boolean)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")


class SportDegree(NamedModel, Base):

    __tablename__ = "sport_degrees"

    assignment_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")


class SportAchievement(NamedModel, Base):

    __tablename__ = "sport_achievements"

    assignment_date = Column(TIMESTAMP(timezone=True))
    document_link = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")


class IdentificationCard(Model, Base):

    __tablename__ = "identification_cards"

    document_number = Column(String)
    date_of_issue = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
    issued_by = Column(String)
    document_link = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")


class DrivingLicence(Model, Base):

    __tablename__ = "driving_licences"

    document_number = Column(String)
    category = Column(ARRAY(String))
    date_of_issue = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
    document_link = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")


class Passport(Model, Base):

    __tablename__ = "passports"

    document_number = Column(String)
    date_of_issue = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
    document_link = Column(String)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personal_profiles.id"), nullable=False)

    profile = relationship("PersonalProfile")

