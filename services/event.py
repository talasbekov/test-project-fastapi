from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import Event
from schemas import EventCreate, EventRead, EventUpdate

from .base import ServiceBase


class EventService(ServiceBase[Event, EventCreate, EventUpdate]):
    
    def get_by_id(self, db: Session, id: str):
        event = super().get(db, id)
        if event is None:
            raise NotFoundException(detail=f"Event with id: {id} is not found!")
        return event


event_service = EventService(Event)
