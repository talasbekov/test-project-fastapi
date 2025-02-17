from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Nationality
from schemas import NationalityCreate, NationalityUpdate, NationalityRead
from services.base import ServiceBase

class NationalityService(ServiceBase[Nationality, NationalityCreate, NationalityUpdate]):
    pass


nationality_service = NationalityService(Nationality)
