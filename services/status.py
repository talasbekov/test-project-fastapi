import uuid
from datetime import datetime
from typing import List

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import (Status, StatusHistory, StatusType,
                    StaffDivision, User, StaffUnit, StatusEnum)
from schemas import StatusRead, StatusCreate, StatusUpdate, StatusTypeRead
from services import user_service
from .base import ServiceBase


class StatusService(ServiceBase[Status, StatusCreate, StatusUpdate]):

    def get_by_id(self, db: Session, id: str) -> Status:
        status = super().get(db, id)
        if status is None:
            raise NotFoundException(detail="User is not found!")
        return status

    def get_status_by_name(self, db: Session, name: str):
        status = db.query(StatusType).filter(StatusType.name == name).first()
        return status

    def get_users_from_status_by_id(self, db: Session, id: str):
        users = db.query(Status).filter(Status.type_id == id).all()
        return users

    def create_relation(self, db: Session, user_id: str, type_id: str):
        status = super().create(db, StatusCreate(type_id=type_id, user_id=user_id))
        return status

    def get_object(self, db: Session, id: str, type: str):
        if type == 'write':
            return db.query(StatusType).filter(StatusType.id == id).first()
        else:
            return db.query(Status).filter(Status.id == id).first().type

    def get_by_option(self,
                      db: Session,
                      type: str,
                      id: str,
                      skip: int,
                      limit: int):
        user = user_service.get_by_id(db, id)
        if type == 'write':
            return [StatusTypeRead.from_orm(status).dict() for status in
                    db.query(StatusType).offset(skip).limit(limit).all()]
        else:
            return [StatusRead.from_orm(status).dict()
                    for status in user.statuses]

    def stop_relation(self, db: Session, user_id: str,
                      status_id: str):
        history = (db.query(StatusHistory)
                   .filter(StatusHistory.status_id == status_id)
                   .order_by(StatusHistory.created_at.desc()).first())
        if history is None:
            raise NotFoundException(
                detail=f"Status with id: {status_id} is not found!")
        history.date_to = datetime.now()
        db.add(history)
        db.flush()
        return history

    def exists_relation(self, db: Session, user_id: str,
                        badge_type_id: str):
        return (
            db.query(Status)
            .filter(Status.user_id == user_id)
            .filter(Status.type_id == badge_type_id)
            .join(StatusHistory)
            .filter(or_(StatusHistory.date_to == None,
                        StatusHistory.date_to > datetime.now()))
            .first()
        ) is not None

    def get_by_name(self, db: Session, name: str):
        return (db.query(StatusType)
                .filter(func.lower(StatusType.name)
                .contains(name.lower()))
                .all())

    def get_active_status_of_user(self,
                                  db: Session,
                                  user_id: str,
                                  status_name: str):
        return (
            db.query(StatusHistory)
            .filter(
                or_(
                    StatusHistory.date_to == None,
                    StatusHistory.date_to > datetime.now(),
                ),
            )
            .join(Status)
            .filter(Status.user_id == user_id)
            .join(StatusType)
            .filter(func.lower(StatusType.name).contains(status_name.lower()))
            .order_by(StatusHistory.date_to.desc())
            .all()
        )

    # Получаем количество отсуствующих по каждому статусу
    # в зависимости от подразделения:
    # на больничном, по рапорту, в отпуске, в командировке
    def get_users_recursive_by_status(
            self, db: Session, department: StaffDivision, status: str
    ):
        users = db.query(User) \
            .join(Status) \
            .join(StatusType) \
            .join(StaffUnit, User.staff_unit_id == StaffUnit.id) \
            .join(StaffDivision, StaffUnit.staff_division_id == StaffDivision.id) \
            .filter(
            StatusType.name == status,
            User.staff_unit_id == StaffUnit.id,
            StaffUnit.staff_division_id == department.id
        ).all()

        # Recursively call this function for each child division
        for child in department.children:
            users.extend(self.get_users_recursive_by_status(db, child, status))

        users_with_status: List[User] = []
        for user in users:
            users_with_status.append(user)

        state_by_status = [name for name in users_with_status]
        return state_by_status

    ALL_STATUSES = [
        StatusEnum.ANNUAL_LEAVE.value,
        StatusEnum.VACATION.value,
        StatusEnum.BUSINESS_TRIP.value,
        StatusEnum.SICK_LEAVE.value,
        StatusEnum.MATERNITY_LEAVE.value
    ]

    def get_count_all_users_recursive_by_status(
            self, db: Session, department: StaffDivision
    ):
        users = db.query(User) \
            .join(Status) \
            .join(StatusType) \
            .join(StaffUnit, User.staff_unit_id == StaffUnit.id) \
            .join(StaffDivision, StaffUnit.staff_division_id == StaffDivision.id) \
            .filter(
            StatusType.name.in_(self.ALL_STATUSES),
            User.staff_unit_id == StaffUnit.id,
            StaffUnit.staff_division_id == department.id
        ).all()

        # Recursively call this function for each child division
        for child in department.children:
            users.extend(self.get_count_all_users_recursive_by_status(db, child))

        users_with_status: List[User] = []
        
        if users is None:
            return 0
        
        for user in users:
            users_with_status.append(user)

        state_by_status = [first_name for first_name in users_with_status]
        return state_by_status


status_service = StatusService(Status)
