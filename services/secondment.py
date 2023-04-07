import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Secondment, StaffDivision
from schemas import SecondmentRead, SecondmentCreate, SecondmentUpdate
from .base import ServiceBase
from services import staff_division_service
from utils import is_valid_uuid


class SecondmentService(ServiceBase[Secondment, SecondmentCreate, SecondmentUpdate]):

    def create_relation(self, db: Session, user_id: uuid.UUID, value):
        if is_valid_uuid(value):
            staff_division = staff_division_service.get_by_id(db, value)
            status = super().create(db, SecondmentCreate(user_id=user_id, staff_division_id=value, name=staff_division.name))
        else:
            status = super().create(db, SecondmentCreate(user_id=user_id, staff_division_id=None, name=value))
        return status
    
    def get_by_option(self, db: Session, skip: int, limit: int):
        pass



secondment_service = SecondmentService(Secondment)
