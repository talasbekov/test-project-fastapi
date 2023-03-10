import uuid

from sqlalchemy import BigInteger, Column, Enum as EnumType, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from enum import Enum

from core import Base
from models import Model


class Properties(Model):

    __tablename__ = "properties"

    type_id =Column(UUID(as_uuid=True), ForeignKey("property_types.id"))

    purchase_date = Column(TIMESTAMP(timezone=True), nullable=False)
    address = Column(String(255), nullable=False)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("additional_profiles.id"))
    profile = relationship("AdditionalProfile", back_populates="properties")

    type = relationship("PropertyType", back_populates="properties")
