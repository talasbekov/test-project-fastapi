import uuid
import json
from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session
from sqlalchemy import distinct, func, select, text


from exceptions import BadRequestException, NotFoundException
from models import (StaffDivision, StaffDivisionEnum, StaffDivisionType, ArchiveStaffDivision,
                    StaffUnit, HrVacancy, Secondment, EmergencyServiceHistory,
                    Position)
from schemas import (
    StaffDivisionCreate,
    StaffDivisionRead,
    StaffDivisionReadMinimized,
    StaffDivisionUpdate,
    StaffDivisionUpdateParentGroup,
    StaffDivisionVacancyRead,
    StaffDivisionOptionRead,
    StaffDivisionOptionChildRead,
    StaffDivisionMatreshkaStepRead, 
    StaffDivisionReadSchedule,
    StaffDivisionBaseSchedule,
    StaffDivisionChildReadSchedule
)

from .base import ServiceBase


class StaffDivisionService(
        ServiceBase[StaffDivision, StaffDivisionCreate, StaffDivisionUpdate]):

    def get_by_id(self, db: Session, id: str) -> StaffDivision:
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(
                f"StaffDivision with id: {id} is not found!")
        for staff_unit in group.staff_units:
            if isinstance(staff_unit.requirements, str):
                staff_unit.requirements = json.loads(staff_unit.requirements)
            if staff_unit.user_replacing:
                if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
                    staff_unit.user_replacing.staff_unit.requirements = json.loads(
                        staff_unit.user_replacing.staff_unit.requirements)
        if isinstance(group.description, str):
            group.description = json.loads(group.description)
        for child in group.children:
            if isinstance(child.description, str):
                child.description = json.loads(child.description)
        return group
    
    def get_by_id_schedule(self, db: Session, id: str) -> StaffDivision:
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(
                f"StaffDivision with id: {id} is not found!")
        res = StaffDivisionReadSchedule.from_orm(group)
        # for i in res.children:
        #     for j in i.staff_units:
        #         j.po
        return res

    def get_one_level_by_id(self, db: Session, id: Optional[str]):
        if id == 'None':
            stmt = (select(StaffDivision)
                    .where(StaffDivision.name == StaffDivisionEnum.SERVICE.value))
            group = db.execute(stmt).first()[0]
            # group = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.SERVICE.value).first()
        else:
            stmt = (select(StaffDivision)
                    .where(StaffDivision.id == id))
            group = db.execute(stmt).first()
            if group is None:
                raise NotFoundException(
                    f"StaffDivision with id: {id} is not found!")
            else:
                group = group[0]

        for staff_unit in group.staff_units:
            if isinstance(staff_unit.requirements, str):
                staff_unit.requirements = json.loads(staff_unit.requirements)
        if isinstance(group.description, str):
            group.description = json.loads(group.description)
        for child in group.children:
            child = child.__dict__
            child['is_parent'] = self.__is_parent(db, child['id'])
            if isinstance(child['description'], str):
                child['description'] = json.loads(child['description'])

        group = group.__dict__
        group['is_parent'] = self.__is_parent(db, group['id'])
        return group

    def delete(self, db: Session, id: str) -> StaffDivision:
        staff_division = self.get_by_id(db, id)
        (db.query(ArchiveStaffDivision)
         .filter(ArchiveStaffDivision.origin_id == staff_division.id)
         .update({ArchiveStaffDivision.origin_id: None}))

        histories = (
            db.query(EmergencyServiceHistory)
            .filter(
                EmergencyServiceHistory.staff_division_id == staff_division.id)
            .all())
        for history in histories:
            history.staff_division_id = None
            history.staff_division_name = staff_division.name
            history.staff_division_nameKZ = staff_division.nameKZ
        self._replace_secondment_division_id_with_name(db,
                                                       staff_division)
        super().remove(db, staff_division.id)
        db.flush()

    def get_all_departments(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        service_staff_function = self.get_by_name(
            db, StaffDivisionEnum.SERVICE.value)
        departments = db.query(self.model).filter(
            StaffDivision.parent_group_id == service_staff_function.id
        ).order_by(StaffDivision.staff_division_number).offset(skip).limit(limit).all()
        return [self._return_correctly(db, department)
                for department in departments]

    def get_departments(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[StaffDivision]:
        service_staff_function = self.get_by_name(
            db, StaffDivisionEnum.SERVICE.value)
        departments = db.query(self.model).filter(
            StaffDivision.parent_group_id == service_staff_function.id,
            StaffDivision.is_active == True
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        return departments

    def get_department_name_by_id(
        self,
        db: Session,
        id: str
    ) -> StaffDivision:
        service_staff_division = self.get_by_name(
            db, StaffDivisionEnum.SERVICE.value)
        staff_division = self.get_by_id(db, id)

        if staff_division.id == service_staff_division.id:
            return {"id": staff_division.id,
                    "name": staff_division.name,
                    "nameKZ": staff_division.nameKZ}

        while staff_division.parent_group_id != service_staff_division.id:
            staff_division = self.get_by_id(db, staff_division.parent_group_id)

        return {"id": staff_division.id,
                "name": staff_division.name,
                "nameKZ": staff_division.nameKZ}

    def get_all_parents(self,
                        db: Session,
                        skip: int, limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        return parents
    

    def get_all_except_special(self,
                               db: Session,
                               skip: int,
                               limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            self.model.name != StaffDivisionEnum.SPECIAL_GROUP.value
        ).order_by(StaffDivision.staff_division_number).offset(skip).limit(limit).all()
        for parent in parents:
            if isinstance(parent.description, str):
                parent.description = json.loads(parent.description)
            for staff_unit in parent.staff_units:
                if isinstance(staff_unit.requirements, str):
                    staff_unit.requirements = json.loads(
                        staff_unit.requirements)
                if staff_unit.user_replacing:
                    if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
                        staff_unit.user_replacing.staff_unit.requirements = json.loads(
                            staff_unit.user_replacing.staff_unit.requirements)
            
        return parents
    
    def get_all_except_special_schedule(self,
                               db: Session,
                               skip: int,
                               limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            self.model.name != StaffDivisionEnum.SPECIAL_GROUP.value
        ).order_by(StaffDivision.staff_division_number).offset(skip).limit(limit).all()
        # for parent in parents:
        #     if isinstance(parent.description, str):
        #         parent.description = json.loads(parent.description)
        #     for staff_unit in parent.staff_units:
        #         if isinstance(staff_unit.requirements, str):
        #             staff_unit.requirements = json.loads(
        #                 staff_unit.requirements)
        #         if staff_unit.user_replacing:
        #             if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
        #                 staff_unit.user_replacing.staff_unit.requirements = json.loads(
        #                     staff_unit.user_replacing.staff_unit.requirements)
           
        return [StaffDivisionReadSchedule.from_orm(parent) for parent in parents]
    
    def get_all_except_special_minimized(self,
                               db: Session,
                               skip: int,
                               limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            self.model.name != StaffDivisionEnum.SPECIAL_GROUP.value
        ).order_by(StaffDivision.staff_division_number).offset(skip).limit(limit).all()
        for parent in parents:
            if isinstance(parent.description, str):
                parent.description = json.loads(parent.description)
            for staff_unit in parent.staff_units:
                if isinstance(staff_unit.requirements, str):
                    staff_unit.requirements = json.loads(
                        staff_unit.requirements)
                if staff_unit.user_replacing:
                    if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
                        staff_unit.user_replacing.staff_unit.requirements = json.loads(
                            staff_unit.user_replacing.staff_unit.requirements)
        return parents
    
    def get_all_except_special_schedule(self,
                               db: Session,
                               skip: int,
                               limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            self.model.name != StaffDivisionEnum.SPECIAL_GROUP.value
        ).order_by(StaffDivision.staff_division_number).offset(skip).limit(limit).all()
        # for parent in parents:
        #     if isinstance(parent.description, str):
        #         parent.description = json.loads(parent.description)
        #     for staff_unit in parent.staff_units:
        #         if isinstance(staff_unit.requirements, str):
        #             staff_unit.requirements = json.loads(
        #                 staff_unit.requirements)
        #         if staff_unit.user_replacing:
        #             if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
        #                 staff_unit.user_replacing.staff_unit.requirements = json.loads(
        #                     staff_unit.user_replacing.staff_unit.requirements)
           
        return [StaffDivisionReadSchedule.from_orm(parent) for parent in parents]
    
    def get_all_except_special_minimized(self,
                               db: Session,
                               skip: int,
                               limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            self.model.name != StaffDivisionEnum.SPECIAL_GROUP.value
        ).order_by(StaffDivision.staff_division_number).offset(skip).limit(limit).all()
        for parent in parents:
            if isinstance(parent.description, str):
                parent.description = json.loads(parent.description)
            for staff_unit in parent.staff_units:
                if isinstance(staff_unit.requirements, str):
                    staff_unit.requirements = json.loads(
                        staff_unit.requirements)
                if staff_unit.user_replacing:
                    if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
                        staff_unit.user_replacing.staff_unit.requirements = json.loads(
                            staff_unit.user_replacing.staff_unit.requirements)
        return parents
    
    def get_all_except_special_schedule(self,
                               db: Session,
                               skip: int,
                               limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            self.model.name != StaffDivisionEnum.SPECIAL_GROUP.value
        ).order_by(StaffDivision.staff_division_number).offset(skip).limit(limit).all()
        # for parent in parents:
        #     if isinstance(parent.description, str):
        #         parent.description = json.loads(parent.description)
        #     for staff_unit in parent.staff_units:
        #         if isinstance(staff_unit.requirements, str):
        #             staff_unit.requirements = json.loads(
        #                 staff_unit.requirements)
        #         if staff_unit.user_replacing:
        #             if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
        #                 staff_unit.user_replacing.staff_unit.requirements = json.loads(
        #                     staff_unit.user_replacing.staff_unit.requirements)
           
        return [StaffDivisionReadSchedule.from_orm(parent) for parent in parents]
    
    def get_all_except_special_minimized(self,
                               db: Session,
                               skip: int,
                               limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            self.model.name != StaffDivisionEnum.SPECIAL_GROUP.value
        ).order_by(StaffDivision.staff_division_number).offset(skip).limit(limit).all()
        for parent in parents:
            if isinstance(parent.description, str):
                parent.description = json.loads(parent.description)
            for staff_unit in parent.staff_units:
                if isinstance(staff_unit.requirements, str):
                    staff_unit.requirements = json.loads(
                        staff_unit.requirements)
                if staff_unit.user_replacing:
                    if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
                        staff_unit.user_replacing.staff_unit.requirements = json.loads(
                            staff_unit.user_replacing.staff_unit.requirements)
        return parents

    def get_all_except_special_raw(self,
                                   db: Session,
                                   skip: int,
                                   limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            self.model.name != StaffDivisionEnum.SPECIAL_GROUP.value
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        return parents

    def get_child_groups(self,
                         db: Session,
                         id: str,
                         skip: int,
                         limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == id
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        for parent in parents:
            if isinstance(parent.description, str):
                parent.description = json.loads(parent.description)
            for staff_unit in parent.staff_units:
                if isinstance(staff_unit.requirements, str):
                    staff_unit.requirements = json.loads(
                        staff_unit.requirements)
        return parents

    def get_all_child_groups(self, db: Session,
                             id: str) -> List[StaffDivision]:
        child_groups = (
            db.query(self.model).filter(
                StaffDivision.parent_group_id == id
            ).all()
        )

        for child_group in child_groups:
            child_groups.extend(self.get_all_child_groups(db, child_group.id))

        return child_groups

    def get_by_name(self, db: Session, name: str) -> StaffDivision:
        group = db.query(self.model).filter(
            StaffDivision.name == name
        ).first()
        if group is None:
            raise NotFoundException(
                f"StaffDivision with name: {name} is not found!")
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

    def get_department_id_from_staff_division_id(self,
                                                 db: Session,
                                                 staff_division_id: str):

        staff_division = self.get_by_id(db, staff_division_id)

        parent_id = staff_division.parent_group_id
        sgo_rk_staff_division = self.get_by_name(
            db, StaffDivisionEnum.SERVICE.value)

        res_id = staff_division.id

        while parent_id != sgo_rk_staff_division.id:
            res_id = parent_id
            tmp = self.get_by_id(db, parent_id)
            parent_id = tmp.parent_group_id

        return res_id

    def get_division_parents_by_id(
            self, db: Session, staff_division_id: str):

        staff_division = self.get_by_id(db, staff_division_id)

        parent_id = staff_division.parent_group_id

        prev_staff_division = staff_division
        staff_division.children = []
        while parent_id is not None:
            staff_division = self.get_by_id(db, parent_id)
            staff_division.children = [prev_staff_division]
            prev_staff_division = staff_division
            parent_id = staff_division.parent_group_id

        for staff_unit in staff_division.staff_units:
            if isinstance(staff_unit.requirements, str):
                staff_unit.requirements = json.loads(staff_unit.requirements)
            if staff_unit.user_replacing:
                if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
                    staff_unit.user_replacing.staff_unit.requirements = json.loads(
                        staff_unit.user_replacing.staff_unit.requirements)
        res = StaffDivisionRead.from_orm(staff_division)
        db.rollback()
        return res
    
    def get_division_parents_by_id_minimized(self, db: Session, staff_division_id: str):

        staff_division = self.get_by_id(db, staff_division_id)

        parent_id = staff_division.parent_group_id

        prev_staff_division = staff_division
        staff_division.children = []
        while parent_id is not None:
            staff_division = self.get_by_id(db, parent_id)
            staff_division.children = [prev_staff_division]
            prev_staff_division = staff_division
            parent_id = staff_division.parent_group_id

        for staff_unit in staff_division.staff_units:
            if isinstance(staff_unit.requirements, str):
                staff_unit.requirements = json.loads(staff_unit.requirements)
            if staff_unit.user_replacing:
                if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
                    staff_unit.user_replacing.staff_unit.requirements = json.loads(
                        staff_unit.user_replacing.staff_unit.requirements)
        res = StaffDivisionReadMinimized.from_orm(staff_division)
        db.rollback()
        return res

    def get_by_option(self,
                      db: Session,
                      type: str,
                      id: Optional[str],
                      skip: int, limit: int):
        if id is None:
            all_except_special = self.get_all_except_special(db, skip, limit)
            return [StaffDivisionOptionRead.from_orm(
                i) for i in all_except_special]
        child_groups = self.get_child_groups(db, id, skip, limit)
        return [StaffDivisionOptionRead.from_orm(i) for i in child_groups]

    def get_full_name(self, db: Session, staff_division_id: str):
        staff_division = self.get_by_id(db, staff_division_id)

        parent_id = staff_division.parent_group_id

        full_name = staff_division.name
        full_nameKZ = staff_division.nameKZ

        while parent_id != None:
            tmp = self.get_by_id(db, parent_id)
            full_name = tmp.name + " / " + full_name
            full_nameKZ = tmp.nameKZ + " / " + full_nameKZ
            parent_id = tmp.parent_group_id

        return full_name, full_nameKZ


    # def get_full_name2(self, db: Session, staff_division_id: str):
    #     query = text("""
    #         WITH parent_divisions (id, name, nameKZ, parent_group_id) AS (
    #             SELECT id, name, nameKZ, parent_group_id
    #             FROM staff_division
    #             WHERE id = :staff_division_id
    #             UNION ALL
    #             SELECT sd.id, sd.name, sd.nameKZ, sd.parent_group_id
    #             FROM staff_division sd
    #             INNER JOIN parent_divisions pd ON sd.parent_group_id = pd.id
    #         )
    #         SELECT name, nameKZ FROM parent_divisions;
    #     """)

    #     result = db.execute(query, {"staff_division_id": staff_division_id})

    #     full_name = []
    #     full_nameKZ = []
    #     for row in result:
    #         full_name.append(row['name'])
    #         full_nameKZ.append(row['nameKZ'])

    #     # Reverse the lists to get the correct order from parent to child
    #     full_name = " / ".join(full_name[::-1])
    #     full_nameKZ = " / ".join(full_nameKZ[::-1])

    #     return full_name, full_nameKZ



    
    def create_from_archive(self,
                            db: Session,
                            archive_staff_division: ArchiveStaffDivision,
                            parent_id: str,
                            leader_id: str):
        self._validate_parent(db, parent_id)
        if archive_staff_division.name == StaffDivisionEnum.DISPOSITION.value:
            parent_id = self.get_by_name(
                db, StaffDivisionEnum.SPECIAL_GROUP.value).id
        res = super().create(
            db, StaffDivisionCreate(
                name=archive_staff_division.name,
                nameKZ=archive_staff_division.nameKZ,
                parent_group_id=parent_id,
                type_id=archive_staff_division.type_id,
                staff_division_number=archive_staff_division.staff_division_number,
                description=archive_staff_division.description,
                is_combat_unit=archive_staff_division.is_combat_unit,
                leader_id=leader_id,
                is_active=True
            )
        )
        return res

    def update_from_archive(self, db: Session,
                            archive_staff_division: ArchiveStaffDivision,
                            parent_id: str,
                            leader_id: str):
        self._validate_parent(db, parent_id)
        staff_division = self.get_by_id(db, archive_staff_division.origin_id)
        if archive_staff_division.name == StaffDivisionEnum.DISPOSITION.value:
            parent_id = self.get_by_name(
                db, StaffDivisionEnum.SPECIAL_GROUP.value).id
        res = self._update(
            db,
            db_obj=staff_division,
            obj_data=staff_division.__dict__,
            obj_in=StaffDivisionUpdate(
                name=archive_staff_division.name,
                nameKZ=archive_staff_division.nameKZ,
                parent_group_id=parent_id,
                type_id=archive_staff_division.type_id,
                staff_division_number=archive_staff_division.staff_division_number,
                description=archive_staff_division.description,
                is_combat_unit=archive_staff_division.is_combat_unit,
                leader_id=leader_id,
                is_active=True
            )
        )
        return res

    def create_or_update_from_archive(self,
                                      db: Session,
                                      archive_staff_division: ArchiveStaffDivision,
                                      parent_id: str, leader_id: str):
        if archive_staff_division.origin_id is None:
            return self.create_from_archive(db,
                                            archive_staff_division,
                                            parent_id,
                                            leader_id)
        return self.update_from_archive(db,
                                        archive_staff_division,
                                        parent_id,
                                        leader_id)

    def make_all_inactive(self, db: Session):
        db.query(self.model).filter(
            StaffDivision.name.not_in([*StaffDivisionEnum])
        ).update({StaffDivision.is_active: False})
        db.flush()

    def get_excluded_staff_divisions(self, db: Session):
        except_service_divisions = list(
            filter(lambda x: x != StaffDivisionEnum.SERVICE, StaffDivisionEnum))
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

    def __is_parent(self, db: Session, id: str):
        stmp = select(StaffDivision).where(StaffDivision.parent_group_id == id)
        if db.execute(stmp).first() is not None:
            return True
        else:
            return False

    def _update(
        self,
        db: Session,
        *,
        db_obj: StaffDivision,
        obj_data: dict,
        obj_in: StaffDivisionUpdate
    ) -> StaffDivision:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.flush()
        return db_obj

    def _replace_secondment_division_id_with_name(self,
                                                  db,
                                                  staff_division: StaffDivision):
        (db.query(Secondment)
            .filter(Secondment.staff_division_id == staff_division.id)
            .update({Secondment.staff_division_id: None,
                     Secondment.name: Secondment.name + ": " + staff_division.name,
                     Secondment.nameKZ: Secondment.nameKZ + ": " + staff_division.nameKZ}
                    )
         )
        db.flush()

    def _return_correctly(self, db: Session, staff_division: StaffDivision):

        count_vacancies = self._get_count_vacancies_recursive(
            db, staff_division)

        staff_division = StaffDivisionVacancyRead.from_orm(
            staff_division).dict()

        staff_division['count_vacancies'] = count_vacancies

        return staff_division

    def _get_count_vacancies_recursive(self,
                                       db: Session,
                                       staff_division: StaffDivision):

        count_vacancies = (
            db.query(func.count(distinct(Position.id)))
            .join(StaffUnit, Position.id == StaffUnit.position_id)
            .join(HrVacancy, HrVacancy.staff_unit_id == StaffUnit.id)
            .join(StaffDivision, StaffDivision.id == StaffUnit.staff_division_id)
            .filter(
                HrVacancy.is_active == True,
                StaffUnit.staff_division_id == staff_division.id
            ).scalar()
        )

        for child in staff_division.children:
            count_vacancies += self._get_count_vacancies_recursive(db, child)

        return count_vacancies

    def _validate_parent(self, db: Session, parent_id: str):
        parent = super().get(db, parent_id)
        if parent is None and parent_id:
            raise BadRequestException(
                f"Parent staffDivision with id: {parent_id} is not found!")

    def get_all_by_name(self, db: Session, name: str) -> List[StaffDivision]:
        return db.query(self.model).filter(
            self.model.name == name
        ).all()

    def get_parent_ids(self, db: Session, id: str) -> List[str]:
        staff_division = self.get_by_id(db, id)

        parent_id = staff_division.parent_group_id

        ids = [staff_division.id]

        while parent_id != None:
            if parent_id is None:
                break
            tmp = self.get_by_id(db, parent_id)
            ids.append(tmp.id)
            parent_id = tmp.parent_group_id

        ids.reverse()
        return ids


staff_division_service = StaffDivisionService(StaffDivision)
