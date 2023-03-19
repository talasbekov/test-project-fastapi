from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import DrivingLicense
from schemas import (DrivingLicenseCreate, DrivingLicenseUpdate)
from services.base import ServiceBase


class DrivingLicenseService(ServiceBase[DrivingLicense, DrivingLicenseCreate, DrivingLicenseUpdate]):

    def get_by_id(self, db: Session, id: str):
        driving_licence = super().get(db, id)
        if driving_licence is None:
            raise NotFoundException(detail=f"DrivingLicense with id: {id} is not found!")
        return driving_licence


driving_license_service = DrivingLicenseService(DrivingLicense)
