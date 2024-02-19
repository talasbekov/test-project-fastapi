from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import BiographicInfo
from schemas import BiographicInfoCreate, BiographicInfoUpdate
from services.base import ServiceBase


class BiographicInfoService(
        ServiceBase[BiographicInfo, BiographicInfoCreate, BiographicInfoUpdate]):

    def get_by_id(self, db: Session, id: str):
        biographic_info = super().get(db, id)
        if biographic_info is None:
            raise NotFoundException(
                detail=f"BiographicInfo with id: {id} is not found!")
        return biographic_info

    def get_by_profile_id(self, db: Session, id: str):
        biographic_info = db.query(self.model).filter(
            self.model.profile_id == id).first()
        if not biographic_info:
            raise NotFoundException(
                detail=f"Biographic info with id: {id} is not found!")
        return biographic_info


biographic_info_service = BiographicInfoService(BiographicInfo)
