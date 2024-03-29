import enum

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from models import NamedModel, Model


class PermissionEnum(str, enum.Enum):
    FULL_ACCESS = 0  # "Полный доступ"
    STAFF_LIST_EDITOR = 1  # "Редакторование штатного расписания"
    PERSONAL_PROFILE_EDITOR = 2  # "Редактирование личных дел"
    VIEW_ALL_EMPLOYEES = 3  # Просмотр всех сотрудников Службы
    VIEW_ALL_EMPLOYEES_BY_DEPARTMENT = 12  # "Просмотр всех сотрудников Департамента"


class PermissionType(NamedModel):
    __tablename__ = "hr_erp_permission_types"

    sequence_id = Column(Integer, nullable=True)
    permissions = relationship(
        "Permission", back_populates="type", cascade="all,delete"
    )


class Permission(Model):
    __tablename__ = "hr_erp_permissions"

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    user = relationship("User", back_populates="permissions")

    staff_unit_id = Column(String(), ForeignKey("hr_erp_staff_units.id"))
    staff_units = relationship("StaffUnit", back_populates="permissions")

    type_id = Column(String(), ForeignKey("hr_erp_permission_types.id"))
    type = relationship("PermissionType", back_populates="permissions")
