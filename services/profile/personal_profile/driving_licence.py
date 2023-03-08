from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import DrivingLicence
from schemas import DrivingLicenceCreate, DrivingLicenceUpdate, DrivingLicenceRead

from services.base import ServiceBase


class DrivingLicenceService(ServiceBase[DrivingLicence, DrivingLicenceCreate, DrivingLicenceUpdate]):

    def get_by_id(self, db: Session, id: str):
        driving_licence = super().get(db, id)
        if driving_licence is None:
            raise NotFoundException(detail=f"DrivingLicence with id: {id} is not found!")
        return driving_licence


driving_licence_service = DrivingLicenceService(DrivingLicence)
