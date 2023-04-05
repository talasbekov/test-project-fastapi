from sqlalchemy.orm import Session

from exceptions import NotFoundException, NotSupportedException
from models import History, RankHistory, StaffUnitHistory
from schemas import HistoryCreate, HistoryUpdate
from .base import ServiceBase

options = {
    'rank_history': RankHistory,
    'staff_unit_history': StaffUnitHistory,
}


class HistoryService(ServiceBase[History, HistoryCreate, HistoryUpdate]):
    def get_by_type(self, db: Session, type: str):
        return db.query(self.model).filter(self.model.type == type).first()

    def get_all_by_type(self, db: Session, type: str):
        return db.query(self.model).filter(self.model.type == type).all()
    def create(self, db: Session, obj_in: HistoryCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(detail=f'Type: {obj_in.type} is not supported!')
        obj_in = cls(**obj_in.dict())
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        return db_obj

history_service = HistoryService(History)
