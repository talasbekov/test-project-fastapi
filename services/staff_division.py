import uuid
from typing import List, Dict, Any

from sqlalchemy.orm import Session


from exceptions import BadRequestException, NotFoundException
from models import (StaffDivision, StaffDivisionEnum, ArchiveStaffDivision,
                    StaffUnit, HrVacancy, Secondment, EmergencyServiceHistory)
from schemas import (
    StaffDivisionCreate,
    StaffDivisionRead,
    StaffDivisionUpdate,
    StaffDivisionUpdateParentGroup,
    StaffDivisionOptionRead,
)

from .base import ServiceBase


class StaffDivisionService(ServiceBase[StaffDivision, StaffDivisionCreate, StaffDivisionUpdate]):

    def get_by_id(self, db: Session, id: str) -> StaffDivision:
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(f"StaffDivision with id: {id} is not found!")
        return group

    def get_all_departments(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        service_staff_function = self.get_by_name(db, StaffDivisionEnum.SERVICE.value)
        departments = db.query(self.model).filter(
            StaffDivision.parent_group_id == service_staff_function.id
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        
        return [self._return_correctly(db, department) for department in departments]

    def get_departments(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[StaffDivision]:
        service_staff_function = self.get_by_name(db, StaffDivisionEnum.SERVICE.value)
        departments = db.query(self.model).filter(
            StaffDivision.parent_group_id == service_staff_function.id,
            StaffDivision.is_active == True
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        return departments

    def get_all_parents(self, db: Session, skip: int, limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        return parents

    def get_all_except_special(self, db: Session, skip: int, limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            self.model.name != StaffDivisionEnum.SPECIAL_GROUP.value
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        return parents

    def get_child_groups(self, db: Session, id: str, skip: int, limit: int) -> List[StaffDivision]:
        return db.query(self.model).filter(
           StaffDivision.parent_group_id == id
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, name: str) -> StaffDivision:
        group = db.query(self.model).filter(
            StaffDivision.name == name
        ).first()
        if group is None:
            raise NotFoundException(f"StaffDivision with name: {name} is not found!")
        return group

    def change_parent_group(self,
            db: Session,
            id: str,
            body: StaffDivisionUpdateParentGroup
    ) -> StaffDivisionRead:
        group = self.get_by_id(db, id)

        self._validate_parent(db, body.parent_group_id)

        group.parent_group_id = body.parent_group_id
        db.add(group)
        db.flush()
        return group
    
    def get_department_id_from_staff_division_id(self, db: Session, staff_division_id: uuid.UUID):

        staff_division = self.get_by_id(db, staff_division_id)

        parent_id = staff_division.parent_group_id

        res_id = staff_division.id

        while parent_id != None:
            res_id = parent_id
            tmp = self.get_by_id(db, parent_id)
            parent_id = tmp.parent_group_id
        
        return res_id

    def get_division_parents_by_id(self, db: Session, staff_division_id: uuid.UUID):

        staff_division = self.get_by_id(db, staff_division_id)

        parent_id = staff_division.parent_group_id

        prev_staff_division = staff_division
        staff_division.children = []
        while parent_id is not None:
            staff_division = self.get_by_id(db, parent_id)
            staff_division.children = [prev_staff_division]
            prev_staff_division = staff_division
            parent_id = staff_division.parent_group_id
        res = StaffDivisionRead.from_orm(staff_division)
        db.rollback()
        return res
    
    def get_by_option(self, db: Session, type: str, id: uuid.UUID, skip: int, limit: int):
        if id is None:
            return [StaffDivisionOptionRead.from_orm(i) for i in self.get_all_except_special(db, skip, limit)]
        return [StaffDivisionOptionRead.from_orm(i) for i in self.get_child_groups(db, id, skip, limit)]

    def get_full_name(self, db: Session, staff_division_id: uuid.UUID):
        staff_division = self.get_by_id(db, staff_division_id)

        parent_id = staff_division.parent_group_id

        res_id = staff_division.id
        
        full_name = staff_division.name
        full_nameKZ = staff_division.nameKZ

        service = self.get_by_name(db, StaffDivisionEnum.SERVICE.value)

        while parent_id != service.id:
            if parent_id is None:
                break
            tmp = self.get_by_id(db, parent_id)
            full_name = tmp.name + " / " + full_name
            full_nameKZ = tmp.nameKZ + " / " + full_nameKZ
            parent_id = tmp.parent_group_id
        
        return full_name, full_nameKZ
    
    def validate_staff_divisions(self, staff_divisions: List[StaffDivision]):
        parents = [StaffDivisionRead.from_orm(staff_division).dict() for staff_division in staff_divisions]

        # Remove candidate staff division into special group
        for parent in parents:
            if parent['name'] == StaffDivisionEnum.SPECIAL_GROUP.value:
                parent['children'] = [child for child in parent['children'] if child['name'] != StaffDivisionEnum.CANDIDATES.value]

                break

        return parents

    def create_from_archive(self, db: Session, archive_staff_division: ArchiveStaffDivision, parent_id: uuid.UUID, leader_id: uuid.UUID):
        self._validate_parent(db, parent_id)
        res = super().create(
            db, StaffDivisionCreate(
                name=archive_staff_division.name,
                nameKZ=archive_staff_division.nameKZ,
                parent_group_id=parent_id,
                description=archive_staff_division.description,
                is_combat_unit=archive_staff_division.is_combat_unit,
                leader_id=leader_id,
                is_active=True
            )
        )
        return res

    def update_from_archive(self, db: Session, archive_staff_division: ArchiveStaffDivision, parent_id: uuid.UUID, leader_id: uuid.UUID):
        self._validate_parent(db, parent_id)
        staff_division = self.get_by_id(db, archive_staff_division.origin_id)
        res = super().update(
            db,
            db_obj=staff_division,
            obj_in=StaffDivisionUpdate(
                name=archive_staff_division.name,
                nameKZ=archive_staff_division.nameKZ,
                parent_group_id=parent_id,
                description=archive_staff_division.description,
                is_combat_unit=archive_staff_division.is_combat_unit,
                leader_id=leader_id,
                is_active=True
            )
        )
        return res

    def create_or_update_from_archive(self, db: Session, archive_staff_division: ArchiveStaffDivision, parent_id: uuid.UUID, leader_id: uuid.UUID):
        if archive_staff_division.origin_id is None:
            return self.create_from_archive(db, archive_staff_division, parent_id, leader_id)
        return self.update_from_archive(db, archive_staff_division, parent_id, leader_id)

    def make_all_inactive(self, db: Session):
        db.query(self.model).filter(
            StaffDivision.name.not_in([*StaffDivisionEnum])
        ).update({StaffDivision.is_active: False})
        db.flush()

    def get_excluded_staff_divisions(self, db: Session):
        except_service_divisions = list(filter(lambda x: x != StaffDivisionEnum.SERVICE, StaffDivisionEnum))
        return db.query(self.model).filter(
            StaffDivision.name.in_(except_service_divisions)
        ).all()

    def delete_all_inactive(self, db: Session):
        staff_divisions = db.query(self.model).filter(
            self.model.is_active == False
        ).all()
        for staff_division in staff_divisions:
            (db.query(ArchiveStaffDivision)
             .filter(ArchiveStaffDivision.origin_id == staff_division.id)
             .update({ArchiveStaffDivision.origin_id: None}))

            histories = (
                db.query(EmergencyServiceHistory)
                .filter(EmergencyServiceHistory.staff_division_id == staff_division.id)
                .all())
            for history in histories:
                history.staff_division_id = None
                history.staff_division_name = staff_division.name
                history.staff_division_nameKZ = staff_division.nameKZ
            self._replace_secondment_division_id_with_name(db, staff_division)
            super().remove(db, staff_division.id)
        db.flush()


    def _replace_secondment_division_id_with_name(self, db, staff_division: StaffDivision):
        (db.query(Secondment)
            .filter(Secondment.staff_division_id == staff_division.id)
            .update({Secondment.staff_division_id: None,
                     Secondment.name: staff_division.name,
                     Secondment.nameKZ: staff_division.nameKZ}
                   )
        )
        db.flush()

    
    def _return_correctly(self, db: Session, staff_division: StaffDivision):
        
        count_vacancies = self._get_count_vacancies_recursive(db, staff_division)
        
        staff_division = StaffDivisionRead.from_orm(staff_division).dict()
        
        staff_division['count_vacancies'] = count_vacancies
        
        return staff_division
    
        
    def _get_count_vacancies_recursive(self, db: Session, staff_division: StaffDivision):
        
        count_vacancies = (
            db.query(HrVacancy)
                .join(StaffUnit, HrVacancy.staff_unit_id == StaffUnit.id)
                .join(StaffDivision, StaffUnit.staff_division_id == StaffDivision.id)
                .filter(
                    HrVacancy.is_active == True,
                    HrVacancy.staff_unit_id == StaffUnit.id,
                    StaffUnit.staff_division_id == staff_division.id
                ).count()
        )
        
        for child in staff_division.children:
            count_vacancies += self._get_count_vacancies_recursive(db, child)
            
        return count_vacancies


    def _validate_parent(self, db: Session, parent_id: uuid.UUID):
        parent = super().get(db, parent_id)
        if parent is None and parent_id:
            raise BadRequestException(f"Parent staffDivision with id: {parent_id} is not found!")


staff_division_service = StaffDivisionService(StaffDivision)
