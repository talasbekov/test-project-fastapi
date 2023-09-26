from models import BadgeType
from schemas import BadgeTypeCreate, BadgeTypeUpdate
from .base import ServiceBase


class BadgeTypeService(
        ServiceBase[BadgeType, BadgeTypeCreate, BadgeTypeUpdate]):
    pass


badge_type_service = BadgeTypeService(BadgeType)
