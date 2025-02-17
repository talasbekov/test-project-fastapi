from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Position, PositionType
from schemas import PositionCreate
from services import ServiceBase


# class PositionTypeService(ServiceBase[PositionType, PositionCreate]):
#     pass

# position_type_service = PositionTypeService(PositionType)