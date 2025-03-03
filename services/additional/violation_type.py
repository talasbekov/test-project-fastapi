from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ViolationType
from schemas import ViolationTypeCreate, ViolationTypeUpdate, ViolationTypeRead
from services.base import ServiceBase

class ViolationTypeService(ServiceBase[ViolationType, ViolationTypeCreate, ViolationTypeUpdate]):
    pass


violation_type_service = ViolationTypeService(ViolationType)
