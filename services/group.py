from typing import List

from fastapi import HTTPException, status
from fastapi.logger import logger as log
from sqlalchemy.orm import Session

from exceptions import BadRequestException, NotFoundException
from models import Group
from schemas import GroupCreate, GroupRead, GroupUpdate

from .base import ServiceBase


class GroupService(ServiceBase[Group, GroupCreate, GroupUpdate]):

    def get_by_id(self, db: Session, id: str):
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(f"Group with id: {id} is not found!")
        return group

    def get_departments(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[Group]:
        return db.query(self.model).filter(
            Group.parent_group_id == None
        ).offset(skip).limit(limit).all()


    def change_parent_group(self,
            db: Session,
            id: str,
            new_parent_group_id: str
    ) -> GroupRead:
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(f"Group with id: {id} is not found!")

        parent_group = super().get(db, new_parent_group_id)
        if parent_group is None:
            raise BadRequestException(f"Parent group with id: {new_parent_group_id} is not found!")
        group.parent_group_id = new_parent_group_id
        db.add(group)
        db.flush()
        return group


group_service = GroupService(Group)
