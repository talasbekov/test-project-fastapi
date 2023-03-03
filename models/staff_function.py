import enum
import uuid

from sqlalchemy import TIMESTAMP, Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base

from .association import staff_unit_functions


class RoleName(str, enum.Enum):
    AGREER = "Утверждающий"
    EXPERT = "Эксперт"
    APPROVER = "Согласующий"
    NOTIFIER = "Увемдомляемый"
    INITIATOR = "Инициатор"


class ServiceFunctionType(Base):

    __tablename__ = "service_function_types"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)


class DocumentFunctionType(Base):

    __tablename__ = "document_function_types"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    can_cancel = Column(Boolean, nullable=False)


class StaffFunction(Base):

    __tablename__ = "staff_functions"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    hours_per_week = Column(Integer())
    discriminator = Column(String(255))

    __mapper_args__ = {
        "polymorphic_on": "discriminator",
        "polymorphic_identity": "staff_function",
    }

    staff_units = relationship(
        "StaffUnit",
        secondary=staff_unit_functions,
        back_populates="staff_functions",
        cascade="all,delete"
    )


class DocumentStaffFunction(StaffFunction):

    priority = Column(Integer(), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("document_function_types.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    role = relationship("DocumentFunctionType")

    __mapper_args__ = {
        "polymorphic_identity": "document_staff_function"
    }


class ServiceStaffFunction(StaffFunction):

    type_id = Column(UUID(as_uuid=True), ForeignKey("service_function_types.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    type = relationship("ServiceFunctionType")

    __mapper_args__ = {
        "polymorphic_identity": "service_staff_function"
    }
