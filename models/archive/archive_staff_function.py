from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel


from .association import archive_staff_unit_function


class RoleName(str, Enum):
    AGREER = "Утверждающий"
    EXPERT = "Эксперт"
    APPROVER = "Согласующий"
    NOTIFIER = "Увемдомляемый"
    INITIATOR = "Инициатор"


class ArchiveDocumentFunctionType(NamedModel):

    __tablename__ = "archive_document_function_types"

    can_cancel = Column(Boolean, nullable=False)

    origin_id = Column(UUID(as_uuid=True), ForeignKey("document_function_types.id"), nullable=True)

    staff_functions = relationship("ArchiveDocumentStaffFunction", back_populates="role", cascade="all,delete")


class ArchiveServiceFunctionType(NamedModel):

    __tablename__ = "archive_service_function_types"

    origin_id = Column(UUID(as_uuid=True), ForeignKey("service_function_types.id"), nullable=True)

    staff_functions = relationship("ArchiveServiceStaffFunction", back_populates="type", cascade="all,delete")


class ArchiveStaffFunction(NamedModel):

    __tablename__ = "archive_staff_functions"

    hours_per_week = Column(Integer())
    discriminator = Column(String(255))

    staff_units = relationship("ArchiveStaffUnit", secondary=archive_staff_unit_function)

    origin_id = Column(UUID(as_uuid=True), ForeignKey("staff_functions.id"), nullable=True)

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "staff_function",
    }


class ArchiveDocumentStaffFunction(ArchiveStaffFunction):

    role_id = Column(UUID(as_uuid=True), ForeignKey("archive_document_function_types.id"))
    jurisdiction_id = Column(UUID(as_uuid=True), ForeignKey("jurisdictions.id"))

    priority = Column(Integer)

    role = relationship("ArchiveDocumentFunctionType", back_populates="staff_functions", foreign_keys=role_id)
    jurisdiction = relationship("Jurisdiction")

    __mapper_args__ = {
        "polymorphic_identity": "document_staff_function"
    }


class ArchiveServiceStaffFunction(ArchiveStaffFunction):

    type_id = Column(UUID(as_uuid=True), ForeignKey("archive_service_function_types.id"))

    type = relationship("ArchiveServiceFunctionType", foreign_keys=type_id)

    __mapper_args__ = {
        "polymorphic_identity": "service_staff_function"
    }
