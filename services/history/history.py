import json
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from typing import List
from sqlalchemy.orm import Session
from services import rank_service

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
    CoolnessStatusEnum,
    User, BadgeType, ReserveEnum,
    PermissionTypeEnum
)
from schemas import HistoryCreate, HistoryUpdate
from schemas.history.history import EquipmentRead
from services import ServiceBase


from schemas import (
    OathRead,
    PrivelegeEmergencyRead,
    PersonnalReserveRead,
    GeneralInformationRead,
    CoolnessRead,
    AttendanceRead,
    HistoryRead,
    HistoryServiceDetailRead,
    HistoryPersonalRead,
    ServiceIdInfoRead,
    HistoryTimeLineRead,
    HistoryContractCreate,
    HistoryBadgeCreate,
    HistoryRankCreate,
    HistorySecondmentCreate,
    HistoryPenaltyCreate,
    HistoryStatusCreate,
    HistoryCoolnessCreate,
    HistoryAttestationCreate,
    HistoryBlackBeretCreate,
    BlackBeretRead,
    RecommenderUserRead
)

from services import (privelege_emergency_service, coolness_service, badge_service,
                      personnal_reserve_service, service_id_service, user_service,
                      recommender_user_service, contract_service, driving_license_service,
                      identification_card_service, passport_service, profile_service,
                      secondment_service, staff_division_service, penalty_service,
                      status_service, rank_service)


