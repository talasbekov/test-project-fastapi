from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


from .association import archive_staff_unit_function


class ArchiveDocumentFunctionType(NamedModel):

    __tablename__ = "hr_erp_arch_doc_fun_types"

    can_cancel = Column(Boolean, nullable=False)

    origin_id = Column(String(), ForeignKey(
        "hr_erp_document_function_types.id"), nullable=True)

    staff_functions = relationship(
        "ArchiveDocumentStaffFunction",
        back_populates="role",
        cascade="all,delete")


class ArchiveServiceFunctionType(NamedModel):

    __tablename__ = "hr_erp_arch_ser_func_type"

    origin_id = Column(String(), ForeignKey(
        "hr_erp_service_function_types.id"), nullable=True)

    staff_functions = relationship(
        "ArchiveServiceStaffFunction",
        back_populates="type",
        cascade="all,delete")


class ArchiveStaffFunction(NamedModel):

    __tablename__ = "hr_erp_archive_staff_functions"

    hours_per_week = Column(Integer())
    discriminator = Column(String(255))

    staff_units = relationship(
        "ArchiveStaffUnit",
        secondary=archive_staff_unit_function)

    origin_id = Column(
        String(),
        ForeignKey("hr_erp_staff_functions.id"),
        nullable=True)

    origin = relationship("StaffFunction", back_populates="archived")

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "staff_function",
    }


class ArchiveDocumentStaffFunction(ArchiveStaffFunction):

    role_id = Column(String(), ForeignKey(
        "hr_erp_arch_doc_fun_types.id"))
    jurisdiction_id = Column(
        String(),
        ForeignKey("hr_erp_jurisdictions.id"))

    priority = Column(Integer)

    role = relationship(
        "ArchiveDocumentFunctionType",
        back_populates="staff_functions",
        foreign_keys=role_id)
    jurisdiction = relationship("Jurisdiction")

    __mapper_args__ = {
        "polymorphic_identity": "document_staff_function"
    }


class ArchiveServiceStaffFunction(ArchiveStaffFunction):

    type_id = Column(String(), ForeignKey(
        "hr_erp_arch_ser_func_type.id"))

    type = relationship("ArchiveServiceFunctionType", foreign_keys=type_id)

    __mapper_args__ = {
        "polymorphic_identity": "service_staff_function"
    }
