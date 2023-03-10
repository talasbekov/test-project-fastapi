import uuid

from sqlalchemy import BigInteger, Column, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class ServiceHousing(Model):

    __tablename__ = "service_housings"

    type_id = Column(UUID(as_uuid=True), ForeignKey("property_types.id"))
    address = Column(String(255))
    issue_date = Column(TIMESTAMP(timezone=True))

    profile_id = Column(UUID(as_uuid=True), ForeignKey("additional_profiles.id"))
    profile = relationship("AdditionalProfile", back_populates="service_housing")

    type = relationship("PropertyType", back_populates="service_housings")
