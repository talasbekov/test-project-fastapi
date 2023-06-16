from sqlalchemy import Column, TEXT
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class Vehicle(NamedModel):

    __tablename__ = "user_vehicles"

    date_from = Column(TIMESTAMP(timezone=True), nullable=False)
    number = Column(String(255), nullable=False, default="")
    document_link = Column(TEXT, nullable=True)
    vin_code = Column(String, nullable=False)

    profile_id = Column(UUID(as_uuid=True), ForeignKey(
        "additional_profiles.id"), nullable=False)
    profile = relationship("AdditionalProfile", back_populates="user_vehicles")
