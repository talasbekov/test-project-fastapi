import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import Model


class AbroadTravel(Model):

    __tablename__ = "abroad_travels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    vehicle_type = Column(String(255), nullable=False)
    destination_country_id = Column(UUID(as_uuid=True), ForeignKey('countries.id'), nullable=False)
    date_from = Column(TIMESTAMP(timezone=True), nullable=False)
    date_to = Column(TIMESTAMP(timezone=True), nullable=False)
    reason = Column(String(255), nullable=False, default="")
    document_link = Column(String(255), nullable=False, default="")

    profile_id = Column(UUID(as_uuid=True), ForeignKey("additional_profiles.id"), nullable=True)

    profile = relationship("AdditionalProfile", back_populates="abroad_travels")
    destination_country = relationship("Country", back_populates="abroad_travels")
