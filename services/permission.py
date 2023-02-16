from sqlalchemy.orm import Session

from .base import ServiceBase

from models import Permission
from schemas import PermissionCreate, PermissionUpdate
from exceptions.client import NotFoundException


class PermissionService(ServiceBase[Permission, PermissionCreate, PermissionUpdate]):
    def get_by_id(self, db: Session, id: str) -> Permission:
        permission = super().get(db, id)
        if permission is None:
            raise NotFoundException(detail="Permission is not found!")
        return permission


permission_service = PermissionService(Permission)
