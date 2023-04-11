from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import MilitaryUnit
from schemas import MilitaryUnitCreate, MilitaryUnitUpdate
from .base import ServiceBase


class MilitaryUnitService(ServiceBase[MilitaryUnit, MilitaryUnitCreate, MilitaryUnitUpdate]):
    pass


military_unit_service = MilitaryUnitService(MilitaryUnit)
