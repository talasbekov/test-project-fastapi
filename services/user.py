import types
import datetime
from typing import List, Optional, Any, Union, Dict
from sqlalchemy.orm import Session, Query
from sqlalchemy import func, and_, not_
from fastapi.encoders import jsonable_encoder
import json
import base64
import requests

from exceptions import NotFoundException, InvalidOperationException, BadRequestException
from models import (
    StaffDivision,
    User,
    StaffUnit,
    Jurisdiction,
    JurisdictionEnum,
    DocumentStaffFunction,
    StaffDivisionEnum,
    HrDocument,
    HrDocumentInfo,
    HrDocumentTemplate,
    ScheduleYear,
    SubjectType,
    StatusHistory,
    Status,
    Position,
    PositionType
)
from schemas import (
    UserCreate,
    UserUpdate,
    UserShortRead,
    DocumentReadForUser,
    UserRead,
)
from services import (
    staff_division_service,
    staff_unit_service,
    jurisdiction_service,
    document_staff_function_service,
    document_staff_function_type_service,
    hr_document_status_service,
    hr_document_template_service,
    categories,
    hr_document_step_service,
)
from .base import ServiceBase

CALLABLES = types.FunctionType, types.MethodType


class UserService(ServiceBase[User, UserCreate, UserUpdate]):

    def create(self, db: Session,
               obj_in: Union[UserCreate, Dict[str, Any]]) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        try:
            obj_in_data['date_birth'] = datetime.datetime.strptime(obj_in_data['date_birth'], '%Y-%m-%d')
        except ValueError:
            obj_in_data['date_birth'] = datetime.datetime.strptime(obj_in_data['date_birth'], '%Y-%m-%dT%H:%M:%S')
        db_obj = self.model(**obj_in_data)  # type: ign
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_id(self, db: Session, id: str) -> User:

        user = super().get(db, id)
        if user is None:
            raise NotFoundException(detail="User is not found!")
        if (user.personal_id):
            user.personal_id = user.personal_id.capitalize()

        # Convert the image URL to a base64 byte object
        # if user.icon.startswith('http'):
        #     try:
        #         response = requests.get(user.icon)
        #         user.icon = base64.b64encode(response.content)
        #     except:
        #         print('Error while converting image to base64')
        return user

    def get_all(self,
                db: Session,
                hr_document_template_id: str,
                filter: str,
                skip: int,
                limit: int):
        users = (
            db.query(self.model)
        )
        if filter != '':
            users = self._add_filter_to_query(users, filter)

        if hr_document_template_id is not None:
            template = (
                hr_document_template_service.get_by_id(
                    db, hr_document_template_id
                )
            )
            excepted_users = self._get_excepted_users_by_document_in_progress(
                db, hr_document_template_id)
            users = (self
                     ._filter_for_eligible_actions(db,
                                                   users,
                                                   hr_document_template_id)
                     .except_(excepted_users)
                     .filter(self.model.is_active == True))

            if template.subject_type == SubjectType.CANDIDATE.value:
                candidate_staff_division = (
                    staff_division_service.get_by_name(
                        db, StaffDivisionEnum.CANDIDATES.value
                    )
                )
                users = (
                    users
                    .join(StaffUnit, StaffUnit.id == self.model.staff_unit_id)
                    .filter(StaffUnit.staff_division_id == candidate_staff_division.id)
                )

                # users = [UserShortRead.from_orm(user) for user in users]
        total = (
            users.count()
        )
        users = (
            users
            .order_by(func.to_char(User.last_name), func.to_char(User.first_name), func.to_char(User.id))
            .distinct()
            .offset(skip)
            .limit(limit)
            .all()
        )
        if hr_document_template_id is not None:
            # print(len(users))
            users = [UserShortRead.from_orm(user) for user in users]
        return total, users

    def is_template_accessible_for_user(self,
                                        db: Session,
                                        user_id: str,
                                        template_id: str) -> bool:
        user = self.get_by_id(db, user_id)

        unavailable_users = self._get_excepted_users_by_document_in_progress(
            db, template_id)

        return True if user not in unavailable_users else False

    def get_all_active(self,
                       db: Session,
                       filter: str,
                       skip: int,
                       limit: int,
                       user_id: str):
        user_queue = self._get_users_by_filter_is_active(
            db, filter, True, user_id)

        users = (
            user_queue
            .order_by(self.model.last_name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        for user in users:
            status_histories = db.query(StatusHistory).order_by(
                StatusHistory.created_at).filter(StatusHistory.user_id == user.id).all()
            for status_history in status_histories:
                if status_history != [] and (status_history.date_to is not None):
                    today = datetime.datetime.now()
                    if status_history.date_from < today and status_history.date_to > today:
                        user.statuses = [status_history.status]
                        break
                    else:
                        user.statuses = []

        return users, user_queue.count()

    def get_all_archived(self,
                         db: Session,
                         filter: str,
                         skip: int,
                         limit: int,
                         user_id: str):
        user_queue = self._get_users_by_filter_is_active(
            db, filter, False, user_id)

        users = (
            user_queue
            .order_by(self.model.last_name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return users, user_queue.count()

    def get_by_email(self, db: Session, email: str):

        user = db.query(self.model).filter(User.email == email).first()

        return user

    def get_by_call_sign(self, db: Session, call_sign: str):

        user = db.query(self.model).filter(User.call_sign == call_sign).first()

        return user

    def get_by_id_number(self, db: Session, id_number: str):

        user = db.query(self.model).filter(
            self.model.id_number == id_number).first()

        return user

    def update_user_patch(self, db: Session, id: str, body: UserUpdate) -> User:
        user = self.get_by_id(db, id)
        if user.call_sign is None:
            user.call_sign = ''

        if body.email is not None:
            user.email = body.email
        if body.first_name is not None:
            user.first_name = body.first_name
        if body.last_name is not None:
            user.last_name = body.last_name
        if body.father_name is not None:
            user.father_name = body.father_name
        if body.icon is not None:
            user.icon = body.icon
        if body.call_sign is not None and body.call_sign.lower() != user.call_sign.lower():
            self._swipe_call_sign(db, user.call_sign.capitalize(), body.call_sign.capitalize())
            user.call_sign = body.call_sign.capitalize()
        if body.id_number is not None:
            user.id_number = body.id_number
        if body.phone_number is not None:
            user.phone_number = body.phone_number
        if body.address is not None:
            user.address = body.address
        if body.service_phone_number is not None:
            user.service_phone_number = body.service_phone_number
        if body.cabinet is not None:
            user.cabinet = body.cabinet
        if body.is_military is not None:
            user.is_military = body.is_military
        if body.supervised_by is not None:
            user.supervised_by = body.supervised_by
        if body.personal_id is not None:
            user.personal_id = body.personal_id
        if body.date_birth is not None:
            user.date_birth = body.date_birth
        if body.iin is not None:
            user.iin = body.iin

        try:
            setattr(user, 'updated_at', datetime.datetime.now())
            db.add(user)
            db.flush()
        except Exception as e:
            print(e)

        return user

    def _validate_id(self, db: Session, id: str):
        if id is None:
            return False
        user = db.query(self.model).filter(self.model.id == id).first()
        if user is not None:
            raise BadRequestException(
                detail="User with this id already exists!")
        return True

    def get_fields(self):
        fields = [key for key, value in User.__dict__.items() if
                  ('id' not in key
                   and not isinstance(value, CALLABLES)
                   and not key.startswith('_'))]
        return fields

    def get_all_by_staff_unit(self, db: Session, staff_unit_id: str):

        users = db.query(self.model).filter(
            self.model.staff_unit_id == staff_unit_id
        ).all()

        return users

    def get_user_by_staff_unit(self, db: Session, staff_unit_id):

        users = db.query(self.model).filter(
            self.model.staff_unit_id == staff_unit_id
        ).first()

        return users

    def get_by_schedule_id(self, db: Session,
                           schedule_id: str,
                           skip: int,
                           limit: int):

        users = (db.query(User)
                 .join(ScheduleYear.users)
                 .filter(ScheduleYear.id == schedule_id)
                 .offset(skip)
                 .limit(limit)
                 .all())

        total = (db.query(User)
                 .join(ScheduleYear.users)
                 .filter(ScheduleYear.id == schedule_id)
                 .count())

        return {'total': total, 'objects': users}

    def get_by_iin(self, db: Session, iin: str):

        user = db.query(self.model).filter(
            self.model.iin == iin
        ).first()

        return user

    def get_by_jurisdiction(
            self, db: Session,
            user_id: str,
            skip: int = 0,
            limit: int = 100
    ):
        current_user = self.get_by_id(db, user_id)

        staff_unit: StaffUnit = staff_unit_service.get_by_id(
            db, current_user.staff_unit_id)

        document_staff_functions: List[DocumentStaffFunction] = []

        for i in staff_unit.staff_functions:
            document_staff_functions.append(
                document_staff_function_service.get_by_id(db, i.id))

        jurisdictions: List[Jurisdiction] = []
        for i in document_staff_functions:
            jurisdictions.append(
                jurisdiction_service.get_by_id(db, i.jurisdiction_id))

        staff_division: StaffDivision = staff_division_service.get_by_id(
            db, staff_unit.staff_division_id)

        for i in jurisdictions:
            if i.name == JurisdictionEnum.ALL_SERVICE.value:
                return super().get_multi(db, skip=skip, limit=limit)

            if i.name == JurisdictionEnum.PERSONNEL.value:
                return self.get_users_by_staff_division(
                    db, staff_division)

            if i.name == JurisdictionEnum.SUPERVISED_EMPLOYEES.value:
                return db.query(self.model).filter(
                    self.model.supervised_by.isnot(None)
                ).all()

            if i.name == JurisdictionEnum.COMBAT_UNIT.value:
                return self._get_users_by_combat_unit_jurisdiction(db)

            if i.name == JurisdictionEnum.STAFF_UNIT.value:
                return self._get_users_by_staff_unit_jurisdiction(db)

            if i.name == JurisdictionEnum.CANDIDATES.value:
                return self._get_users_by_candidates_jurisdiction(db)

    def get_users_by_staff_division(
            self,
            db: Session,
            staff_division: StaffDivision) -> List[User]:
        # Получаем все дочерние штатные группы пользователя, включая саму
        # группу
        staff_divisions: List[StaffDivision] = (
            staff_division_service.get_all_child_groups(
                db, staff_division.id)
        )
        staff_divisions.append(staff_division)

        # Получаем все staff unit из staff divisions
        staff_units: List[StaffUnit] = []
        for i in staff_divisions:
            staff_units.extend(
                staff_unit_service.get_all_by_staff_division_id(db, i.id)['objects'])

        users: List[User] = []
        for i in staff_units:
            users.extend(i.actual_users)

        return users

    def _get_excepted_users_by_document_in_progress(self,
                                                    db: Session,
                                                    hr_document_template_id: str):
        forbidden_statuses = hr_document_status_service.get_by_names(
            db, ["Завершен", "Отменен", "На доработке"])

        excepted_users = (
            db.query(self.model)
            .distinct(self.model.id)
            .join(HrDocument.users)
            .join(HrDocumentInfo, HrDocument.id == HrDocumentInfo.hr_document_id)
        )
        steps = hr_document_step_service.get_all_by_document_template_id(
            db,
            hr_document_template_id)
        for step in steps:
            if step.is_direct_supervisor:
                excepted_users = (
                    excepted_users
                    .join(StaffUnit, StaffUnit.id == User.staff_unit_id)
                    .join(StaffDivision, StaffDivision.id == StaffUnit.staff_division_id)
                    .filter(StaffDivision.leader_id.is_(None)))
                break
        excepted_users = (
            excepted_users
            .filter(HrDocument.hr_document_template_id == hr_document_template_id,
                    HrDocumentInfo.signed_by_id.is_(None),
                    and_(*[HrDocument.status_id !=
                           status.id for status in forbidden_statuses])
                    )
        )
        return excepted_users

    def _get_users_by_combat_unit_jurisdiction(self, db: Session):
        staff_divisions = db.query(StaffDivision).filter(
            StaffDivision.is_combat_unit == True
        ).all()

        staff_units: List[StaffUnit] = []
        for i in staff_divisions:
            staff_units.extend(i.staff_units)

        users: List[User] = []
        for i in staff_units:
            users.extend(i.actual_users)

        return users

    def _get_users_by_staff_unit_jurisdiction(self, db: Session):
        staff_divisions = db.query(StaffDivision).filter(
            StaffDivision.is_combat_unit == False
        ).all()

        staff_units: List[StaffUnit] = []
        for i in staff_divisions:
            staff_units.extend(i.staff_units)

        users: List[User] = []
        for i in staff_units:
            users.extend(i.actual_users)

        return users

    def _get_users_by_candidates_jurisdiction(self, db: Session):
        staff_division = db.query(StaffDivision).filter(
            StaffDivision.name == StaffDivisionEnum.CANDIDATES.value
        ).first()

        staff_units: List[StaffUnit] = []
        staff_units.extend(staff_division.staff_units)

        users: List[User] = []
        for i in staff_units:
            users.extend(i.actual_users)

        return users

    def _get_users_by_filter_is_active(self,
                                       db: Session,
                                       filter: Optional[str],
                                       is_active: bool,
                                       user_id: str) -> Query[Any]:
        users = (
            db.query(self.model)
            .filter(
                self.model.is_active == is_active,
                self.model.id != user_id
            )
        )

        if filter != '':
            users = self._add_filter_to_query(users, filter)

        return users

    def _add_filter_to_query(self, user_query, filter):
        key_words = filter.lower().split()
        users = (
            user_query
            .filter(
                and_(func.concat(func.concat(func.concat(func.lower(User.first_name), ' '),
                                             func.concat(func.lower(User.last_name), ' ')),
                                 func.lower(User.father_name)).contains(name) for name in key_words)
            )
        )
        return users

    def _filter_for_eligible_actions(self,
                                     db: Session,
                                     user_query: Query[Any],
                                     hr_document_template_id: str):
        from .constructor import handlers

        template = hr_document_template_service.get_by_id(
            db, hr_document_template_id
        )
        for i in template.actions['args']:
            action_name = list(i)[0]
            handler = handlers.get(action_name)

            if handler is None or getattr(
                    handler, 'handle_filter', None) is None:
                continue

            user_query = handler.handle_filter(db, user_query)
            # print(len(user_query))
        return user_query

    def get_available_templates(self, db: Session, user_id: str, skip: int, limit: int) -> List[DocumentReadForUser]:
        initiator_role = document_staff_function_type_service.get_initiator(db)
        user = self.get_by_id(db, user_id)
        document_ids = []
        
        functions = (db.query(DocumentStaffFunction)
                    .filter(
                        DocumentStaffFunction.staff_units.any(
                            StaffUnit.id == user.staff_unit_id),
                        DocumentStaffFunction.role_id == initiator_role.id,
                        DocumentStaffFunction.hr_document_step != None
                    ).all())
        
        document_ids = []
        [document_ids.extend(
            categories[handler].get_templates(db, initiator_role.id, user_id))
        if handler != 0 else []
        for handler in categories]
        
        document_ids.extend([
            function.hr_document_step.hr_document_template_id
            for function in functions])
        
        templates = hr_document_template_service.get_all_skip(db, document_ids, skip, limit)
        
        result = []
        for template in templates:
            properties = template.properties
            description = template.description
            actions = template.actions
            document_template=template.documents
            # last_step = template.steps

            # if isinstance(last_step, str):
            #     try:
            #         last_step = json.loads(last_step)  
            #     except json.JSONDecodeError:
            #         last_step = {}

            if isinstance(document_template, str):
                document_template = json.loads(document_template) if document_template else {}

            if isinstance(actions, str):
                actions = json.loads(actions) if actions else {}
            
            if isinstance(properties, str):
                properties = json.loads(properties) if properties else {}
            
            if isinstance(description, str):
                description = json.loads(description) if description else {}
            
            result.append(DocumentReadForUser(
                id=template.id,
                name=template.name or "",
                path=template.path,
                pathKZ=template.pathKZ,
                subject_type=template.subject_type,
                properties=properties,
                actions=actions,
                description=description,
                maintainer_id=template.maintainer_id,
                is_visible=template.is_visible,
                is_due_date_required=template.is_due_date_required,
                is_initial_comment_required=template.is_initial_comment_required,
                is_draft=template.is_draft,
                is_active=template.is_active,
                document_template=document_template,
                # users=template.users or [],
                # last_step=last_step,
                # status=template.status or "",
                # new_value=template.new_value or ""
            ))

        return result


    def _validate_call_sign(self, db: Session, call_sign: str):
        user = db.query(User).filter(User.call_sign == call_sign).first()
        if user:
            user_name = (getattr(user, 'first_name', '') + " " +
                         getattr(user, 'last_name', '') + " " +
                         getattr(user, 'father_name', ''))
            raise InvalidOperationException(
                f"call_sign {call_sign} is already assigned to {user_name}!"
            )

    def _swipe_call_sign(self, db: Session, init_call: str, new_call: str):
        # print(1)
        user = db.query(User).filter(User.call_sign == new_call).first()
        if user:
            # print(user.id)
            user.call_sign = init_call
            try:
                db.add(user)
                # db.flush()
            except Exception as e:
                print(e)
        # print(2)

    def get_all_by_position(self, db: Session, position_id: str):

        users = (db.query(User)
                 .join(StaffUnit.users)
                 .filter(StaffUnit.position_id == position_id)
                 .all())

        return users

    def get_iin_by_ids(self, db: Session, user_ids: List[str]):
        users = db.query(User.iin).filter(User.id.in_(user_ids)).all()

        users_iin = [user[0] for user in users]

        return users_iin

    def get_all_iin_by_ids(self, db: Session, user_ids: List[str], candidate_ids: List[str]):
        users_iin = self.get_iin_by_ids(db, user_ids)
    
        candidates_iin = self.get_iin_by_ids(db, candidate_ids)

        return {'Сотрудники': users_iin, 'Кандидаты': candidates_iin}

    def get_all_heads_except_pgs(self, db: Session) -> List[User]:
        # head_positions_users = db.query(User)\
        # .join(StaffDivision, User.staff_unit_id == StaffDivision.leader_id)\
        # .join(StaffUnit, StaffUnit.id == User.staff_unit_id)\
        # .join(Position, StaffUnit.actual_position_id == Position.id)\
        # .filter(Position.name.like('%Начальник%'))\
        # .filter(not_(Position.name.like('%Начальник службы%')))\
        # .all()

        leaders = staff_division_service.get_all_leaders(db)
        head_positions_users = []
        for user in leaders:
            if user.staff_unit and user.staff_unit.actual_position and user.staff_unit.actual_position.category_code == 'ПГС':
                continue
            head_positions_users.append(user)

        total = len(head_positions_users)
        return total, head_positions_users

    def get_all_unemployed(self, db: Session, is_free: bool, skip: int, limit: int) -> List[UserShortRead]:
        if is_free:
            users = db.query(User)\
                .join(StaffUnit, User.actual_staff_unit_id == StaffUnit.id)\
                .join(Position, StaffUnit.position_id == Position.id)\
                .join(PositionType, Position.type_id == PositionType.id)\
                .filter(PositionType.name == 'В распоряжении')\
                .offset(skip)\
                .limit(limit)\
                .all()
        else:
            users = db.query(User)\
                .offset(skip)\
                .limit(limit)\
                .all()
        return [UserShortRead.from_orm(user) for user in users]

    def get_user_by_iin(self, db: Session, iin: str) -> Optional[UserShortRead]:
        user = db.query(User).filter(User.iin == iin).first()
        return UserShortRead.from_orm(user) if user else None

    def get_users_for_vacancy_fill(self, db: Session, staff_unit_id: str, filter: str, skip: int, limit: int, user_id: str):
        staff_unit = staff_unit_service.get_by_id(db, staff_unit_id)
        users = (
            db.query(self.model)
        )
        if filter != '':
            users = self._add_filter_to_query(users, filter)
        
        # users_by_staff_division = self.get_users_by_staff_division(
        #     db, staff_unit.staff_division)

        users_by_staff_division = users.join(StaffUnit, StaffUnit.id == self.model.staff_unit_id)\
                                        .filter(StaffUnit.staff_division_id == staff_unit.staff_division_id).all()
        if staff_unit.actual_position is not None:
            max_rank = staff_unit.actual_position.max_rank
        else:
            max_rank = staff_unit.position.max_rank
        res = []
        for user in users_by_staff_division:
            if user.id == user_id:
                continue
            user_temp = {"id": user.id, "first_name": user.first_name,
                         "last_name": user.last_name, "father_name": user.father_name, "icon":user.icon, "rank": user.rank, "staff_unit_id": user.staff_unit_id, "is_eligible": False}
            if user.rank.rank_order <= max_rank.rank_order and user.rank.rank_order >= 14:
                user_temp["is_eligible"] = True
            res.append(user_temp)
        return sorted(res, key=lambda x: x["is_eligible"], reverse=True)
    
    def update_user_rank(self, db: Session, id: str, rank_id: str):
        user = super().get(db, id)
        if user is None:
            raise NotFoundException(detail="User is not found!")
        user.rank_id = rank_id
        user.updated_at = datetime.datetime.now()
        db.add(user)  
        db.flush()    
        return user 



user_service = UserService(User)
