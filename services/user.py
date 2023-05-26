import types
import uuid
from typing import List, Optional, Any
from sqlalchemy.orm import make_transient
from sqlalchemy.orm import Session, Query
from sqlalchemy import func, or_, and_

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
    Attestation,
    Badge,
    Rank,
    Contract,
    Coolness,
    Equipment,
    Event,
    History,
    Notification,
    Penalty,
    PersonalReserve,
    PrivilegeEmergency,
    Profile,
    RecommenderUser,
    Secondment,
    ServiceID,
    StaffList,
    Status,
    UserOath,
    UserStat,
    ArchiveStaffUnit,
    NameChangeHistory,
    Candidate,
    ServiceCharacteristicHistory,
)
from schemas import (
    UserCreate,
    UserUpdate,
    HrDocumentTemplateRead,
)
from services import (
    staff_division_service,
    staff_unit_service,
    jurisdiction_service,
    document_staff_function_service,
    document_staff_function_type_service,
    hr_document_status_service,
    hr_document_template_service,
    staff_unit_service,
)
from .base import ServiceBase

CALLABLES = types.FunctionType, types.MethodType


class UserService(ServiceBase[User, UserCreate, UserUpdate]):

    def get_by_id(self, db: Session, id: str) -> User:

        user = super().get(db, id)
        if user is None:
            raise NotFoundException(detail="User is not found!")

        return user

    def get_all(self, db: Session, hr_document_template_id: uuid.UUID, filter: str, skip: int, limit: int) -> List[User]:
        users = (
            db.query(self.model)
        )

        if filter != '':
            users = self._add_filter_to_query(users, filter)

        if hr_document_template_id is not None:
            excepted_users = self._get_excepted_users_by_document_in_progress(db, hr_document_template_id)
            users = self._filter_for_eligible_actions(db, users, hr_document_template_id).except_(excepted_users)

        users = (
            users
            .order_by(self.model.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return users

    def get_all_active(self, db: Session, filter: str, skip: int, limit: int) -> List[User]:
        users = self._get_users_by_filter_is_active(db, filter, skip, limit, True)

        return users

    def get_all_archived(self, db: Session, filter: str, skip: int, limit: int) -> List[User]:
        users = self._get_users_by_filter_is_active(db, filter, skip, limit, False)

        return users

    def get_by_email(self, db: Session, email: str):

        user = db.query(self.model).filter(User.email == email).first()

        return user

    def get_by_call_sign(self, db: Session, call_sign: str):

        user = db.query(self.model).filter(User.call_sign == call_sign).first()

        return user

    def get_by_id_number(self, db: Session, id_number: str):

        user = db.query(self.model).filter(self.model.id_number == id_number).first()

        return user

    def update_user_patch(self, db: Session, id: str, body: UserUpdate) -> User:

        user = self.get_by_id(db, id)

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
        if body.call_sign is not None and body.call_sign != user.call_sign:
            self._validate_call_sign(db, body.call_sign)
            user.call_sign = body.call_sign
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
        if self._validate_id(db, body.id):
            print('id is valid')
            self.update_id(db, user.id, body.id)    

        db.add(user)
        db.flush()

        return user
    
    def _validate_id(self, db: Session, id: str):
        if id is None:
            return False
        user = db.query(self.model).filter(self.model.id == id).first()
        if user is not None:
            raise BadRequestException(detail="User with this id already exists!")
        return True
    
    def get_fields(self):
        fields = [key for key, value in User.__dict__.items() if
                  (not 'id' in key and not isinstance(value, CALLABLES) and not key.startswith('_'))]
        return fields

    def get_by_staff_unit(self, db: Session, staff_unit_id):

        users = db.query(self.model).filter(
            self.model.actual_staff_unit_id == staff_unit_id
        ).all()

        return users
    
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

        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, current_user.actual_staff_unit_id)

        document_staff_functions: List[DocumentStaffFunction] = []

        for i in staff_unit.staff_functions:
            document_staff_functions.append(document_staff_function_service.get_by_id(db, i.id))

        jurisdictions: List[Jurisdiction] = []
        for i in document_staff_functions:
            jurisdictions.append(jurisdiction_service.get_by_id(db, i.jurisdiction_id))

        staff_division: StaffDivision = staff_division_service.get_by_id(db, staff_unit.staff_division_id)

        for i in jurisdictions:
            if i.name == JurisdictionEnum.ALL_SERVICE.value:
                return super().get_multi(db, skip=skip, limit=limit)

            if i.name == JurisdictionEnum.PERSONNEL.value:
                return self._get_users_by_personnel_jurisdiction(db, staff_division)

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

    def _get_users_by_personnel_jurisdiction(self, db: Session, staff_division: StaffDivision) -> List[User]:
        # Получаем все дочерние штатные группы пользователя, включая саму группу
        staff_divisions: List[StaffDivision] = staff_division_service.get_child_groups(db, staff_division.id)
        staff_divisions.append(staff_division)

        # Получаем все staff unit из staff divisions
        staff_units: List[StaffUnit] = []
        for i in staff_divisions:
            staff_units.extend(staff_unit_service.get_by_staff_division_id(db, i.id))

        users: List[User] = []
        for i in staff_units:
            users.extend(i.actual_users)

        return users

    def _get_excepted_users_by_document_in_progress(self, db: Session, hr_document_template_id: uuid.UUID):
        forbidden_statuses = hr_document_status_service.get_by_names(db, ["Завершен", "Отменен"])
        excepted_users = (
            db.query(self.model)
            .distinct(self.model.id)
            .join(HrDocument.users)
            .join(HrDocumentInfo, HrDocument.id == HrDocumentInfo.hr_document_id)
            .filter(HrDocument.hr_document_template_id == hr_document_template_id,
                    HrDocumentInfo.signed_by_id.is_(None),
                    and_(*[HrDocument.status_id != status.id for status in forbidden_statuses])
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

    def _get_users_by_filter_is_active(self, db: Session, filter: Optional[str], skip: int, limit: int, is_active: bool)\
            -> List[User]:
        users = (
            db.query(self.model)
            .filter(self.model.is_active.is_(is_active))
        )

        if filter != '':
            users = self._add_filter_to_query(users, filter)

        users = (
            users
            .order_by(self.model.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return users

    def _add_filter_to_query(self, user_query, filter):
        key_words = filter.lower().split()
        users = (user_query
                 .filter(and_(func.concat(func.lower(User.first_name), ' ',
                              func.lower(User.last_name), ' ',
                              func.lower(User.father_name)).contains(name) for name in key_words)
                )
        )
        return users

    def _filter_for_eligible_actions(self, db: Session, user_query: Query[Any], hr_document_template_id: uuid.UUID):
        from .constructor import handlers
        template = hr_document_template_service.get_by_id(
            db, hr_document_template_id
        )
        for i in template.actions['args']:
            action_name = list(i)[0]
            handler = handlers.get(action_name)

            if handler is None or getattr(handler, 'handle_filter', None) is None:
                continue

            user_query = handler.handle_filter(db, user_query)

        return user_query

    def get_available_templates(self, db: Session, user_id: uuid.UUID) -> List[HrDocumentTemplate]:
        initiator_role = document_staff_function_type_service.get_initiator(db)
        user = self.get_by_id(db, user_id)
        document_ids = []
        for function in user.staff_unit.staff_functions:
            if function.discriminator != DocumentStaffFunction.__mapper_args__['polymorphic_identity']:
                continue
            if function.role_id == initiator_role.id:
                if (function.hr_document_step is None):
                    continue
                document_ids.append(function.hr_document_step.hr_document_template_id)
        return hr_document_template_service.get_all(db, document_ids)

    def _validate_call_sign(self,db: Session, call_sign: str):
        user = db.query(User).filter(User.call_sign == call_sign).first()
        if user:
            user_name = user.first_name + " " + user.last_name + " " + user.father_name
            raise InvalidOperationException(
                f"call_sign {call_sign} is already assigned to {user_name}!"
            )

    def update_id(self, db: Session, id: uuid.UUID, new_id: uuid.UUID):
        user = self.get_by_id(db, id)

        new_user = User(
            id=new_id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name,
            icon=user.icon,
            phone_number=user.phone_number,
            address=user.address,
            rank_id=user.rank_id,
            last_signed_at=user.last_signed_at,
            staff_unit_id=user.staff_unit_id,
            actual_staff_unit_id=user.actual_staff_unit_id,
            supervised_by=user.supervised_by,
            description=user.description,
            cabinet=user.cabinet,
            service_phone_number=user.service_phone_number,
            is_military=user.is_military,
            personal_id=user.personal_id,
            iin=user.iin,
            date_birth=user.date_birth,
        )
        print('create new user')
        db.add(new_user)
        db.commit()
        new_user = self.get_by_id(db, new_id)
        print('new user created')
        db.query(History).filter(History.user_id == id).update({'user_id': new_user.id})
        db.query(Profile).filter(Profile.user_id == id).update({'user_id': new_user.id})
        db.query(Attestation).filter(Attestation.user_id == id).update({'user_id': new_user.id})
        db.query(Badge).filter(Badge.user_id == id).update({Badge.user_id: new_user.id})
        db.query(Contract).filter(Contract.user_id == id).update({Contract.user_id: new_user.id})
        db.query(Coolness).filter(Coolness.user_id == id).update({Coolness.user_id: new_user.id})
        db.query(Equipment).filter(Equipment.user_id == id).update({Equipment.user_id: new_user.id})
        db.query(Event).filter(Event.user_id == id).update({Event.user_id: new_user.id})
        db.query(HrDocumentInfo).filter(HrDocumentInfo.signed_by_id == id).update({HrDocumentInfo.signed_by_id: new_user.id})
        db.query(HrDocumentInfo).filter(HrDocumentInfo.assigned_to_id == id).update({HrDocumentInfo.assigned_to_id: new_user.id})
        db.query(HrDocument).filter(HrDocument.initialized_by_id == id).update({HrDocument.initialized_by_id: new_user.id})
        db.query(Notification).filter(Notification.receiver_id == id).update({Notification.receiver_id: new_user.id})
        db.query(Penalty).filter(Penalty.user_id == id).update({Penalty.user_id: new_user.id})
        db.query(PersonalReserve).filter(PersonalReserve.user_id == id).update({PersonalReserve.user_id: new_user.id})
        db.query(PrivilegeEmergency).filter(PrivilegeEmergency.user_id == id).update({PrivilegeEmergency.user_id: new_user.id})
        db.query(RecommenderUser).filter(RecommenderUser.user_id == id).update({RecommenderUser.user_id: new_user.id})
        db.query(RecommenderUser).filter(RecommenderUser.user_by_id == id).update({RecommenderUser.user_by_id: new_user.id})
        db.query(Secondment).filter(Secondment.user_id == id).update({Secondment.user_id: new_user.id})
        db.query(ServiceID).filter(ServiceID.user_id == id).update({ServiceID.user_id: new_user.id})
        db.query(StaffList).filter(StaffList.user_id == id).update({StaffList.user_id: new_user.id})
        db.query(Status).filter(Status.user_id == id).update({Status.user_id: new_user.id})
        db.query(UserOath).filter(UserOath.user_id == id).update({UserOath.user_id: new_user.id})
        db.query(UserStat).filter(UserStat.user_id == id).update({UserStat.user_id: new_user.id})
        db.query(ArchiveStaffUnit).filter(ArchiveStaffUnit.user_id == id).update({ArchiveStaffUnit.user_id: new_user.id})
        db.query(ArchiveStaffUnit).filter(ArchiveStaffUnit.actual_user_id == id).update({ArchiveStaffUnit.actual_user_id: new_user.id})
        db.query(NameChangeHistory).filter(NameChangeHistory.user_id == id).update({NameChangeHistory.user_id: new_user.id})
        db.query(ServiceCharacteristicHistory).filter(ServiceCharacteristicHistory.characteristic_initiator_id == id).update({ServiceCharacteristicHistory.characteristic_initiator_id: new_user.id})
        db.query(Candidate).filter(Candidate.recommended_by == id).update({Candidate.recommended_by: new_user.id})

        db.flush()
        print('flushed')
        self.remove(db, id)

        print('removed')
        
        make_transient(user)

        new_user.email = user.email
        new_user.call_sign = user.call_sign
        new_user.id_number = user.id_number
        
        db.add(new_user)
        db.flush() 
        return new_user


user_service = UserService(User)
