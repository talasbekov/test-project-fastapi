from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from enum import Enum as EnumBase


class FormEnum(EnumBase):
    form1 = "Форма 1"
    form2 = "Форма 2"
    form3 = "Форма 3"


class PrivilegeEmergency(Model):

    __tablename__ = "privelege_emergencies"
    form = Column(Enum(FormEnum), nullable=True)
    date_from = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="privelege_emergencies")
