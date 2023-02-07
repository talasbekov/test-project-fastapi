from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase
from models import Group
from schemas import GroupCreate, GroupUpdate, GroupRead

from exceptions import NotFoundException


class GroupService(ServiceBase[Group, GroupCreate, GroupUpdate]):
    
    def get_by_id(self, db: Session, id: str):
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(f"Group with id: {id} is not found!")
        return group

group_service = GroupService(Group)
