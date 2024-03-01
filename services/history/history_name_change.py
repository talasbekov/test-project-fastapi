from sqlalchemy.orm import Session

from models import NameChange
from schemas import HistoryNameChangeCreate, HistoryNameChangeUpdate
from services import ServiceBase


class NameChangeService(
        ServiceBase[NameChange, HistoryNameChangeCreate, HistoryNameChangeUpdate]):

    def get_all_by_user_id(self, db: Session, user_id: str):
        return db.query(self.model).filter(self.model.user_id == user_id).all()


history_name_change_service = NameChangeService(NameChange)
