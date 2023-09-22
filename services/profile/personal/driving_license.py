import json 

from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from exceptions.client import NotFoundException
from models import DrivingLicense
from schemas import (
    DrivingLicenseCreate,
    DrivingLicenseUpdate,
    DrivingLicenseLinkUpdate)
from services.base import ServiceBase


class DrivingLicenseService(
        ServiceBase[DrivingLicense, DrivingLicenseCreate, DrivingLicenseUpdate]):

    def get_by_id(self, db: Session, id: str):
        driving_licence = super().get(db, id)
        if driving_licence is None:
            raise NotFoundException(
                detail=f"DrivingLicense with id: {id} is not found!")
        driving_licence.category = eval(driving_licence.category)
        return driving_licence

    def update_document_link(self, db: Session, id: str,
                             body: DrivingLicenseLinkUpdate):
        license = self.get_by_id(db, id)
        license.document_link = body.document_link
        db.add(license)
        db.flush()
        
    def update(
        self,
        db: Session,
        *,
        db_obj: DrivingLicense,
        obj_in: DrivingLicenseUpdate
    ) -> DrivingLicense:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.flush()
        db_obj.category = eval(db_obj.category)
        return db_obj


driving_license_service = DrivingLicenseService(DrivingLicense)
