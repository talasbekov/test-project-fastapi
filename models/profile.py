from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Profile(Model, Base):

    __tablename__ = "profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", cascade="all, delete")

    personal_profile = relationship("PersonalProfile", back_populates="profile", cascade="all,delete", uselist=False)
