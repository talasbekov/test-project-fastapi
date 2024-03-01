import enum

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import NamedModel, Model

class PermissionEnum(str, enum.Enum):
    FULL_ACCESS = "Полный доступ"
    STAFF_LIST_EDITOR = "Редакторование штатного расписания"
    PERSONAL_PROFILE_EDITOR = "Редактирование личных дел"


class PermissionType(NamedModel):
    __tablename__ = "hr_erp_permission_types"
    
    permissions = relationship(
        "Permission",
        back_populates="type",
        cascade="all,delete")


class Permission(Model):
    __tablename__ = "hr_erp_permissions"

    user_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"))
    user = relationship("User")
    type_id = Column(String(),
                     ForeignKey("hr_erp_permission_types.id"))
    type = relationship(
        "PermissionType",
        back_populates="permissions")