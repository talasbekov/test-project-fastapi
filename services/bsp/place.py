from models import Place
from schemas import PlaceCreate, PlaceUpdate
from services.base import ServiceBase


class PlaceService(ServiceBase[Place, PlaceCreate, PlaceUpdate]):
    pass

place_service = PlaceService(Place)
