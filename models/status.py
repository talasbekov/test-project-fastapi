from enum import Enum

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel, Model


class StatusEnum(Enum):
    ROOT = 'отпуск'
    VACATION = 'В отпуске'
    MATERNITY_LEAVE = 'В отпуске по беременности и родам'
    SICK_LEAVE = 'В отпуске по болезни'


class StatusType(NamedModel):

    __tablename__ = "status_types"

    statuses = relationship("Status", back_populates="type")


class Status(Model):

    __tablename__ = "statuses"
    
    type_id = Column(UUID(as_uuid=True), ForeignKey("status_types.id"))
    type = relationship("StatusType", back_populates="statuses")

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="statuses")

    history = relationship("StatusHistory", back_populates="status", uselist=False)
