from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Profile(Model, Base):

    __tablename__ = "profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", cascade="all, delete")

    additional_profile_id = Column(UUID(as_uuid=True), ForeignKey("additional_profiles.id"))
    additional_profile = relationship("AdditionalProfile", cascade="all, delete")
