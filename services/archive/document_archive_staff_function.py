import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveDocumentStaffFunction, DocumentStaffFunction
from schemas import (
    ArchiveDocumentStaffFunctionCreate,
    ArchiveDocumentStaffFunctionUpdate,
    NewArchiveDocumentStaffFunctionCreate
)
from services import ServiceBase


class DocumentArchiveStaffFunction(
        ServiceBase[
            ArchiveDocumentStaffFunction, 
            ArchiveDocumentStaffFunctionCreate, 
            ArchiveDocumentStaffFunctionUpdate]):

    def get_by_id(self, db: Session, id: str):
        document_staff_function = super().get(db, id)
        if document_staff_function is None:
            raise NotFoundException(
                detail=f"DocumentArchiveStaffFunction with id: {id} is not found!")
        return document_staff_function

    def create_based_on_existing_archive_staff_function(
            self, 
            db: Session, 
            staff_function: DocumentStaffFunction, 
            role_id: uuid.UUID):
        return super().create(db, ArchiveDocumentStaffFunctionCreate(
            name=staff_function.name,
            nameKZ=staff_function.nameKZ,
            hours_per_week=staff_function.hours_per_week,
            role_id=role_id,
            jurisdiction_id=staff_function.jurisdiction_id,
            priority=staff_function.priority,
            origin_id=staff_function.id
        ))

    def create_archive_staff_function(
            self, 
            db: Session, 
            body: NewArchiveDocumentStaffFunctionCreate):
        return super().create(db, ArchiveDocumentStaffFunctionCreate(
            name=body.name,
            nameKZ=body.nameKZ,
            hours_per_week=body.hours_per_week,
            role_id=body.role_id,
            jurisdiction_id=body.jurisdiction_id,
            priority=body.priority,
            origin_id=None
        ))

    def update_archive_staff_function(
            self, 
            db: Session, 
            staff_function: DocumentStaffFunction, 
            body: NewArchiveDocumentStaffFunctionCreate):
        return super().update(db, 
                              db_obj=staff_function, 
                              obj_in=ArchiveDocumentStaffFunctionCreate(
            name=body.name,
            nameKZ=body.nameKZ,
            hours_per_week=body.hours_per_week,
            role_id=body.role_id,
            jurisdiction_id=body.jurisdiction_id,
            priority=body.priority,
            origin_id=None
        ))


document_archive_staff_function_service = DocumentArchiveStaffFunction(
    ArchiveDocumentStaffFunction)
