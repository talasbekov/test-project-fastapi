import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from models import Model
from models.association import family_abroad_travel


class AbroadTravel(Model):

    __tablename__ = "hr_erp_abroad_travels"

    id = Column(
        String(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False)
    vehicle_type_id = Column(
        String(),
        ForeignKey("hr_erp_vehicle_types.id"), nullable=True)
    vehicle_type = relationship("VehicleType")
    destination_country_id = Column(
        String(),
        ForeignKey('hr_erp_countries.id'),
        nullable=True)
    date_from = Column(TIMESTAMP(timezone=True), nullable=False)
    date_to = Column(TIMESTAMP(timezone=True), nullable=False)
    reason = Column(String(255), nullable=False, default="")
    reasonKZ = Column('reasonkz', String, nullable=True)
    document_link = Column(String(255), nullable=False, default="")

    profile_id = Column(String(), ForeignKey(
        "hr_erp_additional_profiles.id"), nullable=True)

    profile = relationship(
        "AdditionalProfile",
        back_populates="abroad_travels")
    destination_country = relationship(
        "Country", back_populates="abroad_travels")

    family_abroad_travel = relationship(
        "AbroadTravel",
        secondary=family_abroad_travel,
        cascade="all, delete")