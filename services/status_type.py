from models import StatusType
from schemas import StatusTypeCreate, StatusTypeUpdate
from .base import ServiceBase


class StatusTypeService(
        ServiceBase[StatusType, StatusTypeCreate, StatusTypeUpdate]):
    pass


status_type_service = StatusTypeService(StatusType)
