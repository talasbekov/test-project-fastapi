from typing import List

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Permission, PermissionType
from schemas import PermissionCreate, PermissionUpdate
from services import staff_unit_service, user_service

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
        permissions = (
            db.query(self.model)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        count = db.query(self.model).count()
        return {"total": count, "objects": permissions}

    def get_permission_types(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(PermissionType).offset(skip).limit(limit).all()

    def has_permission(
        self, db: Session, user_id: str, role: str, permissions: list[int]
    ):
        staff_unit = staff_unit_service.get_by_id(db, role)
        user = user_service.get_by_id(db, user_id)

        # Получение всех permission_types, которые соответствуют списку permissions
        permission_types = (
            db.query(PermissionType)
            .filter(PermissionType.sequence_id.in_(permissions))
            .all()
        )

        # Проверка, что все permission_types из списка permissions найдены
        if len(permission_types) != len(permissions):
            raise NotFoundException(detail="One or more permission types not found!")

        # Проверка, что для каждого permission_type существует разрешение для данного пользователя и staff_unit
        for permission_type in permission_types:
            permission = (
                db.query(self.model)
                .filter(
                    self.model.type_id == permission_type.id,
                    self.model.user_id == user.id,
                    self.model.staff_unit_id == staff_unit.id,
                )
                .first()
            )
            # Если для любого из permission_types не найдено разрешение, возвращаем False
            if not permission:
                return False

        # Все разрешения найдены
        return True

    def get_permissions_by_user(self, db: Session, user_id: str):
        permissions = db.query(self.model).filter(self.model.user_id == user_id).all()
        return permissions


permission_service = PermissionService(Permission)
