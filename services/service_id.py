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


service_id_service = ServiceIDService(ServiceID)
