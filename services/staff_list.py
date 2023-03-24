import uuid

from sqlalchemy.orm import Session

from exceptions import NotFoundException, NotSupportedException
from models import (
    DocumentStaffFunction,
    ServiceStaffFunction,
    StaffDivision,
    StaffList,
    StaffUnit,
)
from schemas import (
    StaffListCreate,
    StaffListUpdate,
    StaffListUserCreate,
)
from services import (
    ServiceBase,
    archive_staff_division_service,
    archive_staff_function_service,
    archive_staff_unit_service,
    document_archive_staff_function_service,
    service_archive_staff_function_service,
    staff_division_service,
    document_archive_staff_function_type_service,
    service_archive_staff_function_type_service,
    document_staff_function_type_service,
    service_staff_function_type_service,
)

options = {
    DocumentStaffFunction.__mapper_args__['polymorphic_identity']: {
        "service": document_archive_staff_function_service,
        "type": document_archive_staff_function_type_service,
        "type_id": "role_id",
        "origin": document_staff_function_type_service,
    },
    ServiceStaffFunction.__mapper_args__['polymorphic_identity']: {
        "service": service_archive_staff_function_service,
        "type": service_archive_staff_function_type_service,
        "type_id": "type_id",
        "origin": service_staff_function_type_service,
    },
}


class StaffListService(ServiceBase[StaffList,StaffListCreate,StaffListUpdate]):

    def get_by_id(self, db: Session, id: str):
        staff_list = super().get(db,id)
        if staff_list is None:
            raise NotFoundException(detail="Staff list is not found!")
        return staff_list

    def create_by_user_id(self,db: Session, user_id: uuid.UUID, obj_in: StaffListUserCreate):

        create_staff_list = StaffListCreate(
            name = obj_in.name,
            status="IN PROGRESS",
            user_id=user_id
        )
        staff_list = super().create(db, create_staff_list)
        staff_divisions = staff_division_service.get_departments(db, 0, 100)
        for staff_division in staff_divisions:
            self._create_archive_staff_division(db, staff_division, staff_list.id, None)

        db.add(staff_list)
        db.flush()
        return staff_list

    def _create_archive_staff_division(self, db: Session, staff_division: StaffDivision, staff_list_id: uuid.UUID, parent_group_id: uuid.UUID):

        archive_division = archive_staff_division_service.create_based_on_existing_staff_division(db, staff_division, staff_list_id, parent_group_id)

        if staff_division.children:
            for child in staff_division.children:
                child_archive_staff_division = self._create_archive_staff_division(db, child, staff_list_id, archive_division.id)
                archive_division.children.append(child_archive_staff_division)

        if staff_division.staff_units:
            for staff_unit in staff_division.staff_units:
                staff_unit: StaffUnit

                staff_unit_user_id = staff_unit.users[0].id if staff_unit.users else None
                staff_unit_actual_user_id = staff_unit.actual_users[0].id if staff_unit.actual_users else None

                archive_staff_unit = archive_staff_unit_service.create_based_on_existing_staff_unit(db, staff_unit, staff_unit_user_id, staff_unit_actual_user_id)

                if staff_unit.staff_functions:
                    for staff_function in staff_unit.staff_functions:
                        if not archive_staff_function_service.exists_by_origin_id(db, staff_function.id):
                            service = options.get(staff_function.discriminator)
                            if service is None:
                                raise NotSupportedException(detail="Staff function type is not supported!")
                            
                            type = service['type'].get_by_origin_id(db, staff_function.id)

                            if type is None:
                                print(service)
                                type = service['type'].create_based_on_existing_archive_staff_function_type(
                                    db,
                                    service['origin'].get_by_id(db, getattr(staff_function, service['type_id']))
                                )

                            archive_staff_function = service['service'].create_based_on_existing_archive_staff_function(
                                db,
                                staff_function,
                                type.id
                            )
                            
                            archive_staff_unit.staff_functions.append(archive_staff_function)

                archive_division.staff_units.append(archive_staff_unit)

        db.add(archive_division)
        db.flush()

        return archive_division

    def sign(self, db: Session, id: str):
        staff_divisions = db.query(StaffDivision).all()
        staff_list = self.get_by_id(db, id)
        staff_obj = staff_list.data 
        return None


staff_list_service = StaffListService(StaffList)
