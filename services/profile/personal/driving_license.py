import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import DrivingLicense
from schemas import (DrivingLicenseCreate, DrivingLicenseUpdate, DrivingLicenseLinkUpdate)
from services.base import ServiceBase


class DrivingLicenseService(ServiceBase[DrivingLicense, DrivingLicenseCreate, DrivingLicenseUpdate]):

    def get_by_id(self, db: Session, id: str):
        driving_licence = super().get(db, id)
        if driving_licence is None:
            raise NotFoundException(detail=f"DrivingLicense with id: {id} is not found!")
        return driving_licence
    
    def update_document_link(self, db: Session, id: uuid.UUID, body: DrivingLicenseLinkUpdate):
        license = self.get_by_id(db, id)
        license.document_link = body.document_link
        db.add(license)
        db.flush()


driving_license_service = DrivingLicenseService(DrivingLicense)
