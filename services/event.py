from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase
from models import Event
from schemas import EventRead, EventCreate, EventUpdate

from exceptions import NotFoundException


class EventService(ServiceBase[Event, EventCreate, EventUpdate]):
    
    def get_by_id(self, db: Session, id: str):
        event = super().get(db, id)
        if event is None:
            raise NotFoundException(detail=f"Event with id: {id} is not found!")
        return event


event_service = EventService(Event)