classes = {
    StaffUnit: 'emergency_history',
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
    'emergency_history': EmergencyServiceHistory,
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
        cls.date_to is None
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

    def get_by_id(self, db: Session, id: str) -> History:
        history = self.get(db, id)
        if type(history) == EmergencyServiceHistory:
            if history.staff_division is not None:
                if isinstance(history.staff_division.description, str):
                    history.staff_division.description = json.loads(
                        history.staff_division.description)
        if history is None:
            raise NotFoundException(
                detail=f"History with id {id} not found!")
        return history

    def get_by_type(self, db: Session, type: str):
        histories = db.query(self.model).filter(self.model.type == type).all()

        lis_of_histories = []
        for history in histories:
            lis_of_histories.append(HistoryRead.from_orm(history).to_dict())
        return lis_of_histories

    def get_all(self, db: Session, skip: int, limit: int):
        histories = db.query(self.model).offset(skip).limit(limit).all()

        list_of_histories = []
        for history in histories:
            list_of_histories.append(HistoryRead.from_orm(history).to_dict())
        return list_of_histories

    def get_all_by_type(self, db: Session, type: str, skip: int, limit: int):
        histories = self._get_all_by_type(
            db, type).offset(skip).limit(limit).all()

        list_of_histories = []
        for history in histories:
            list_of_histories.append(HistoryRead.from_orm(history).to_dict())
        return list_of_histories

    def _get_all_by_type(self, db: Session, type: str):
        return db.query(self.model).filter(self.model.type == type)

    def get_all_by_type_and_user_id(
            self, db: Session, type: str, user_id: str, skip: int, limit: int):
        if type == 'beret_history':
            black_beret = badge_service.get_black_beret_by_user_id(db, user_id)
            if black_beret is None:
                return []
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
                self._get_all_by_type_and_user_id(db, type, user_id)
                .offset(skip)
                .limit(limit)
                .all()
            )

        lis_of_histories = []
        for history in histories:
            lis_of_histories.append(HistoryRead.from_orm(history).to_dict())
        return lis_of_histories

    def _get_all_by_type_and_user_id(self, db: Session, type: str, user_id):
        return db.query(self.model).filter(self.model.type ==
                                           type, self.model.user_id == user_id)

    def create(self, db: Session, obj_in: HistoryCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        if hasattr(cls, "badge_id"):
            badge = badge_service.get_by_id(db, obj_in.badge_id)
            if badge is None:
                raise NotFoundException(
                    detail=f'Badge with id: {obj_in.badge_id} not found!')
        # Фильтруем данные:
        model_columns = {c.name for c in cls.__table__.columns}
        data = {
            k: v for k, v in obj_in.dict(exclude_none=True).items()
            if k in model_columns
        }

        obj_db = cls(**data)
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db

    def create_contract_history(self, db: Session, obj_in: HistoryContractCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        contract = contract_service.create_relation(
            db, obj_in.user_id, obj_in.contract_type_id)
        obj_data = {
            "user_id": obj_in.user_id,
            "contract_id": contract.id,
            "type": obj_in.type,
            "document_number": obj_in.document_number,
            "date_from": obj_in.date_from,
            "date_to": obj_in.date_to if obj_in.date_to is not None else None,
            "experience_years": obj_in.experience_years,
            "date_credited": obj_in.date_credited,
        }
        obj_db = cls(**obj_data)
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db

    def create_badge_history(self, db: Session, obj_in: HistoryBadgeCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        badge = badge_service.create_relation(
            db, obj_in.user_id, obj_in.badge_type_id)
        obj_data = {
            "user_id": obj_in.user_id,
            "badge_id": badge.id,
            "type": obj_in.type,
            "document_number": obj_in.document_number,
            "date_from": obj_in.date_from,
            "date_to": obj_in.date_to if obj_in.date_to is not None else None,
            "reason": obj_in.reason,
            "reasonKZ": obj_in.reasonKZ,
        }
        obj_db = cls(**obj_data)
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db
    
    def create_rank_history(self, db: Session, obj_in: HistoryRankCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        #rank = rank_service.create_relation(db, obj_in.user_id, obj_in.rank_id)
        obj_data = {
            "user_id": obj_in.user_id,
            "rank_id": obj_in.rank_id,
            "type": obj_in.type,
            "document_number": obj_in.document_number,
            "date_from": obj_in.date_from,
            #"date_to": obj_in.date_to if obj_in.date_to is not None else None,
            "early_promotion": obj_in.early_promotion,
            "rank_assigned_by": obj_in.rank_assigned_by,
        }
        obj_db = cls(**obj_data)
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db
    
    def create_black_beret_history(self, db: Session, obj_in: HistoryBlackBeretCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        black_beret_type = badge_service.get_black_beret(db)
        badge = badge_service.create_relation(
            db, obj_in.user_id, black_beret_type.id)
        obj_data = {
            "user_id": obj_in.user_id,
            "badge_id": badge.id,
            "type": obj_in.type,
            "document_number": obj_in.document_number,
            "date_from": obj_in.date_from,
        }
        obj_db = cls(**obj_data)
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db

    def create_secondment_history(self, db: Session, obj_in: HistorySecondmentCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        if obj_in.staff_division_id:
            staff_division = staff_division_service.get_by_id(
                db, obj_in.staff_division_id)
            secondment = secondment_service.create_relation(
                db, obj_in.user_id, staff_division)
        else:
            secondment = secondment_service.create_relation(
                db, obj_in.user_id, obj_in.value)
        obj_data = {
            "user_id": obj_in.user_id,
            "secondment_id": secondment.id,
            "type": obj_in.type,
            "document_number": obj_in.document_number,
            "date_from": obj_in.date_from,
            "date_to": obj_in.date_to if obj_in.date_to is not None else None
        }
        obj_db = cls(**obj_data)
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db

    def create_penalty_history(self, db: Session, obj_in: HistoryPenaltyCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        penalty = penalty_service.create_relation(
            db, obj_in.user_id, obj_in.penalty_type_id)
        obj_data = {
            "user_id": obj_in.user_id,
            "penalty_id": penalty.id,
            "type": obj_in.type,
            "document_number": obj_in.document_number,
            "date_from": obj_in.date_from,
            "date_to": obj_in.date_to if obj_in.date_to is not None else None,
            "reason": obj_in.reason,
            "reasonKZ": obj_in.reasonKZ
        }
        obj_db = cls(**obj_data)
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db

    def create_status_history(self, db: Session, obj_in: HistoryStatusCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        status = status_service.create_relation(
            db, obj_in.user_id, obj_in.status_type_id)
        obj_data = {
            "user_id": obj_in.user_id,
            "status_id": status.id,
            "type": obj_in.type,
            "document_number": obj_in.document_number,
            "date_from": obj_in.date_from,
            "date_to": obj_in.date_to if obj_in.date_to is not None else None
        }
        obj_db = cls(**obj_data)
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db

    def create_coolness_history(self, db: Session, obj_in: HistoryCoolnessCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        coolness = coolness_service.create_relation(
            db, obj_in.user_id, obj_in.coolness_type_id, obj_in.coolness_status)
        obj_data = {
            "user_id": obj_in.user_id,
            "coolness_id": coolness.id,
            "type": obj_in.type,
            "document_number": obj_in.document_number,
            "date_from": obj_in.date_from,
            "date_to": obj_in.date_to if obj_in.date_to is not None else None
        }
        obj_db = cls(**obj_data)
        db.add(obj_db)
        db.flush()
        db.refresh(obj_db)
        return obj_db

    def create_attestation_history(self, db: Session, obj_in: HistoryAttestationCreate):
        cls = options.get(obj_in.type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {obj_in.type} is not supported!')
        attesation = Attestation(**{"user_id": obj_in.user_id})
        obj_data = {
            "user_id": obj_in.user_id,
            "attestation_id": attesation.id,
            "type": obj_in.type,
            "document_number": obj_in.document_number,
            "date_from": obj_in.date_from,
            "attestation_status": obj_in.attestation_status,
            "attestation_statusKZ": obj_in.attestation_statusKZ,
            "date_to": obj_in.date_to if obj_in.date_to is not None else None,
            "date_credited": obj_in.date_credited
        }
        obj_db = cls(**obj_data)
        db.add(obj_db)
        db.add(attesation)
        db.flush()
        db.refresh(obj_db)
        return obj_db

    def get_type_by_user_id(self, db: Session, user_id: str, type: str):
        cls = options.get(type)
        if cls is None:
            raise NotSupportedException(
                detail=f'Type: {type} is not supported!')
        return cls

    def get_all_by_user_id(self, db: Session, user_id: str, requester_id: str, permissions: List[int]):
        user = user_service.get_by_id(db, user_id)
        general_information = self.get_general_information_by_user_id(
            db, user_id, user)
        badges = db.query(BadgeHistory).filter(
            BadgeHistory.user_id == user_id).order_by(BadgeHistory.date_from.desc()).all()
        ranks = db.query(RankHistory).filter(RankHistory.user_id == user_id).order_by(RankHistory.date_from.desc()).all()
        # for rank in ranks:
        #     print(rank.__dict__)
        #     if rank.rank is not None:
        #         rank = rank.rank
        rank = user_service.get_by_id(db, user_id).rank
        penalties = db.query(PenaltyHistory).filter(
            PenaltyHistory.user_id == user_id).order_by(PenaltyHistory.date_from.desc()).all()
        contracts = db.query(ContractHistory).filter(
            ContractHistory.user_id == user_id).order_by(ContractHistory.date_from.desc()).all()
        if user_id==requester_id or int(PermissionTypeEnum.VIEW_ATTESTATION.value) in permissions:
            attestations = db.query(AttestationHistory).filter(
                AttestationHistory.user_id == user_id).order_by(AttestationHistory.date_from.desc()).all()
        else:
            attestations = "Permission Denied"
        if user_id==requester_id or int(PermissionTypeEnum.VIEW_SERVICE_CHARACTERISTICS.value) in permissions:
            characteristics = db.query(ServiceCharacteristicHistory).filter(
                ServiceCharacteristicHistory.user_id == user_id).order_by(ServiceCharacteristicHistory.date_from.desc()).all()
        else: 
            characteristics = "Permission Denied"
        holidays = db.query(StatusHistory).filter(
            StatusHistory.user_id == user_id).order_by(StatusHistory.date_from.desc()).all()
        emergency_contracts = db.query(EmergencyServiceHistory).filter(
            EmergencyServiceHistory.user_id == user_id).order_by(EmergencyServiceHistory.date_from.desc()).all()
        experience = db.query(WorkExperienceHistory).filter(
            WorkExperienceHistory.user_id == user_id).order_by(WorkExperienceHistory.date_from.desc()).all()
        secondments = db.query(SecondmentHistory).filter(
            SecondmentHistory.user_id == user_id).order_by(SecondmentHistory.date_from.desc()).all()
        
        for i in emergency_contracts:
            if i.position is not None:
                print(i.position.__dict__)

        # print("HEEEEEERE")
        # print(i.__dict__ for i in secondments)
        equipments = user.equipments

        # clothing_equipments_type_count = (
        #     equipment_service
        #     .get_clothing_equipments_type_count(db)
        # )

        # equipment_models_count = (
        #     equipment_service
        #     .get_clothing_equipment_models_count_by_user(
        #         db,
        #         user_id
        #     )
        # )
        # percentage = {}
        # if equipment_models_count:
        #     for equipment_model in equipment_models_count:
        #         percentage[equipment_model[0]] = (
        #             equipment_model[1] * 100) / clothing_equipments_type_count
        try:
            service_id_info = self.get_service_id_by_user_id(db, user_id)
        except Exception as e:
            print(e)
        
        # equipments_dict = [EquipmentRead.from_orm(
        #     equipment).dict() for equipment in equipments]
        # equipments_dict.append(percentage)

        attendance = AttendanceRead(
            physical_training=100,
            tactical_training=100,
            shooting_training=100,
        )

        history_service_detail_read = HistoryServiceDetailRead(
            holidays=holidays,
            badges=badges,
            rank=rank if rank is not None else None,
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
        additional_emergency_length = {"years":0, "months":0, "days":0}
        for experience in history_service_detail_read.experience:
            if experience.is_credited:
                additional_emergency_length["years"] += experience.length_of_service["years"]
                additional_emergency_length["months"] += experience.length_of_service["months"]
                additional_emergency_length["days"] += experience.length_of_service["days"]
        if history_service_detail_read.emergency_contracts and len(history_service_detail_read.emergency_contracts) > 0:
            emergency_contract = history_service_detail_read.emergency_contracts[0]
            if emergency_contract.length_of_service is None:
                emergency_contract.length_of_service = {"years": 0, "months": 0, "days": 0}
            emergency_contract.length_of_service["years"] += additional_emergency_length["years"]
            emergency_contract.length_of_service["months"] += additional_emergency_length["months"]
            emergency_contract.length_of_service["days"] += additional_emergency_length["days"]
        history_dict = HistoryServiceDetailRead.from_orm(
            history_service_detail_read).dict()
        return history_dict

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
            token_number=service_id.token_number
        )
        return service_id_read

    def get_service_id_by_user_id_and_date(self, db: Session, user_id: str, date_till):
        service_id = service_id_service.get_by_user_id_and_date(db, user_id, date_till)
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

    def get_general_information_by_user_id(
            self, db: Session, user_id: str, user: User):
        oauth_user = db.query(UserOath).filter(
            UserOath.user_id == user_id).first()
        if oauth_user is None or oauth_user.military_unit is None:
            user_oath_read = None
        else:
            user_oath_read = OathRead(
                id=oauth_user.id,
                date=oauth_user.date,
                military_name=oauth_user.military_unit,
                military_nameKZ=oauth_user.military_unit,
                military_id=oauth_user.military_unit
            )

        privelege_emergency = privelege_emergency_service.get_by_user_id(
            db, user_id)
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

        coolnesses = coolness_service.get_by_user_id(db, user_id)
        coolnesses_list = []
        if coolnesses is None:
            coolness_read = None
        else:
            for coolness in coolnesses:
                coolness_read = CoolnessRead(
                    type_id=coolness.type_id,
                    # date_to=coolness.history.date_to,
                    type=coolness.type,
                    id=coolness.id,
                    user_id=coolness.user_id,
                    coolness_status=coolness.coolness_status.value,
                )
                coolnesses_list.append(coolness_read)
        # HERE!
        black_beret_badge = badge_service.get_black_beret_by_user_id(db, user_id)
        # print('black_beret_badge')
        # print(black_beret_badge.id)
        if black_beret_badge is not None:
            # print("here1")
            black_beret = db.query(BadgeHistory).filter(
                BadgeHistory.user_id == user_id,
                BadgeHistory.badge_id == black_beret_badge.id,
                # BadgeHistory.date_to == None
            ).first()
            # print('black_beret')
            # print(black_beret is None)
            if black_beret is not None:
                black_beret = BlackBeretRead(
                    id=black_beret.id,
                    badge_id=black_beret.badge_id,
                    date_from=black_beret.date_from,
                    document_number=black_beret.document_number
                )
                # print(black_beret.id)
        else:
            # print("here_null")
            black_beret = None
            
        personal_reserve = personnal_reserve_service.get_by_user_id(
            db, user_id)
        if personal_reserve is None:
            personal_reserve_read = None
        else:
            personal_reserve_read = PersonnalReserveRead(
                reserve_date=personal_reserve.reserve_date,
                id=personal_reserve.id,
                reserve=personal_reserve.reserve,
                user_id=personal_reserve.user_id,
                document_link=personal_reserve.document_link,
                document_number=personal_reserve.document_number
            )
        recommender = recommender_user_service.get_by_user_id(db, user_id)
        #fulfill recommender RecommenderUserRead schema
        if recommender is not None:
            recommender = RecommenderUserRead(
                id=recommender.id,
                user_id=recommender.user_id,
                recommendant=recommender.recommendant,
                researcher=recommender.researcher,
                document_link=recommender.document_link,
                researcher_id=recommender.researcher_id,
                user_by_id=recommender.user_by_id
            )

        general_information_read = GeneralInformationRead(
            oath=user_oath_read,
            privilege_emergency_secrets=privelege_emergency_read,
            personnel_reserve=personal_reserve_read,
            coolness=coolnesses_list,
            black_beret=black_beret,
            recommender=recommender
        )

        return general_information_read

    def get_general_information_by_user_id_and_date(
            self, db: Session, user_id: str, user: User, date_till):
        oauth_user = db.query(UserOath).filter(
            UserOath.user_id == user_id,
            UserOath.date <= date_till
        ).first()
        if oauth_user is None or oauth_user.military_unit is None:
            user_oath_read = None
        else:
            user_oath_read = OathRead(
                id=oauth_user.id,
                date=oauth_user.date,
                military_name=oauth_user.military_unit.name,
                military_nameKZ=oauth_user.military_unit.nameKZ,
                military_id=oauth_user.military_unit_id
            )

        privelege_emergency = privelege_emergency_service.get_by_user_id_and_date(
            db, user_id, date_till)
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

        coolnesses = coolness_service.get_by_user_id_and_date(db, user_id, date_till)
        coolnesses_list = []
        if coolnesses is None:
            coolness_read = None
        else:
            for coolness in coolnesses:
                coolness_read = CoolnessRead(
                    type_id=coolness.type_id,
                    # date_to=coolness.history.date_to,
                    type=coolness.type,
                    id=coolness.id,
                    user_id=coolness.user_id,
                    coolness_status=coolness.coolness_status.value,
                )
                coolnesses_list.append(coolness_read)

        black_beret_badge = badge_service.get_black_beret_by_user_id_and_date(db,
                                                                              user_id,
                                                                              date_till)
        if black_beret_badge is not None:
            black_beret = db.query(BadgeHistory).filter(
                BadgeHistory.user_id == user_id,
                BadgeHistory.badge_id == black_beret_badge.id,
                BadgeHistory.date_from <= date_till,
                BadgeHistory.date_to == None
            ).first()

            if black_beret is not None:
                black_beret = BlackBeretRead(
                    id=black_beret.id,
                    badge_id=black_beret.badge_id,
                    date_from=black_beret.date_from,
                    document_number=black_beret.document_number
                )
        else:
            black_beret = None

        personal_reserve = personnal_reserve_service.get_by_user_id_and_date(
            db, user_id, date_till)
        if personal_reserve is None:
            personal_reserve_read = None
        else:
            personal_reserve_read = PersonnalReserveRead(
                reserve_date=personal_reserve.reserve_date,
                id=personal_reserve.id,
                reserve=personal_reserve.reserve,
                user_id=personal_reserve.user_id,
                document_link=personal_reserve.document_link,
                document_number=personal_reserve.document_number
            )
        recommender = recommender_user_service.get_by_user_id_and_date(db,
                                                                       user_id,
                                                                       date_till)
        # fulfill recommender RecommenderUserRead schema
        if recommender is not None:
            recommender = RecommenderUserRead(
                id=recommender.id,
                user_id=recommender.user_id,
                recommendant=recommender.recommendant,
                researcher=recommender.researcher,
                document_link=recommender.document_link
            )

        general_information_read = GeneralInformationRead(
            oath=user_oath_read,
            privilege_emergency_secrets=privelege_emergency_read,
            personnel_reserve=personal_reserve_read,
            coolness=coolnesses_list,
            black_beret=black_beret,
            recommender=recommender
        )

        return general_information_read

    def create_history(self, db: Session, user_id: str, object):
        diff = classes.get(type(object))
        if diff is None:
            raise NotSupportedException(
                detail=f'Type: {diff} is not supported!')
        cls = options.get(diff)
        if cls is None:
            raise NotSupportedException(
                detail=f'In options: {diff} is not present!')
        return cls.create_history(db, user_id, object.id, finish_last)

    def create_timeline_history(
        self,
        db: Session,
        user_id: str,
        object,
        date_from: datetime,
        date_to: datetime,
    ):
        diff = classes.get(type(object))
        if diff is None:
            raise NotSupportedException(
                detail=f"Type: {diff} is not supported!")
        cls = options.get(diff)
        if cls is None:
            raise NotSupportedException(
                detail=f"In options: {diff} is not present!")
        if getattr(cls, "create_timeline_history", None) is None:
            raise NotSupportedException(
                detail=(f"Class: {cls.__name__} "
                        "does not support date_from, date_to format!")
            )
        return cls.create_timeline_history(
            db, user_id, object.id, finish_last, date_from, date_to
        )

    def update_secondment(self, db: Session, id: str, object: HistoryUpdate):
        history = self.get_by_id(db, id)
        if history is None:
            raise NotFoundException(
                detail=f'History with id: {id} is not found!')
        for key, value in object.dict(exclude_unset=True).items():
            setattr(history, key, value)
        if history.secondment_id:
            staff_division = staff_division_service.get_by_id(db, object.staff_division_id)
            history.secondment.staff_division_id = staff_division.id
            history.secondment.name = staff_division.name
            history.secondment.nameKZ = staff_division.nameKZ
        else:
            raise NotFoundException(
                detail=f'Secondment is not found!')
        setattr(history, 'updated_at', datetime.now())
        db.add(history)
        db.commit()
        return history

    def update_badge(self, db: Session, id: str, object: HistoryUpdate):
        history = self.get_by_id(db, id)
        if history is None:
            raise NotFoundException(
                detail=f'History with id: {id} is not found!')
        for key, value in object.dict(exclude_unset=True).items():
            setattr(history, key, value)
        if history.badge_id:
            badge = badge_service.get_by_id(db, history.badge_id)
            history.badge.type_id = object.badge_type_id
        else:
            raise NotFoundException(
                detail=f'Badge is not found!')
        setattr(history, 'updated_at', datetime.now())
        db.add(history)
        db.commit()
        return history

    def update_rank(self, db: Session, id: str, object: HistoryUpdate):
        history = self.get_by_id(db, id)
        if history is None:
            raise NotFoundException(
                detail=f'History with id: {id} is not found!')
        for key, value in object.dict(exclude_unset=True).items():
            setattr(history, key, value)
        if history.rank_id:
            rank = rank_service.get_by_id(db, history.rank_id)
            history.rank.type_id = object.rank_type_id
        else:
            raise NotFoundException(
                detail=f'Rank is not found!')
        setattr(history, 'updated_at', datetime.now())
        db.add(history)
        db.commit()
        return history


    def update_status(self, db: Session, id: str, object: HistoryUpdate):
        history = self.get_by_id(db, id)
        if history is None:
            raise NotFoundException(
                detail=f'History with id: {id} is not found!')
        for key, value in object.dict(exclude_unset=True).items():
            setattr(history, key, value)
        if history.status_id:
            status = status_service.get_by_id(db, history.status_id)
            history.status.type_id = object.status_type_id
        else:
            raise NotFoundException(
                detail=f'Status is not found!')
        setattr(history, 'updated_at', datetime.now())
        db.add(history)
        db.commit()
        return history

    def update(self, db: Session, id: str, object: HistoryUpdate):
        history = self.get_by_id(db, id)
        if history is None:
            raise NotFoundException(
                detail=f'History with id: {id} is not found!')
        for key, value in object.dict(exclude_unset=True).items():
            setattr(history, key, value)
        setattr(history, 'updated_at', datetime.now())
        db.add(history)
        db.commit()
        return history

    def get_all_personal(self, db: Session, user_id: str,
                         date_from, date_to, skip: int = 0, limit: int = 100):
        if date_to is not None:
            histories = (
                db.query(self.model)
                .filter(self.model.user_id == user_id,
                        self.model.date_from <= date_to)
                # add secondary sort order
                .order_by(self.model.date_from.desc(), self.model.id.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        elif date_from is not None:
            start_date = date_from.replace(day=1)
            next_month = date_from.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
            histories = (
                db.query(self.model)
                .filter(self.model.user_id == user_id,
                        self.model.date_from >= start_date,
                        self.model.date_from <= end_date)
                # add secondary sort order
                .order_by(self.model.date_from.desc(), self.model.id.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            histories = (
                db.query(self.model)
                .filter(self.model.user_id == user_id)
                # add secondary sort order
                .order_by(self.model.date_from.desc(), self.model.id.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        lis_of_histories = []
        for history in histories:
            type_cls = self.get_type_by_user_id(db, user_id, history.type)
            obj = db.query(type_cls).filter(type_cls.id == history.id).first()
            lis_of_histories.append(
                HistoryPersonalRead.from_orm(obj).to_dict())
        return lis_of_histories

    def has_penalty_history(self, db: Session, user_id: str) -> bool:
        penalty_history = (
            db.query(PenaltyHistory)
            .filter(PenaltyHistory.date_to == None,
                    PenaltyHistory.user_id == user_id)
            .first()
        )

        return penalty_history != None

    def get_timeline(self, db: Session, user_id: str):
        user = user_service.get_by_id(db, user_id)

        general_information = self.get_general_information_by_user_id(
            db, user_id, user)
        badges = (db.query(BadgeHistory)
                  .join(Badge, BadgeHistory.badge_id == Badge.id)
                  .join(BadgeType, Badge.type_id == BadgeType.id)
                  .filter(
            BadgeHistory.user_id == user_id,
            BadgeType.badge_order > 0
        ).all())
        ranks = db.query(RankHistory).filter(
            RankHistory.user_id == user_id).all()
        penalties = db.query(PenaltyHistory).filter(
            PenaltyHistory.user_id == user_id).all()
        contracts = db.query(ContractHistory).filter(
            ContractHistory.user_id == user_id).all()
        attestations = db.query(AttestationHistory).filter(
            AttestationHistory.user_id == user_id).all()
        characteristics = db.query(ServiceCharacteristicHistory).filter(
            ServiceCharacteristicHistory.user_id == user_id).all()
        holidays = db.query(StatusHistory).filter(
            StatusHistory.user_id == user_id).all()
        emergency_contracts = db.query(EmergencyServiceHistory).filter(
            EmergencyServiceHistory.user_id == user_id).all()
        experience = db.query(WorkExperienceHistory).filter(
            WorkExperienceHistory.user_id == user_id).all()
        secondments = db.query(SecondmentHistory).filter(
            SecondmentHistory.user_id == user_id).all()
        equipments = user.equipments
        driving_license = driving_license_service.get_by_user_id(db, user_id)
        identification_card = identification_card_service.get_by_user_id(
            db, user_id)
        passport = passport_service.get_by_user_id(db, user_id)
        educational_profile = profile_service.get_by_user_id(
            db, user_id).educational_profile
        academic_degrees = educational_profile.academic_degree
        academic_titles = educational_profile.academic_title
        educations = educational_profile.education
        courses = educational_profile.course

        service_id_info = self.get_service_id_by_user_id(db, user_id)
        # print(badges)
        timeline_read = HistoryTimeLineRead(
            badges=badges,
            rank = user.rank,
            ranks=ranks,
            contracts=contracts,
            emergency_contracts=emergency_contracts,
            equipments=equipments,
            driving_license=driving_license,
            identification_card=identification_card,
            passport=passport,
            academic_degrees=academic_degrees,
            academic_titles=academic_titles,
            educations=educations,
            courses=courses
        )
        # print("timeline:", timeline_read)
        timeline_dict = HistoryTimeLineRead.from_orm(
            timeline_read).dict()
        return timeline_dict

    def get_timeline_by_date(self, db: Session, user_id: str, date_till):
        user = user_service.get_by_id(db, user_id)

        general_information = self.get_general_information_by_user_id_and_date(
            db, user_id, user, datetime.combine(date_till, datetime.min.time()))
        badges = (db.query(BadgeHistory)
                  .join(Badge, BadgeHistory.badge_id == Badge.id)
                  .join(BadgeType, Badge.type_id == BadgeType.id)
                  .filter(
            BadgeHistory.user_id == user_id,
            BadgeHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            BadgeHistory.date_to <= datetime.combine(date_till, datetime.min.time()),
            BadgeType.badge_order > 0
        ).all())
        ranks = db.query(RankHistory).filter(
            RankHistory.user_id == user_id,
            RankHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            RankHistory.date_to <= datetime.combine(date_till, datetime.min.time())
        ).all()
        penalties = db.query(PenaltyHistory).filter(
            PenaltyHistory.user_id == user_id,
            PenaltyHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            PenaltyHistory.date_to <= datetime.combine(date_till, datetime.min.time())
        ).all()
        contracts = db.query(ContractHistory).filter(
            ContractHistory.user_id == user_id,
            ContractHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            ContractHistory.date_to <= datetime.combine(date_till,datetime.min.time())
        ).all()
        attestations = db.query(AttestationHistory).filter(
            AttestationHistory.user_id == user_id,
            AttestationHistory.date_credited <= datetime.combine(date_till, datetime.min.time()),
            AttestationHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            AttestationHistory.date_to <= datetime.combine(date_till, datetime.min.time())
        ).all()
        characteristics = db.query(ServiceCharacteristicHistory).filter(
            ServiceCharacteristicHistory.user_id == user_id,
            ServiceCharacteristicHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            ServiceCharacteristicHistory.date_to <= datetime.combine(date_till, datetime.min.time())
        ).all()
        holidays = db.query(StatusHistory).filter(
            StatusHistory.user_id == user_id,
            StatusHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            StatusHistory.date_to <= datetime.combine(date_till, datetime.min.time())
        ).all()
        emergency_contracts = db.query(EmergencyServiceHistory).filter(
            EmergencyServiceHistory.user_id == user_id,
            EmergencyServiceHistory.date_credited <= datetime.combine(date_till, datetime.min.time()),
            EmergencyServiceHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            EmergencyServiceHistory.date_to <= datetime.combine(date_till, datetime.min.time())
        ).all()
        experience = db.query(WorkExperienceHistory).filter(
            WorkExperienceHistory.user_id == user_id,
            WorkExperienceHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            WorkExperienceHistory.date_to <= datetime.combine(date_till, datetime.min.time())
        ).all()
        secondments = db.query(SecondmentHistory).filter(
            SecondmentHistory.user_id == user_id,
            SecondmentHistory.date_from <= datetime.combine(date_till, datetime.min.time()),
            SecondmentHistory.date_to <= datetime.combine(date_till, datetime.min.time())
        ).all()
        equipments = [equipment
                      for equipment in user.equipments
                      if equipment.date_from <= datetime.combine(date_till, datetime.min.time())
                      and equipment.date_to is not None
                      and equipment.date_to <= datetime.combine(date_till, datetime.min.time())]
        driving_license = driving_license_service.get_by_user_id_and_date(
            db, user_id, datetime.combine(date_till, datetime.min.time()))
        identification_card = identification_card_service.get_by_user_id_and_date(
            db, user_id, datetime.combine(date_till, datetime.min.time()))
        passport = passport_service.get_by_user_id_and_date(
            db, user_id, datetime.combine(date_till, datetime.min.time()))
        educational_profile = profile_service.get_by_user_id(
            db, user_id).educational_profile
        academic_degrees = [academic_degree
                            for academic_degree in educational_profile.academic_degree
                            if academic_degree.assignment_date <= date_till]
        academic_titles = [academic_title
                            for academic_title in educational_profile.academic_title
                            if academic_title.assignment_date <= date_till]
        educations = [education
                      for education in educational_profile.education
                      if education.start_date <= date_till
                      and education.end_date is not None
                      and education.end_date <= date_till]
        courses = [course
                   for course in educational_profile.course
                   if course.start_date <= date_till
                   and course.end_date is not None
                   and course.end_date <= date_till]

        service_id_info = self.get_service_id_by_user_id_and_date(db, user_id, date_till)

        timeline_read = HistoryTimeLineRead(
            holidays=holidays,
            badges=badges,
            rank = user.rank,
            ranks=ranks,
            penalties=penalties,
            contracts=contracts,
            attestations=attestations,
            characteristics=characteristics,
            emergency_contracts=emergency_contracts,
            experience=experience,
            secondments=secondments,
            equipments=equipments,
            general_information=general_information,
            service_id_info=service_id_info,
            driving_license=driving_license,
            identification_card=identification_card,
            passport=passport,
            academic_degrees=academic_degrees,
            academic_titles=academic_titles,
            educations=educations,
            courses=courses
        )
        timeline_dict = HistoryTimeLineRead.from_orm(
            timeline_read).dict()
        return timeline_dict

    # TODO
    # def get_timeline(self, db: Session, user_id: str, filter_timedelta: int, date: datetime):
    #     user = user_service.get_by_id(db, user_id)
    #     events = []
    #     privelege_emergency = privelege_emergency_service.get_by_user_id(
    #         db, user_id)
    #     if privelege_emergency is not None:
    #         events.append(Event(
    #             date=privelege_emergency.date_from,
    #             value=privelege_emergency.form,
    #             type="from",
    #             name="privelege_emergency"
    #         ))
    #         events.append(Event(
    #             date=privelege_emergency.date_to,
    #             value=privelege_emergency.form,
    #             type="to",
    #             name="privelege_emergency"
    #         ))

    #     personal_reserve = personnal_reserve_service.get_by_user_id(
    #         db, user_id)
    #     if personal_reserve is not None:
    #         events.append(Event(
    #             date=personal_reserve.date_from,
    #             value=personal_reserve.reserve,
    #             type="from",
    #             name="personal_reserve",
    #         ))
    #         events.append(Event(
    #             date=personal_reserve.date_to,
    #             value=personal_reserve.reserve,
    #             name="personal_reserve"
    #         ))

    #     badges = db.query(BadgeHistory).filter(
    #         BadgeHistory.user_id == user_id).all()
    #     for badge in badges:
    #         events.append(Event(
    #             date=badge.date_from,
    #             value=BadgeServiceDetailRead(badge),
    #             type="from",
    #             name="badge"
    #         ))
    #         if badge.date_to is not None:
    #             events.append(Event(
    #                 date=badge.date_to,
    #                 value=BadgeServiceDetailRead(badge),
    #                 type="to",
    #                 name="badge"
    #             ))
    #     ranks = db.query(RankHistory).filter(
    #         RankHistory.user_id == user_id).all()
    #     penalties = db.query(PenaltyHistory).filter(
    #         PenaltyHistory.user_id == user_id).all()
    #     contracts = db.query(ContractHistory).filter(
    #         ContractHistory.user_id == user_id).all()
    #     attestations = db.query(AttestationHistory).filter(
    #         AttestationHistory.user_id == user_id).all()
    #     characteristics = db.query(ServiceCharacteristicHistory).filter(
    #         ServiceCharacteristicHistory.user_id == user_id).all()
    #     holidays = db.query(StatusHistory).filter(
    #         StatusHistory.user_id == user_id).all()
    #     emergency_contracts = db.query(EmergencyServiceHistory).filter(
    #         EmergencyServiceHistory.user_id == user_id).all()
    #     experience = db.query(WorkExperienceHistory).filter(
    #         WorkExperienceHistory.user_id == user_id).all()
    #     secondments = db.query(SecondmentHistory).filter(
    #         SecondmentHistory.user_id == user_id).all()
    #     equipments = user.equipments

    #     service_id_info = self.get_service_id_by_user_id(db, user_id)

    #     attendance = AttendanceRead(
    #         physical_training=100,
    #         tactical_training=100,
    #         shooting_training=100,
    #     )

    #     return TimeLineRead(events)

    def black_beret_remove(self, db: Session, id: str):
        obj = db.query(self.model).get(id)
        if obj:
            badge = db.query(Badge).filter(Badge.id == obj.badge_id).first()
            db.delete(obj)
            db.delete(badge)
            db.flush()
        return obj
    
    def rank_histories_remove(self, db: Session, id: str):
        obj = db.query(self.model).get(id)
        if obj:
            rank = db.query(Rank).filter(Rank.id == obj.rank_id).first()
            db.delete(obj)
            db.delete(rank)
            db.flush()
        return obj
    
    def get_expiring_contracts(self, db: Session):
        today = datetime.now()
        day_30 = today + timedelta(days=30)

        latest_contract_subquery = db.query(
            ContractHistory.user_id.label("user_id"),
            func.max(ContractHistory.date_to).label("last_date_to")
        ).filter(
            ContractHistory.date_to >= today + timedelta(days=1),
            ContractHistory.date_to <= day_30
        ).group_by(ContractHistory.user_id).subquery()
        # print(latest_contract_subquery.c.user_id)
        # Main query to join the subquery and fetch the expiring contracts
        expiring_contracts = db.query(ContractHistory).join(
            latest_contract_subquery,
            and_(
                ContractHistory.user_id == latest_contract_subquery.c.user_id,
                ContractHistory.date_to == latest_contract_subquery.c.last_date_to
            )
        )

        return expiring_contracts.all()
    
    
    def get_expiring_ranks(self, db: Session):
        today = datetime.now()
        day_30 = today + timedelta(days=30)

        ranks = db.query(RankHistory).all()
        expiring_ranks = []
        for rank in ranks:
            rank_of_user = rank_service.get_by_id(db, rank.rank_id)
            duration_days = rank_of_user.duration * 365
            user = user_service.get_by_id(db, rank.user_id)
            user_max_rank = user.staff_unit.position.max_rank_id
            if rank.date_from + timedelta(days=duration_days) <= day_30 and rank_of_user.higher_rank_id is not None and rank_of_user.higher_rank_id != user_max_rank:
                expiring_ranks.append(rank)

        return expiring_ranks    


history_service = HistoryService(History)

