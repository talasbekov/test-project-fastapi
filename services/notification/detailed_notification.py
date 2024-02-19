import json

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models import Notification, SocketSession
from schemas import DetailedNotificationRead, DetailedNotificationCreate, DetailedNotificationUpdate
from services import ServiceBase
from typing import Union, Dict, Any
from models import DetailedNotification

class DetailedNotificationService(
        ServiceBase[DetailedNotification, DetailedNotificationCreate, DetailedNotificationUpdate]):
    def get_receiveds_by_user_id(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 10):
        return (
            db.query(self.model)
            .filter(self.model.receiver_id == user_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
    def get_multi(
        self, db: Session, user_id: str, skip: int = 0, limit: int = 100
    ):
        notifications = (
            db.query(self.model)
            # .filter(self.model.receiver_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        for notification in notifications:
            if notification.hr_document_id is not None:
                if isinstance(notification.hr_document.properties, str):
                    notification.hr_document.properties = json.loads(notification.hr_document.properties)
                if isinstance(notification.hr_document.document_template.properties, str):
                    notification.hr_document.document_template.properties = json.loads(notification.hr_document.document_template.properties)
                if isinstance(notification.hr_document.document_template.actions, str):
                    notification.hr_document.document_template.actions= json.loads(notification.hr_document.document_template.actions)
                if isinstance(notification.hr_document.document_template.description, str):
                    notification.hr_document.document_template.description= json.loads(notification.hr_document.document_template.description)
        notifications_count = (
            db.query(self.model)
            .filter(self.model.receiver_id == user_id)
            .count()
        )
        return {"total": notifications_count, "objects": notifications}
    
    def create(self, db: Session,
               body: Union[DetailedNotificationCreate, Dict[str, Any]]):
        body = jsonable_encoder(body)
        notification = DetailedNotification(**body) 
        db.add(notification)
        db.commit()
        if notification.hr_document_id is not None:
            if isinstance(notification.hr_document.properties, str):
                notification.hr_document.properties = json.loads(notification.hr_document.properties)
            if isinstance(notification.hr_document.document_template.properties, str):
                notification.hr_document.document_template.properties = json.loads(notification.hr_document.document_template.properties)
            if isinstance(notification.hr_document.document_template.actions, str):
                notification.hr_document.document_template.actions= json.loads(notification.hr_document.document_template.actions)
            if isinstance(notification.hr_document.document_template.description, str):
                notification.hr_document.document_template.description= json.loads(notification.hr_document.document_template.description)
        return notification
    
    def remove_document_notification(self, db: Session, document_id: str, user_id: str):
        notification = (
            db.query(self.model)
            .filter(self.model.hr_document_id == document_id,
                    self.model.receiver_id == user_id)
            .first()
        )
        if notification is None:
            return
        db.delete(notification)
        db.commit()

detailed_notification_service = DetailedNotificationService(DetailedNotification)
