import enum

from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class FamilyStatusEnum(str, enum.Enum):
    MARRIED = "Married"
    WIDOWED = "Widowed"
    SEPARATED = "Separated"
    DIVORCED = "Divorced"
    SINGLE = "Single"


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
