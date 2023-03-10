import uuid
from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as EnumType
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel

 

class Vehicle(NamedModel, Base):

    __tablename__ = "user_vehicles"

    date_from = Column(TIMESTAMP(timezone=True), nullable=False)
    number = Column(String(255), nullable=False, default="")

    profile_id = Column(UUID(as_uuid=True), ForeignKey("additional_profiles.id"), nullable=False)
    profile = relationship("AdditionalProfile", back_populates="user_vehicles")
    