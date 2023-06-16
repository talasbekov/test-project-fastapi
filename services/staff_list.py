import datetime
from typing import Optional
import uuid

from sqlalchemy import desc
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
    ArchiveStaffUnit,
    ArchiveDocumentStaffFunction,
    StaffListStatusEnum,
)
from schemas import (
    StaffListCreate,
    StaffListUpdate,
    StaffListUserCreate,
    StaffListStatusRead,
    HrVacancyUpdate,
)
from services import (
    ServiceBase,
    archive_staff_division_service,
    archive_staff_unit_service,
    document_archive_staff_function_service,
    service_archive_staff_function_service,
    staff_division_service,
    document_archive_staff_function_type_service,
    service_archive_staff_function_type_service,
    document_staff_function_type_service,
    service_staff_function_type_service,
    hr_document_template_service,
    staff_unit_service,
    service_staff_function_service,
    hr_vacancy_service,
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

    def create_by_user_id(self, db: Session, user_id: uuid.UUID, obj_in: StaffListUserCreate, current_user_role_id: str):

        create_staff_list = StaffListCreate(
            name=obj_in.name,
            user_id=user_id
        )
        staff_list = super().create(db, create_staff_list)
        staff_divisions = staff_division_service.get_all_except_special(
            db, 0, 100)
        for staff_division in staff_divisions:
            self._create_archive_staff_division(
                db, staff_division, staff_list.id, None, current_user_role_id)

        staff_list.status = StaffListStatusEnum.IN_PROGRESS.value
        db.add(staff_list)
        db.flush()
        return staff_list

    def duplicate(self, db: Session, staff_list_id: uuid.UUID, user_id: uuid.UUID, obj_in: StaffListUserCreate, current_user_role_id: str):
        create_staff_list = StaffListCreate(
            name=obj_in.name,
            user_id=user_id
        )
        staff_list = super().create(db, create_staff_list)
        for archive_staff_division in db.query(ArchiveStaffDivision).filter(
                ArchiveStaffDivision.staff_list_id == staff_list_id):
            staff_division = staff_division_service.get_by_id(
                db, archive_staff_division.origin_id)
            self._create_archive_staff_division(
                db, staff_division, staff_list.id, None, current_user_role_id)

        db.add(staff_list)
        db.flush()
        return staff_list

    async def apply_staff_list(
        self,
        db: Session,
        staff_list_id: uuid.UUID,
        signed_by: str,
        document_creation_date: datetime.date,
        current_user_id: uuid.UUID,
        current_user_role_id: uuid.UUID
    ):
        staff_list = self.get_by_id(db, staff_list_id)

        staff_division_service.make_all_inactive(db)
        exclude_staff_division_ids = [
            i.id for i in staff_division_service.get_excluded_staff_divisions(db)]
        staff_unit_service.make_all_inactive(db, exclude_staff_division_ids)
        service_staff_function_service.make_all_inactive(db)

        staff_divisions: list[ArchiveStaffDivision] = (
            archive_staff_division_service.get_departments(
                db, staff_list_id, 0, 100)
        )
        new_staff_divisions = []
        for staff_division in staff_divisions:
            new_staff_division = self._create_staff_division(
                db, staff_division, None, current_user_role_id)
            new_staff_divisions.append(new_staff_division)

        staff_list.document_signed_by = signed_by
        staff_list.document_signed_at = document_creation_date
        staff_list.status = StaffListStatusEnum.APPROVED.value
        staff_list.is_signed = True

        staff_unit_service.delete_all_inactive(db)
        staff_division_service.delete_all_inactive(db)
        service_staff_function_service.delete_all_inactive(db)
        db.add(staff_list)
        db.flush()
        await self.create_disposition_doc_by_staff_list_id(db, staff_list_id, current_user_id, current_user_role_id)
        return staff_list

    def _create_staff_division(self, db: Session,
                               staff_division: ArchiveStaffDivision,
                               parent_id: Optional[uuid.UUID],
                               current_user_role_id: uuid.UUID,
                               ) -> StaffDivision:
        is_leader_needed = None
        leader_id = None
        parent = archive_staff_division_service.get(db,
                                                    staff_division.parent_group_id)
        new_staff_division = staff_division_service.create_or_update_from_archive(
            db,
            staff_division,
            parent.origin_id if parent else None,
            None
        )

        if staff_division.children:
            for child in staff_division.children:
                child_staff_division = self._create_staff_division(
                    db,
                    child,
                    new_staff_division.id,
                    current_user_role_id
                )
                new_staff_division.children.append(child_staff_division)
        staff_division.origin_id = new_staff_division.id

        if staff_division.leader_id is not None:
            is_leader_needed = True
        staff_units: list[ArchiveStaffUnit] = staff_division.staff_units

        for staff_unit in staff_units:
            new_staff_unit = staff_unit_service.create_or_update_from_archive(
                db, staff_unit, new_staff_division.id)
            if is_leader_needed and staff_unit.id == staff_division.leader_id:
                leader_id = new_staff_unit.id
            staff_unit.origin_id = new_staff_unit.id
            new_staff_unit = self._create_and_add_functions_to_new_unit(db,
                                                                        staff_unit,
                                                                        new_staff_unit)
            db.add(new_staff_unit)
            db.add(staff_unit)
            db.flush()
            hr_vacancy = hr_vacancy_service.get_by_archieve_staff_unit(db, staff_unit.id)
            if hr_vacancy:
                body = HrVacancyUpdate()
                body.staff_unit_id = new_staff_unit.id
                body.is_active = None
                body.hr_vacancy_requirements_ids = None

                hr_vacancy_service.update(db, hr_vacancy, body, current_user_role_id)

        new_staff_division.leader_id = leader_id
        db.add(new_staff_division)
        db.add(staff_division)
        db.flush()

        return new_staff_division

    def _create_and_add_functions_to_new_unit(self, db, archive_staff_unit, new_staff_unit):
        archive_staff_functions = archive_staff_unit.staff_functions
        for arhive_staff_function in archive_staff_functions:
            if isinstance(arhive_staff_function, ArchiveDocumentStaffFunction):
                continue

            new_staff_function_type = None
            if arhive_staff_function.type_id is not None:
                new_staff_function_type = service_staff_function_type_service.create_or_update_from_archive(
                    db, arhive_staff_function.type_id)

            new_staff_function = service_staff_function_service.create_or_update_from_archive(
                db, arhive_staff_function, getattr(new_staff_function_type, 'id', None))

            arhive_staff_function.origin_id = new_staff_function.id
            new_staff_unit.staff_functions.append(new_staff_function)
            db.add(new_staff_function)
            db.add(arhive_staff_function)
        return new_staff_unit

    def _create_archive_staff_division(self, db: Session, staff_division: StaffDivision, staff_list_id: uuid.UUID,
                                       parent_group_id: Optional[uuid.UUID], current_user_role_id: str):

        archive_division = archive_staff_division_service.create_based_on_existing_staff_division(db, staff_division,
                                                                                                  staff_list_id,
                                                                                                  parent_group_id)

        if staff_division.children:
            for child in staff_division.children:
                child_archive_staff_division = self._create_archive_staff_division(db, child, staff_list_id,
                                                                                   archive_division.id, current_user_role_id)
                archive_division.children.append(child_archive_staff_division)

        is_leader_needed = False
        leader_id = None
        if staff_division.leader_id is not None:
            is_leader_needed = True

        if staff_division.staff_units:
            for staff_unit in staff_division.staff_units:
                staff_unit: StaffUnit

                staff_unit_user_id = staff_unit.users[0].id if staff_unit.users else None
                staff_unit_actual_user_id = staff_unit.actual_users[
                    0].id if staff_unit.actual_users else None
                staff_unit_user_replacing = staff_unit.user_replacing_id
                staff_unit_position = staff_unit.position_id

                archive_staff_unit = archive_staff_unit_service.create_based_on_existing_staff_unit(db, staff_unit,
                                                                                                    staff_unit_user_id,
                                                                                                    staff_unit_position,
                                                                                                    staff_unit_actual_user_id,
                                                                                                    staff_unit_user_replacing,
                                                                                                    archive_division)

                if is_leader_needed:
                    if staff_division.leader_id == staff_unit.id:
                        leader_id = archive_staff_unit.id

                if staff_unit.staff_functions:
                    for staff_function in staff_unit.staff_functions:
                        service = options.get(staff_function.discriminator)
                        if isinstance(staff_function, ServiceStaffFunction):
                            print(staff_function)
                        if isinstance(staff_function, DocumentStaffFunction):
                            print('Anime')
                        if service is None:
                            raise NotSupportedException(
                                detail="Staff function type is not supported!")
                        type = service['type'].create_based_on_existing_archive_staff_function_type(
                            db,
                            service['origin'].get_by_id(db, getattr(
                                staff_function, service['type_id']))
                        )

                        archive_staff_function = service['service'].create_based_on_existing_archive_staff_function(
                            db,
                            staff_function,
                            type.id if type else None
                        )

                        archive_staff_unit.staff_functions.append(
                            archive_staff_function)
                db.add(archive_staff_unit)
                db.flush()
                hr_vacancy = hr_vacancy_service.get_by_staff_unit(
                    db, staff_unit.id)

                if hr_vacancy:
                    body = HrVacancyUpdate()
                    body.archive_staff_unit_id = archive_staff_unit.id
                    body.is_active = None
                    body.hr_vacancy_requirements_ids = None
                    body.staff_unit_id = None

                    hr_vacancy_service.update(db, hr_vacancy, body,
                                              current_user_role_id)
                archive_division.staff_units.append(archive_staff_unit)

        if is_leader_needed:
            archive_division.leader_id = leader_id

        db.add(archive_division)
        db.flush()

        return archive_division

    async def create_disposition_doc_by_staff_list_id(
            self,
            db: Session,
            staff_list_id: uuid.UUID,
            current_user_id: uuid.UUID,
            current_user_role_id: str,
    ):
        hr_document_template = hr_document_template_service.get_disposition(
            db=db)
        user_ids = self.get_disposition_user_ids_by_staff_list_id(db, staff_list_id)
        steps = hr_document_template_service.get_steps_by_document_template_id(db, hr_document_template.id, user_ids[0])
        body = HrDocumentInit(
            hr_document_template_id=hr_document_template.id,
            user_ids=user_ids,
            document_step_users_ids=steps,
            parent_id=None,
            due_date=datetime.datetime.now() + datetime.timedelta(days=7),
            properties={}
        )
        hr_document = await hr_document_service.initialize(db, body, current_user_id, current_user_role_id)
        print(hr_document)
        return hr_document

    def get_disposition_user_ids_by_staff_list_id(self, db: Session, staff_list_id: uuid.UUID):
        disposition_division = archive_staff_division_service.get_by_name(db, StaffDivisionEnum.DISPOSITION.value, staff_list_id)
        archive_staff_units = archive_staff_unit_service.get_by_archive_staff_division_id(db, disposition_division.id)
        user_ids = []
        for archive_staff_unit in archive_staff_units:
            user_ids.append(archive_staff_unit.user_id)
        return user_ids

    def get_super_doc_by_staff_list_id(
            self,
            db: Session,
            id: uuid.UUID
    ):
        hr_document_template = hr_document_template_service.get_staff_list(
            db=db)
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
                       .order_by(desc(StaffList.updated_at))
                       .offset(skip)
                       .limit(limit)
                       .all())

        return staff_lists

    def update(self, db: Session, staff_list_id: uuid.UUID, body: StaffListUpdate):
        staff_list = self.get_by_id(db, staff_list_id)
        return super().update(
            db=db, db_obj=staff_list, obj_in=body
        )


staff_list_service = StaffListService(StaffList)
