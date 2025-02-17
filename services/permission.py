from typing import List

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Permission, PermissionType, PermissionEnum, User
from schemas import PermissionCreate, PermissionUpdate, PermissionRead

from .base import ServiceBase


class PermissionService(ServiceBase[Permission, PermissionCreate, PermissionUpdate]):

    def get_by_id(self, db: Session, id: str):
        permission = super().get(db, id)
        if permission is None:
            raise NotFoundException(detail=f"Permission with id: {id} is not found!")
        return permission
    
    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Permission]:
        permissions = db.query(self.model).order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()
        count = db.query(self.model).count()
        return {"total": count, "objects": permissions}

    def get_permission_types(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(PermissionType).offset(skip).limit(limit).all()
    
    def has_permission(self, db: Session, user_id: str, permission_type: PermissionEnum):
        permission_type = db.query(PermissionType).filter(PermissionType.name==permission_type).first()
        if permission_type is None:
            raise NotFoundException(detail=f"Permission type with given name is not found!")
        permission = db.query(self.model).filter(self.model.type_id==permission_type.id).first()
        return permission is not None
        
    def get_permissions_by_user(self, db: Session, user_id: str):
        permissions = db.query(self.model).filter(self.model.user_id==user_id).all()
        return permissions

permission_service = PermissionService(Permission)
