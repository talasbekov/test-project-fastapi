from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

from models import SocketSession
from schemas import NotificationCreate, NotificationUpdate
from services import ServiceBase


class SocketSessionService(
        ServiceBase[SocketSession, NotificationCreate, NotificationUpdate]):
        
    def register_connection(self, db: Session, user_id: str):
        session = SocketSession(user_id=user_id)
        db.add(session)
        db.commit()
        
    def delete_session(self, db: Session, user_id: str):
        session = db.query(SocketSession).get(user_id)
        db.delete(session)
        db.commit()
        return session
    
    def is_exist(self, db: Session, user_id: str):
        return db.query(exists().where(SocketSession.user_id == user_id)).scalar()


socket_session_service = SocketSessionService(SocketSession)
