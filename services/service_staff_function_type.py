from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ServiceFunctionType, ArchiveServiceFunctionType
from schemas import ServiceStaffFunctionTypeCreate, ServiceStaffFunctionTypeUpdate
from .archive.service_archive_staff_function_type import (
    service_archive_staff_function_type_service
)
from .base import ServiceBase


class ServiceFunctionTypeService(
        ServiceBase[ServiceFunctionType,
                    ServiceStaffFunctionTypeCreate,
                    ServiceStaffFunctionTypeUpdate]):

    def get_by_id(self, db: Session, id: str):
        if id is None:
            return None
        service_function_type = super().get(db, id)
        if service_function_type is None:
            raise NotFoundException(
                detail=f"ServiceFunctionType with id: {id} is not found!")
        return service_function_type

    def _update_from_archive(
            self,
            db,
            archive_staff_function_type: ArchiveServiceFunctionType):
        service_function_type = self.get_by_id(
            db, archive_staff_function_type.origin_id)

        res = super().update(
            db,
            db_obj=service_function_type,
            obj_in=ServiceStaffFunctionTypeUpdate(
                name=archive_staff_function_type.name,
                nameKZ=archive_staff_function_type.nameKZ,
            )
        )
        return res

    def _create_from_archive(
            self,
            db,
            archive_staff_function_type: ArchiveServiceFunctionType):
        res = super().create(
            db, ServiceStaffFunctionTypeCreate(
                name=archive_staff_function_type.name,
                nameKZ=archive_staff_function_type.nameKZ,
            )
        )
        return res

    def create_or_update_from_archive(
            self,
            db: Session,
            type_id: ArchiveServiceFunctionType):
        type = service_archive_staff_function_type_service.get_by_id(
            db, type_id)
        if type.origin_id is None:
            return self._create_from_archive(db,
                                             type)
        return self._update_from_archive(db,
                                         type)


service_staff_function_type_service = ServiceFunctionTypeService(
    ServiceFunctionType)
