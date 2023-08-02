from enum import Enum

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import NamedModel, Model


class StatusEnum(Enum):
    ROOT = 'отпуск'
    VACATION = 'В отпуске'
    MATERNITY_LEAVE = 'В отпуске по беременности и родам'
    SICK_LEAVE = 'В отпуске по болезни'
    BUSINESS_TRIP = 'В командировке'
    ANNUAL_LEAVE = 'Ежегодный отпуск'


class StatusType(NamedModel):

    __tablename__ = "status_types"

    statuses = relationship("Status", back_populates="type")


class Status(Model):

    __tablename__ = "statuses"

    type_id = Column(String(), ForeignKey("status_types.id"))
    type = relationship("StatusType", back_populates="statuses")

    user_id = Column(String(), ForeignKey("users.id"))
    user = relationship("User", back_populates="statuses")

    history = relationship(
        "StatusHistory",
        back_populates="status",
        uselist=False)

    history = relationship(
        "StatusHistory",
        back_populates="status",
        uselist=False)
