import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class AdditionalProfile(Model):

    __tablename__ = "additional_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))

    profile = relationship("Profile")
