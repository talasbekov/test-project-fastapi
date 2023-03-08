import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Profile(Model):

    __tablename__ = "profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="profile")

    educational_profile = relationship("EducationalProfile", back_populates="profile", cascade="all,delete", uselist=False)
