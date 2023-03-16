from sqlalchemy.orm import Session
from services import (ServiceBase, staff_division_service, archive_staff_division_service
                      , archive_staff_unit_service, staff_unit_service, archive_staff_function_service,
                      document_archive_staff_function_service,
                      service_archive_staff_function_service)

from exceptions import NotFoundException, NotSupportedException
from models import StaffList, StaffDivision, StaffUnit, DocumentStaffFunction, ServiceStaffFunction
from schemas import (StaffListCreate,StaffListRead,StaffListUpdate, 
                     ArchiveStaffDivisionCreate, ArchiveServiceStaffFunctionCreate, ArchiveStaffUnitCreate,
                     ArchiveStaffUnitCreateWithStaffFunctions)


options = {
    DocumentStaffFunction.__mapper_args__['polymorphic_identity']: document_archive_staff_function_service,
    ServiceStaffFunction.__mapper_args__['polymorphic_identity']: service_archive_staff_function_service,
}

class StaffListService(ServiceBase[StaffList,StaffListCreate,StaffListUpdate]):

    def get_by_id(self, db: Session, id: str):
        staff_list = super().get(db,id)
        if staff_list is None:
            raise NotFoundException(detail="Staff list is not found!")
        return staff_list
    
    def create_by_user_id(self,db: Session,user_id: str, obj_in: StaffListCreate):

        db_obj = obj_in.dict()
        db_obj['user_id'] = user_id
        staff_list = super().create(db,db_obj)
        staff_divisions = staff_list.archive_staff_divisions
        for staff_division in staff_divisions:
            self._create_archive_staff_division(db, staff_division, staff_list.id)
        
        return staff_list

    def _create_archive_staff_division(self,db: Session,staff_division: StaffDivision,staff_list_id: str):

        archive_division = ArchiveStaffDivisionCreate(
            parent_group_id=staff_division.parent_group_id,
            name=staff_division.name,
            description=staff_division.description,
            children = [],
            staff_units = []
        )
        
        if staff_division.children:
            for child in staff_division.children:

                child_archive_staff_division = self.archive_staff_function_create_archive_staff_division(db, child, staff_list_id)

                archive_division.children.append(child_archive_staff_division)

        if staff_division.staff_units:
            for staff_unit in staff_division.staff_units:
                archive_staff_unit = ArchiveStaffUnitCreate(
                    staff_unit_id = staff_unit.id,
                    staff_list_id = staff_list_id,
                    staff_functions = []
                )

                if staff_unit.staff_functions:
                    for staff_function in staff_unit.staff_functions:
                        if not archive_staff_function_service.exists_by_origin_id(db, staff_function.id):

                            serv = options.get(staff_function.discriminator)
                            if serv is None:
                                raise NotSupportedException(detail="Staff function type is not supported!")

                            archive_staff_function = serv.create_archive_staff_function(db, staff_function, staff_list_id)
                            archive_staff_unit.staff_functions.append(archive_staff_function)

                archive_staff_unit = archive_staff_unit_service.create(db,archive_staff_unit)
                archive_division.staff_units.append(archive_staff_unit)

        archive_division = archive_staff_division_service.create(db,archive_division)

        return archive_division


    def sign(self,db: Session, id: str):
        staff_divisions = db.query(StaffDivision).all()
        staff_list = self.get_by_id(db, id)
        staff_obj = staff_list.data 
        return None



staff_list_service = StaffListService(StaffList)
