import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

from core import Base
from models import Model


class SpecialCheck(Model):

    __tablename__ = "special_checks"

    number = Column(String(255), nullable=False)
    issued_by = Column(String(255), nullable=False)
    date_of_issue = Column(TIMESTAMP(timezone=True), nullable=False)
    document_link = Column(String(255), nullable=False)

    profile_id = Column(UUID(as_uuid=True), ForeignKey("additional_profiles.id"))

    profile = relationship("AdditionalProfile")

