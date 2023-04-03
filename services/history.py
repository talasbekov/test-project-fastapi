from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import History
from schemas import HistoryCreate, HistoryUpdate
from .base import ServiceBase


class HistoryService(ServiceBase[History, HistoryCreate, HistoryUpdate]):
    def get_by_type(self, db: Session, type: str):
        return db.query(self.model).filter(self.model.type == type).first()

    def get_all_by_type(self, db: Session, type: str):
        return db.query(self.model).filter(self.model.type == type).all()
    

history_service = HistoryService(History)
