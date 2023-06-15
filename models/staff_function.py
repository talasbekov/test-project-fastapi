import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel
from .association import staff_unit_function


class JurisdictionEnum(str, enum.Enum):
    ALL_SERVICE = "Вся служба"
    PERSONNEL = "Личный Состав"
    COMBAT_UNIT = "Боевое Подразделение"
    STAFF_UNIT = "Штабное Подразделение"
    CANDIDATES = "Кандидаты"
    SUPERVISED_EMPLOYEES = "Курьируемые сотрудники"


class DocumentFunctionTypeEnum(str, enum.Enum):
    INITIATOR = "Инициатор"
    EXPERT = "Эксперт"
    APPROVER = "Утверждающий"
    COORDINATOR = "Согласующий"
    NOTIFIED = "Уведомляемый"


class ServiceFunctionType(NamedModel):

    __tablename__ = "service_function_types"

    staff_functions = relationship("ServiceStaffFunction", back_populates="type", cascade="all,delete")


class DocumentFunctionType(NamedModel):

    __tablename__ = "document_function_types"

    can_cancel = Column(Boolean, nullable=False)

    staff_functions = relationship("DocumentStaffFunction", back_populates="role", cascade="all,delete")


class StaffFunction(NamedModel):

    __tablename__ = "staff_functions"

    hours_per_week = Column(Integer())
    discriminator = Column(String(255))
    is_active = Column(Boolean, nullable=True)

    staff_units = relationship("StaffUnit", secondary=staff_unit_function)

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "staff_function",
    }


class DocumentStaffFunction(StaffFunction):

    role_id = Column(UUID(as_uuid=True), ForeignKey("document_function_types.id"))
    jurisdiction_id = Column(UUID(as_uuid=True), ForeignKey("jurisdictions.id"))

    priority = Column(Integer)

    role = relationship("DocumentFunctionType")
    hr_document_step = relationship("HrDocumentStep", back_populates='staff_function',cascade="all,delete", uselist=False)
    jurisdiction = relationship("Jurisdiction", cascade="all, delete")

    __mapper_args__ = {
        "polymorphic_identity": "document_staff_function"
    }


class ServiceStaffFunction(StaffFunction):

    type_id = Column(UUID(as_uuid=True), ForeignKey("service_function_types.id"))

    type = relationship("ServiceFunctionType", back_populates="staff_functions")

    __mapper_args__ = {
        "polymorphic_identity": "service_staff_function"
    }
