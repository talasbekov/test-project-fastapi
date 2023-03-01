import enum
import uuid

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model, NamedModel

from .association import staff_unit_function


class RoleName(str, enum.Enum):
    AGREER = "Утверждающий"
    EXPERT = "Эксперт"
    APPROVER = "Согласующий"
    NOTIFIER = "Увемдомляемый"
    INITIATOR = "Инициатор"


class ServiceFunctionType(NamedModel, Base):

    __tablename__ = "service_function_types"


class DocumentFunctionType(NamedModel, Base):

    __tablename__ = "document_function_types"

    can_cancel = Column(Boolean, nullable=False)


class StaffFunction(NamedModel, Base):

    __tablename__ = "staff_functions"

    hours_per_week = Column(Integer())
    discriminator = Column(String(255))

    staff_units = relationship("StaffUnit", secondary=staff_unit_function)

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "staff_function",
    }


class DocumentStaffFunction(StaffFunction):

    priority = Column(Integer())
    role_id = Column(UUID(as_uuid=True), ForeignKey("document_function_types.id"))

    role = relationship("DocumentFunctionType")

    __mapper_args__ = {
        "polymorphic_identity": "document_staff_function"
    }


class ServiceStaffFunction(StaffFunction):

    type_id = Column(UUID(as_uuid=True), ForeignKey("service_function_types.id"))

    type = relationship("ServiceFunctionType")

    __mapper_args__ = {
        "polymorphic_identity": "service_staff_function"
    }
