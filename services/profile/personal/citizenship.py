from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Citizenship
from schemas import CitizenshipCreate, CitizenshipUpdate, CitizenshipRead
from services.base import ServiceBase

class CitizenshipService(ServiceBase[Citizenship, CitizenshipCreate, CitizenshipUpdate]):
    pass


citizenship_service = CitizenshipService(Citizenship)
