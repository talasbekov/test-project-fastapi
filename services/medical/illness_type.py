from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import IllnessType
from schemas import IllnessTypeCreate, IllnessTypeUpdate, IllnessTypeRead
from services.base import ServiceBase

class IllnessTypeService(ServiceBase[IllnessType, IllnessTypeCreate, IllnessTypeUpdate]):
    pass


illness_type_service = IllnessTypeService(IllnessType)
