import uuid
from sqlalchemy import Column, ForeignKey, String, Enum as EnumType
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from enum import Enum
from core import Base
from models import Model


class DestinationCountry(Enum):
    test = "test"

class AbroadTravel(Model, Base):

    __tablename__ = "medical_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    vehicle_type = Column(String(255), nullable=False)
    destination_country = Column(EnumType(DestinationCountry), nullable=False, default=DestinationCountry.test)
    date_from = Column(TIMESTAMP(timezone=True), nullable=False)
    date_to = Column(TIMESTAMP(timezone=True), nullable=False)
    reason = Column(String(255), nullable=False, default="")
    document_link = Column(String(255), nullable=False, default="")

    profile_id = Column(UUID(as_uuid=True), ForeignKey("additional_profiles.id"), nullable=False)

    profile = relationship("AdditionalProfile")