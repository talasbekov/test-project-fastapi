from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ActivityType
from schemas import ActivityTypeCreate, ActivityTypeUpdate, ActivityTypeRead
from services.base import ServiceBase

class ActivityTypeService(ServiceBase[ActivityType, ActivityTypeCreate, ActivityTypeUpdate]):
    pass


activity_type_service = ActivityTypeService(ActivityType)
