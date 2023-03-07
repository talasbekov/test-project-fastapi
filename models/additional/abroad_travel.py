import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

from core import Base
from models import Model

class VehicleType(Enum):
    car = "car"
    bus = "bus"
    train = "train"
    plane = "plane"

class DestinationCountry(Enum):
    test = "test"


class AbroadTravel(Model):

    __tablename__ = "medical_profiles"

    vehicle_type = Column(Enum(VehicleType), nullable=False)
    destination_country = Column(Enum(DestinationCountry), nullable=False)
    date_from = Column(TIMESTAMP(timezone=True), nullable=False)
    date_to = Column(TIMESTAMP(timezone=True), nullable=False)
    reason = Column(String(255), nullable=False)
    document_link = Column(String(255), nullable=False)

    profile_id = Column(UUID(as_uuid=True), ForeignKey("additional_profiles.id"))

    profile = relationship("AdditionalProfile")

