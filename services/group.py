from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase
from models import Group
from schemas import GroupCreate, GroupUpdate, GroupRead

from exceptions import NotFoundException, BadRequestException


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
        return db.query(Group).filter(
            Group.parent_group_id == None
        ).offset(skip).limit(limit).all()


    def change_parent_group(self,
            db: Session,
            id: str,
            body: GroupUpdate
    ) -> GroupRead:
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(f"Group with id: {id} is not found!")

        if body.parent_group_id == None:
            raise BadRequestException("Parent group id should be no empty")
        group.parent_group_id = body.parent_group_id
        db.add(group)
        db.commit()
        db.refresh(group)
        return group


group_service = GroupService(Group)
