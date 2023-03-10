import uuid

from sqlalchemy import BigInteger, Column, Enum as EnumType, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from enum import Enum

from core import Base
from models import NamedModel


class PropertyType(NamedModel):
    __tablename__ = "property_types"

    properties = relationship("Properties", back_populates="type")
