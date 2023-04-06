from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ServiceID
from schemas import ServiceIDCreate, ServiceIDUpdate
from .base import ServiceBase


class ServiceIDService(ServiceBase[ServiceID, ServiceIDCreate, ServiceIDUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"ServiceID with id: {id} is not found!")
        return rank
    
    def get_by_user_id(self, db: Session, user_id: str):
        service_id = db.query(self.model).filter(self.model.user_id == user_id).first()
        return service_id

service_id_service = ServiceIDService(ServiceID)
