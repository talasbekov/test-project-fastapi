import enum
import uuid

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import TimeBaseModel

from .association import user_functions


class RoleName(str, enum.Enum):
    AGREER = "Утверждающий"
    EXPERT = "Эксперт"
    APPROVER = "Согласующий"
    NOTIFIER = "Увемдомляемый"
    INITIATOR = "Инициатор"


class ServiceFunctionType(TimeBaseModel, Base):

    __tablename__ = "service_function_types"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)


class DocumentFunctionType(TimeBaseModel, Base):

    __tablename__ = "document_function_types"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    can_cancel = Column(Boolean, nullable=False)


class StaffFunction(TimeBaseModel, Base):

    __tablename__ = "staff_functions"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    hours_per_week = Column(Integer())
    discriminator = Column(String(255))

    users = relationship("User", secondary=user_functions)

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
