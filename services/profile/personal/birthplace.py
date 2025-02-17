from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Birthplace
from schemas import BirthplaceCreate, BirthplaceUpdate, BirthplaceRead
from services.base import ServiceBase

class BirthplaceService(ServiceBase[Birthplace, BirthplaceCreate, BirthplaceUpdate]):
    pass


birthplace_service = BirthplaceService(Birthplace)
