from sqlalchemy import Column, TEXT
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class Vehicle(NamedModel):

    __tablename__ = "hr_erp_user_vehicles"

    date_from = Column(TIMESTAMP(timezone=True), nullable=False)
    number = Column('vehicle_number', String(255), nullable=False, default="")
    document_link = Column(TEXT, nullable=True)
    vin_code = Column(String, nullable=False)

    profile_id = Column(String(), ForeignKey(
        "hr_erp_additional_profiles.id"), nullable=False)
    profile = relationship("AdditionalProfile", back_populates="user_vehicles")
