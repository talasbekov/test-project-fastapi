
from sqlalchemy import Column, ForeignKey,Integer, String, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from enum import Enum as EnumBase


class SpecialtyEnum(EnumBase):
    specialty1 = "Специалист 1 класса - наставник (мастер)"
    specialty2 = "Специалист 2 класса - наставник (мастер)"
    specialty3 = "Специалист 3 класса - наставник (мастер)"

class CoolnessStatusEnum(EnumBase):
    granted = "Выдан"
    confirmed = "Подтвержден"
    removed = "Изъят"

class CoolnessType(NamedModel):

    __tablename__ = "coolness_types"
    order = Column(Integer, nullable=False)

    coolnesses = relationship("Coolness", back_populates="type")

class Coolness(Model):

    __tablename__ = "coolnesses"
    type_id = Column(UUID(as_uuid=True), ForeignKey("coolness_types.id"))
    type = relationship("CoolnessType", back_populates="coolnesses")

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="coolnesses")

    history = relationship("CoolnessHistory", back_populates="coolness", uselist=False)
