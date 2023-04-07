import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from exceptions import NotFoundException, NotSupportedException
from models import (
    History,
    RankHistory,
    StaffUnitHistory,
    PenaltyHistory,
    ContractHistory,
    EmergencyServiceHistory,
    WorkExperienceHistory,
    SecondmentHistory,
    NameChangeHistory,
    AttestationHistory,
    ServiceCharacteristicHistory,
    StatusHistory,
    CoolnessHistory,
    UserOath,
    StaffUnit,
    Rank,
    Penalty,
    Contract,
    Secondment,
    NameChange,
    Attestation,
    Status,
    Badge,
    Coolness,
    PersonnalReserve,
    PrivelegeEmergency,
)
from schemas import HistoryCreate, HistoryUpdate
from services import ServiceBase


from schemas import (
    OathRead,
    PrivelegeEmergencyRead,
    PersonnalReserveRead,
    GeneralInformationRead,
    CoolnessRead,
    AttendanceRead,
    ServiceIDRead
    
)

from services import (privelege_emergency_service, coolness_service, badge_service,
                      personnal_reserve_service, service_id_service)


classes = {
    StaffUnit: 'staff_unit_history',
    Rank: 'rank_history',
    Penalty: 'penalty_history',
    Contract: 'contract_history',
    Secondment: 'secondment_history',
    NameChange: 'name_change_history',
    Attestation: 'attestation_history',
    Status: 'status_history',
    Coolness: 'coolness_history'
}

options = {
    'staff_unit_history': StaffUnitHistory,
    'rank_history': RankHistory,
    'penalty_history': PenaltyHistory,
    'contract_history': ContractHistory,
    'emergency_service_history': EmergencyServiceHistory,
    'work_experience_history': WorkExperienceHistory,
    'secondment_history': SecondmentHistory,
    'name_change_history': NameChangeHistory,
    'attestation_history': AttestationHistory,
    'service_characteristic_history': ServiceCharacteristicHistory,
    'status_history': StatusHistory,
    'coolness_history': CoolnessHistory
}


def get_last_by_user_id(db: Session, user_id: str, type: str):
    cls: History = options.get(type)
    if cls is None:
        raise NotSupportedException(detail=f'Type: {type} is not supported!')
    res = db.query(cls).filter(
        cls.user_id == user_id,
        cls.date_to == None
    ).order_by(cls.date_to.desc()).first()
    return res

def finish_last(db: Session, user_id: str, type: str):
    last_history: History = get_last_by_user_id(db, user_id, type)
    if last_history is None:
        return
    last_history.date_to = datetime.now()
    db.add(last_history)
    db.flush()


class HistoryService(ServiceBase[History, HistoryCreate, HistoryUpdate]):
    def get_by_type(self, db: Session, type: str):
        return db.query(self.model).filter(self.model.type == type).first()

    def get_all_by_type(self, db: Session, type: str):
        return db.query(self.model).filter(self.model.type == type).all()
    def create(self, db: Session, obj_in: HistoryCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(detail=f'Type: {obj_in.type} is not supported!')
        obj_in = cls(**obj_in.dict())
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        return db_obj

    def get_type_by_user_id(self, db: Session, user_id: str, type: str):
        cls = options.get(type)
        if cls is None:
            raise NotSupportedException(detail=f'Type: {type} is not supported!')
        return cls

    def get_all_by_user_id(self, db: Session, user_id: str):
        general_info_read = self.get_general_information_by_user_id(db, user_id)
        attendance_read = AttendanceRead(
            physical_training=100,
            shooting_training=100,
            tactical_training=100
        )
        service_id_read = self.get_service_id_by_user_id(db, user_id)

    

    def get_service_id_by_user_id(self, db: Session, user_id: str):
        service_id = service_id_service.get_by_user_id(db, user_id)
        service_id_read = ServiceIDRead(
            id=service_id.id,
            date_to=service_id.date_to,
            id_status=service_id.id_status,
            number=service_id.number,
            token_status=service_id.token_status,
            user_id=service_id.user_id
        )
        return service_id_read
        

    
    def get_general_information_by_user_id(self, db: Session, user_id: str):
        oauth_user = db.query(UserOath).filter(UserOath.user_id == user_id).first()
        if oauth_user is None or oauth_user.military_unit is None:
            raise NotFoundException(detail=f'User with id: {user_id} not found!')
        user_oath_read = OathRead(date=oauth_user.date, military_name=oauth_user.military_unit.name)
        privelege_emergency = privelege_emergency_service.get_by_user_id(db, user_id)
        privelege_emergency_read = PrivelegeEmergencyRead(
            date_from=privelege_emergency.date_from,
            date_to=privelege_emergency.date_to,
            form=privelege_emergency.form,
            id=privelege_emergency.id,
        )
        coolness = coolness_service.get_by_user_id(db, user_id)
        coolness_read = CoolnessRead(
            date_from=coolness.date_from,
            date_to=coolness.date_to,
            speciality=coolness.speciality,
            id=coolness.id,
        )
        black_beret = badge_service.get_black_beret_by_user_id(db, user_id)
        is_badge_black = False
        if black_beret:
            is_badge_black = True

        personnal_reseive = personnal_reserve_service.get_by_user_id(db, user_id)
        personnal_reseive_read = PersonnalReserveRead(
            date_from=personnal_reseive.date_from,
            date_to=personnal_reseive.date_to,
            id=personnal_reseive.id,
        )
        
        general_information_read = GeneralInformationRead(
            oath=user_oath_read,
            privilege_emergency_secrets=privelege_emergency_read,
            personnel_reserve=personnal_reseive_read,
            coolness=coolness_read,
            is_badge_black=is_badge_black,
            researcher='',
            recommendation=''
        )
        

        return general_information_read

    def create_history(self, db: Session, user_id: uuid.UUID,  object):
        diff = classes.get(type(object))
        if diff is None:
            raise NotSupportedException(detail=f'Type: {diff} is not supported!')
        cls = options.get(diff)
        if cls is None:
            raise NotSupportedException(detail=f'In options: {diff} is not present!')
        cls.create_history(db, user_id, object.id, finish_last)


history_service = HistoryService(History)
