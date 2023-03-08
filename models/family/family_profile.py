from sqlalchemy import ARRAY, TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class FamilyProfile(Model):

    __tablename__ = "family_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))

    profile = relationship("Profile", back_populates="family_profile")
    family = relationship("Family", back_populates="profile", cascade="all, delete")
