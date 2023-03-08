import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class AnthropometricData(Model):

    __tablename__ = "anthropometric_data"

    head_circumference = Column(Integer)
    shoe_size = Column(Integer)
    neck_circumference = Column(Integer)
    shape_size = Column(Integer)
    bust_size = Column(Integer)
    
    profile_id = Column(UUID(as_uuid=True), ForeignKey("medical_profiles.id"))

    profile = relationship("MedicalProfile")
