
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from enum import Enum as EnumBase


class SpecialtyEnum(EnumBase):
    specialty1 = "Специалист 1 класса"
    specialty2 = "Специалист 2 класса"
    specialty3 = "Специалист 3 класса"


class CoolnessStatusEnum(EnumBase):
    granted = {"name": "Присвоен", "nameKZ": "Берілген"}
    confirmed = {"name": "Подтвержден", "nameKZ": "Растады"}
    removed = {"name": "Лишен", "nameKZ": "Жоилды"}
    demoted = {"name": "Снижен", "nameKZ": "Тусирилди"}


class CoolnessType(NamedModel):

    __tablename__ = "hr_erp_coolness_types"
    order = Column('COOLNESS_ORDER', Integer, nullable=False)
    # percentage = Column('PERCENTAGE', Integer, nullable=True)
    coolnesses = relationship("Coolness", back_populates="type")


class Coolness(Model):

    __tablename__ = "hr_erp_coolnesses"
    type_id = Column(String(), ForeignKey("hr_erp_coolness_types.id"))
    type = relationship("CoolnessType", back_populates="coolnesses")

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    user = relationship("User", back_populates="coolnesses")
    
    coolness_status = Column(Enum(CoolnessStatusEnum), nullable=False)

    history = relationship(
        "CoolnessHistory",
        back_populates="coolness",
        uselist=False)
