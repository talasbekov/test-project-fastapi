from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class PersonalProfile(Model, Base):

    __tablename__ = "personal_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)

    profile = relationship("Profile", cascade="all, delete")
