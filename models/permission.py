import enum

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from models import NamedModel, Model

class PermissionEnum(str, enum.Enum):
    FULL_ACCESS = "Полный доступ"
    STAFF_LIST_EDITOR = "Редакторование штатного расписания"
    PERSONAL_PROFILE_EDITOR = "Редактирование личных дел"
    VIEW_ALL_EMPLOYEES = "Просмотр сотрудников"
    VACANCY_MANAGEMENT = "Управление вакансими"
    VIEW_ALL_EMPLOYEES_BY_DEPARTMENT = "Просмотр сотрудников по подразделению"
    
class PermissionTypeEnum(str, enum.Enum):
    STAFF_LIST_EDITOR = 1
    PERSONAL_PROFILE_EDITOR = 2
    VIEW_ALL_EMPLOYEES = 3
    VACANCY_MANAGEMENT = 4
    VIEW_STAFF_LIST = 5
    ADMIN_PANEL = 7
    BSP_EDITOR = 8
    SURVEY_EDITOR = 9
    PSYCH_CHARACTERISTIC_EDITOR = 10
    POLIGRAPH_EDITOR = 11
    VIEW_ALL_EMPLOYEES_BY_DEPARTMENT = 12
    VIEW_SERVICE_CHARACTERISTICS = 13
    VIEW_POLIGRAPH = 14
    VIEW_SPEC_INSPECTIONS = 15
    VIEW_ATTESTATION = 16
    VIEW_UD = 17
    VIEW_DISP_UCHET = 18
    VIEW_LEAVES = 19
    VIEW_MEDICAL_LISTS = 20
    VIEW_VIOLATIONS = 21
    VIEW_PSYCH_CHARACTERISTICS = 22
    VIEW_FAMILY = 23
    VIEW_FAMILY_ADDITIONAL = 24

class PermissionType(NamedModel):
    __tablename__ = "hr_erp_permission_types"
    sequence_id = Column(Integer)
    permissions = relationship(
        "Permission",
        back_populates="type",
        cascade="all,delete")


class Permission(Model):
    __tablename__ = "hr_erp_permissions"

    user_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"))
    user = relationship("User", back_populates = 'permissions')
    type_id = Column(String(),
                     ForeignKey("hr_erp_permission_types.id"))
    type = relationship(
        "PermissionType",
        back_populates="permissions")
    