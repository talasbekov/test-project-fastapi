from models import PenaltyType
from schemas import PenaltyTypeCreate, PenaltyTypeUpdate
from .base import ServiceBase


class PenaltyTypeService(ServiceBase[PenaltyType, PenaltyTypeCreate, PenaltyTypeUpdate]):
    pass

penalty_type_service = PenaltyTypeService(PenaltyType)
