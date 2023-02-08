from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase
from models import Role
from schemas import RoleCreate, RoleUpdate, RoleRead

from exceptions import NotFoundException


class RoleService(ServiceBase[Role, RoleCreate, RoleUpdate]):

    def get_by_id(self, db: Session, id: str):
        role = super().get(db, id)
        if role is None:
            raise NotFoundException(detail=f"Role with id: {id} is not found!")
        return role


role_service = RoleService(Role)
