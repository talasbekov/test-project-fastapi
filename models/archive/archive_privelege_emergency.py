from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from enum import Enum as EnumBase


class ArchiveFormEnum(EnumBase):
    form1 = "Форма 1"
    form2 = "Форма 2"
    form3 = "Форма 3"


class ArchivePrivilegeEmergency(Model):

    __tablename__ = "archive_privelege_emergencies"
    form = Column(Enum(ArchiveFormEnum), nullable=True)
    date_from = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)
    origin_id = Column(UUID(as_uuid=True), ForeignKey("privelege_emergencies.id"), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="archive_privelege_emergencies")
