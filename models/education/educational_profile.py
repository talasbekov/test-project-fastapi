from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from models import Model


class EducationalProfile(Model, Base):

    __tablename__ = "educational_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    profile = relationship("Profile")
