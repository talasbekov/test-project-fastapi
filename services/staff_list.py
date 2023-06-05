from typing import List, Optional
import uuid

from sqlalchemy.orm import Session, joinedload

from exceptions import NotFoundException, NotSupportedException
from models import (
    DocumentStaffFunction,
    ServiceStaffFunction,
    StaffDivision,
    StaffList,
    StaffUnit,
    ArchiveStaffDivision,
    User,
    HrDocument,
)
from schemas import (
    StaffListCreate,
    StaffListUpdate,
    StaffListUserCreate,
    StaffListStatusRead
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
    hr_document_template_service,
    position_service,
    archive_position_service,
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


class StaffListService(ServiceBase[StaffList, StaffListCreate, StaffListUpdate]):

    def get_by_id(self, db: Session, id: str):
        staff_list = super().get(db, id)
        if staff_list is None:
            raise NotFoundException(detail="Staff list is not found!")
        return staff_list

    def create_by_user_id(self, db: Session, user_id: uuid.UUID, obj_in: StaffListUserCreate):

        create_staff_list = StaffListCreate(
            name=obj_in.name,
            user_id=user_id
        )
        staff_list = super().create(db, create_staff_list)
        staff_divisions = staff_division_service.get_departments(db, 0, 100)
        for staff_division in staff_divisions:
            self._create_archive_staff_division(db, staff_division, staff_list.id, None)
        db.add(staff_list)
        db.flush()
        return staff_list

    def duplicate(self, db: Session, staff_list_id: uuid.UUID, user_id: uuid.UUID, obj_in: StaffListUserCreate):
        create_staff_list = StaffListCreate(
            name=obj_in.name,
            user_id=user_id
        )
        staff_list = super().create(db, create_staff_list)
        for archive_staff_division in db.query(ArchiveStaffDivision).filter(
                ArchiveStaffDivision.staff_list_id == staff_list_id):
            staff_division = staff_division_service.get_by_id(db, archive_staff_division.origin_id)
            self._create_archive_staff_division(db, staff_division, staff_list.id, None)

        db.add(staff_list)
        db.flush()
        return staff_list

    def _create_archive_staff_division(self, db: Session, staff_division: StaffDivision, staff_list_id: uuid.UUID,
                                       parent_group_id: Optional[uuid.UUID]):

        archive_division = archive_staff_division_service.create_based_on_existing_staff_division(db, staff_division,
                                                                                                  staff_list_id,
                                                                                                  parent_group_id)

        if staff_division.children:
            for child in staff_division.children:
                child_archive_staff_division = self._create_archive_staff_division(db, child, staff_list_id,
                                                                                   archive_division.id)
                archive_division.children.append(child_archive_staff_division)

        is_leader_needed = False
        leader_id = None
        if staff_division.leader_id is not None:
            is_leader_needed = True

        positions = position_service.get_multi(db, 0, 100)
        for position in positions:
            archive_position_service.create_based_on_existing_position(db,
                                                                       position.name,
                                                                       position.nameKZ,
                                                                       position.category_code,
                                                                       position.max_rank_id,
                                                                       position.id)
        if staff_division.staff_units:
            for staff_unit in staff_division.staff_units:
                staff_unit: StaffUnit

                staff_unit_user_id = staff_unit.users[0].id if staff_unit.users else None
                staff_unit_actual_user_id = staff_unit.actual_users[0].id if staff_unit.actual_users else None
                staff_unit_user_replacing = staff_unit.user_replacing_id
                staff_unit_form = getattr(staff_unit, "form ", None)

                archive_staff_unit = archive_staff_unit_service.create_based_on_existing_staff_unit(db, staff_unit,
                                                                                                    staff_unit_user_id,
                                                                                                    staff_unit_form,
                                                                                                    staff_unit_actual_user_id,
                                                                                                    staff_unit_user_replacing,
                                                                                                    archive_division)

                if is_leader_needed:
                    if staff_division.leader_id == staff_unit.id:
                        leader_id = archive_staff_unit.id

                if staff_unit.staff_functions:
                    for staff_function in staff_unit.staff_functions:
                        if not archive_staff_function_service.exists_by_origin_id(db, staff_function.id):
                            service = options.get(staff_function.discriminator)
                            if service is None:
                                raise NotSupportedException(detail="Staff function type is not supported!")

                            type = service['type'].get_by_origin_id(db, staff_function.id)

                            if type is None:
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

        if is_leader_needed:
            archive_division.leader_id = leader_id

        db.add(archive_division)
        db.flush()

        return archive_division

    def get_super_doc_by_staff_list_id(
            self,
            db: Session,
            id: uuid.UUID
    ):
        hr_document_template = hr_document_template_service.get_staff_list(db=db)
        hr_document_template_id = hr_document_template.id
        hr_documents = db.query(HrDocument).filter(
            HrDocument.hr_document_template_id == hr_document_template_id
        )
        super_doc = None
        for hr_document in hr_documents:
            if str(id) == hr_document.properties['staff_list'].get('value'):
                super_doc = hr_document
        if super_doc is None:
            raise NotFoundException(detail="Hr document not found")
        return super_doc

    def get_drafts(self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''):
        staff_lists = (db.query(StaffList)
                       .join(User)
                       .options(joinedload(StaffList.user))
                       .filter(StaffList.is_signed == False,
                               StaffList.name.contains(filter))
                       .offset(skip)
                       .limit(limit)
                       .all())

        return [StaffListStatusRead.from_orm(staff_list) for staff_list in staff_lists]

    def get_signed(self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''):
        staff_lists = (db.query(StaffList)
                       .join(User)
                       .options(joinedload(StaffList.user))
                       .filter(StaffList.is_signed == True,
                               StaffList.name.contains(filter))
                       .offset(skip)
                       .limit(limit)
                       .all())
        signed_staff_lists = []
        for staff_list in staff_lists:
            super_doc = self.get_super_doc_by_staff_list_id(db, staff_list.id)
            status = super_doc.status
            reg_number = super_doc.reg_number
            signed_staff_list = StaffListStatusRead.from_orm(staff_list)
            signed_staff_list.status = {
                "name": status.name,
                "nameKZ": status.nameKZ,
            }
            signed_staff_list.reg_number = reg_number
            signed_staff_lists.append(signed_staff_list)

        return signed_staff_lists

    def update(self, db: Session, staff_list_id: uuid.UUID, body: StaffListUpdate):
        staff_list = self.get_by_id(db, staff_list_id)
        return super().update(
            db=db, db_obj=staff_list, obj_in=body
        )


staff_list_service = StaffListService(StaffList)
