import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class MedicalProfile(Model):

    __tablename__ = "medical_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))

    profile = relationship("Profile", back_populates="medical_profile")
