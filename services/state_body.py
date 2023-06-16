import uuid

from sqlalchemy.orm import Session

from models import StateBody
from schemas import StateBodyCreate, StateBodyUpdate, StateBodyRead
from .base import ServiceBase


class StateBodyService(ServiceBase[StateBody, StateBodyCreate, StateBodyUpdate]):
    def get_by_option(self, 
                      db: Session, 
                      type: str, 
                      id: uuid.UUID, 
                      skip: int, 
                      limit: int):
        body = db.query(self.model).offset(skip).limit(limit).all()
        return [StateBodyRead.from_orm(i) for i in body]


state_body_service = StateBodyService(StateBody)
