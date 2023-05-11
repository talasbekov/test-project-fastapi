import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from exceptions import NotFoundException, NotSupportedException
from models import (
    History,
    RankHistory,
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
    BadgeHistory,
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
    PersonalReserve,
    PrivilegeEmergency,
    User
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
    ServiceIDRead,
    HistoryRead,
    HistoryServiceDetailRead,
    HistoryPersonalRead,
    ServiceIdInfoRead
)

from services import (privelege_emergency_service, coolness_service, badge_service,
                      personnal_reserve_service, service_id_service, user_service,
                      recommender_user_service)


classes = {
    StaffUnit: 'emergency_service_history',
    Rank: 'rank_history',
    Penalty: 'penalty_history',
    Contract: 'contract_history',
    Secondment: 'secondment_history',
    NameChange: 'name_change_history',
    Attestation: 'attestation',
    Status: 'status_history',
    Coolness: 'coolness_history',
    Badge: 'badge_history',
}

options = {
    'rank_history': RankHistory,
    'penalty_history': PenaltyHistory,
    'contract_history': ContractHistory,
    'emergency_service_history': EmergencyServiceHistory,
    'work_experience_history': WorkExperienceHistory,
    'secondment_history': SecondmentHistory,
    'attestation': AttestationHistory,
    'name_change_history': NameChangeHistory,
    'status_history': StatusHistory,
    'coolness_history': CoolnessHistory,
    'service_characteristic_history': ServiceCharacteristicHistory,
    'badge_history': BadgeHistory,
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
    return last_history


class HistoryService(ServiceBase[History, HistoryCreate, HistoryUpdate]):

    def get_by_type(self, db: Session, type: str):
        histories = db.query(self.model).filter(self.model.type == type).all()

        lis_of_histories = []
        for history in histories:
            lis_of_histories.append(HistoryRead.from_orm(history).to_dict())
        return lis_of_histories

    def get_all_by_type(self, db: Session, type: str, skip: int, limit: int):
        histories = db.query(self.model).filter(self.model.type == type).offset(skip).limit(limit).all()

        lis_of_histories = []
        for history in histories:
            lis_of_histories.append(HistoryRead.from_orm(history).to_dict())
        return lis_of_histories

    def get_all_by_type_and_user_id(self, db: Session, type: str, user_id: uuid.UUID, skip: int, limit: int):
        if type == 'beret_history':
            black_beret_type = badge_service.get_black_beret(db)
            black_beret = badge_service.get_badge_by_type(db, black_beret_type.id)
            histories = (
                db.query(BadgeHistory)
                .filter(
                    BadgeHistory.user_id == user_id,
                    BadgeHistory.badge_id == black_beret.id
                )
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            histories = (
                db.query(self.model)
                .filter(
                    self.model.type == type,
                    self.model.user_id == user_id
                )
                .offset(skip)
                .limit(limit)
                .all()
            )

        lis_of_histories = []
        for history in histories:
            lis_of_histories.append(HistoryRead.from_orm(history).to_dict())
        return lis_of_histories

    def create(self, db: Session, obj_in: HistoryCreate):
        cls = options.get(obj_in.type) 
        if cls is None:
            raise NotSupportedException(detail=f'Type: {obj_in.type} is not supported!')
        if hasattr(cls, "badge_id"):
            badge = badge_service.get_by_id(db, obj_in.badge_id)
            if badge is None:
                raise NotFoundException(detail=f'Badge with id: {obj_in.badge_id} not found!')
        obj_db = cls(**obj_in.dict(exclude_none=True))
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db
    
    def get_type_by_user_id(self, db: Session, user_id: str, type: str):
        cls = options.get(type)
        if cls is None:
            raise NotSupportedException(detail=f'Type: {type} is not supported!')
        return cls

    def get_all_by_user_id(self, db: Session, user_id: str):
        user = user_service.get_by_id(db, user_id)
        general_information = self.get_general_information_by_user_id(db, user_id, user)        
        badges = db.query(BadgeHistory).filter(BadgeHistory.user_id == user_id).all()
        ranks = db.query(RankHistory).filter(RankHistory.user_id == user_id).all()
        penalties = db.query(PenaltyHistory).filter(PenaltyHistory.user_id == user_id).all()
        contracts = db.query(ContractHistory).filter(ContractHistory.user_id == user_id).all()
        attestations = db.query(AttestationHistory).filter(AttestationHistory.user_id == user_id).all()
        characteristics = db.query(ServiceCharacteristicHistory).filter(ServiceCharacteristicHistory.user_id == user_id).all()
        holidays = db.query(StatusHistory).filter(StatusHistory.user_id == user_id).all()
        emergency_contracts = db.query(EmergencyServiceHistory).filter(EmergencyServiceHistory.user_id == user_id).all()
        experience = db.query(WorkExperienceHistory).filter(WorkExperienceHistory.user_id == user_id).all()
        secondments = db.query(SecondmentHistory).filter(SecondmentHistory.user_id == user_id).all()
        equipments = user.equipments
        service_id_info =self.get_service_id_by_user_id(db, user_id)
        
        attendance = AttendanceRead(
            physical_training=100,
            tactical_training=100,
            shooting_training=100,
        )

        history_service_detail_read = HistoryServiceDetailRead(
            holidays=holidays,
            badges=badges,
            ranks=ranks,
            penalties=penalties,
            contracts=contracts,
            attestations=attestations,
            attendance=attendance,
            characteristics=characteristics,
            emergency_contracts=emergency_contracts,
            experience=experience,
            secondments=secondments,
            equipments=equipments,
            general_information=general_information,
            service_id_info=service_id_info
        )
        return history_service_detail_read


    def get_service_id_by_user_id(self, db: Session, user_id: str):
        service_id = service_id_service.get_by_user_id(db, user_id)
        if service_id is None:
            return None
        
        service_id_read = ServiceIdInfoRead(
            id=service_id.id,
            date_to=service_id.date_to,
            token_status=service_id.token_status,
            id_status=service_id.id_status,
            number=service_id.number,
        )
        return service_id_read
        

    
    def get_general_information_by_user_id(self, db: Session, user_id: str, user: User):
        oauth_user = db.query(UserOath).filter(UserOath.user_id == user_id).first()
        if oauth_user is None or oauth_user.military_unit is None:
            user_oath_read = None
        else:
            user_oath_read = OathRead(
                id=oauth_user.id,
                date=oauth_user.date, military_name=oauth_user.military_unit.name, military_id=oauth_user.military_unit_id)
        
        privelege_emergency = privelege_emergency_service.get_by_user_id(db, user_id)
        if privelege_emergency is None:
            privelege_emergency_read = None
        else:         
            privelege_emergency_read = PrivelegeEmergencyRead(
                date_from=privelege_emergency.date_from,
                date_to=privelege_emergency.date_to,
                form=privelege_emergency.form,
                id=privelege_emergency.id,
                user_id=privelege_emergency.user_id,
            )
        
        coolness = coolness_service.get_by_user_id(db, user_id)
        if coolness is None:
            coolness_read = None
        else:
            coolness_read = CoolnessRead(
                type_id=coolness.type_id,
                date_to=coolness.history.date_to,
                type=coolness.type,
                id=coolness.id,
                user_id=coolness.user_id,
            )
        
        black_beret = badge_service.get_black_beret_by_user_id(db, user_id)
        is_badge_black = False
        if black_beret:
            is_badge_black = True

        personal_reserve = personnal_reserve_service.get_by_user_id(db, user_id)
        if personal_reserve is None:
            personal_reserve_read = None
        else:
            personal_reserve_read = PersonnalReserveRead(
                date_from=personal_reserve.date_from,
                date_to=personal_reserve.date_to,
                id=personal_reserve.id,
                reserve=personal_reserve.reserve,
                user_id=personal_reserve.user_id,
                document_link=personal_reserve.document_link,
                document_number=personal_reserve.document_number
            )
        recommender = recommender_user_service.get_by_user_id(db, user_id)
        if recommender:
            recommender_user = {"name": recommender.user_by.last_name + ' '
                                        + recommender.user_by.first_name[0] + '.'
                                        + recommender.user_by.father_name[0] + '.',
                                "id": str(user.id)
                                }
        else:
            recommender_user = None
        if user:
            researcher = {"name": user.last_name + ' ' + user.first_name[0] + '.' + user.father_name[0] + '.',
                          "id": str(user.id)
                          }
        else:
            researcher = None

        general_information_read = GeneralInformationRead(
            oath=user_oath_read,
            privilege_emergency_secrets=privelege_emergency_read,
            personnel_reserve=personal_reserve_read,
            coolness=coolness_read,
            is_badge_black=is_badge_black,
            researcher=researcher,
            recommender=recommender_user
        )


        return general_information_read

    def create_history(self, db: Session, user_id: uuid.UUID, object):
        diff = classes.get(type(object))
        if diff is None:
            raise NotSupportedException(detail=f'Type: {diff} is not supported!')
        cls = options.get(diff)
        if cls is None:
            raise NotSupportedException(detail=f'In options: {diff} is not present!')
        return cls.create_history(db, user_id, object.id, finish_last)

    def create_timeline_history(
        self,
        db: Session,
        user_id: uuid.UUID,
        object,
        date_from: datetime,
        date_to: datetime,
    ):
        diff = classes.get(type(object))
        if diff is None:
            raise NotSupportedException(detail=f"Type: {diff} is not supported!")
        cls = options.get(diff)
        if cls is None:
            raise NotSupportedException(detail=f"In options: {diff} is not present!")
        if getattr(cls, "create_timeline_history", None) is None:
            raise NotSupportedException(
                detail=f"Class: {cls.__name__} does not support date_from, date_to format!"
            )
        return cls.create_timeline_history(
            db, user_id, object.id, finish_last, date_from, date_to
        )

    def update(self, db: Session, id: uuid.UUID, object: HistoryUpdate): 
        history = self.get_by_id(db, id)
        if history is None:
            raise NotFoundException(detail=f'History with id: {id} is not found!')
        for key, value in object.dict(exclude_unset=True).items():
            setattr(history, key, value)
        db.add(history)
        db.flush()
        return history


    def get_all_personal(self, db: Session, user_id: uuid.UUID, date_from, skip: int = 0, limit: int = 100):
        if date_from is None:
            histories = (
                db.query(self.model)
                .filter(self.model.user_id == user_id)
                .order_by(self.model.date_from.desc(), self.model.id.asc())  # add secondary sort order
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            start_date = date_from.replace(day=1)
            next_month = date_from.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
            histories = (
                db.query(self.model)
                .filter(self.model.user_id == user_id, self.model.date_from >= start_date, self.model.date_from <= end_date)
                .order_by(self.model.date_from.desc(), self.model.id.asc())  # add secondary sort order
                .offset(skip)
                .limit(limit)
                .all()
            )
        lis_of_histories = []
        for history in histories:
            type_cls = self.get_type_by_user_id(db, user_id, history.type)
            obj = db.query(type_cls).filter(type_cls.id == history.id).first()
            lis_of_histories.append(HistoryPersonalRead.from_orm(obj).to_dict())
        return lis_of_histories


history_service = HistoryService(History)
