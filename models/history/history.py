import datetime
import uuid
from enum import Enum as BaseEnum

from typing import Union

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Double, Integer, Boolean
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship, Session

from exceptions import NotSupportedException, NotFoundException
from models import (
    NamedModel,
    Model,
    StaffUnit,
    Rank, 
    Penalty,
    Coolness,
    Contract,
    ContractType,
    Secondment,
    # NameChange,
    Attestation,
    Status,
    Coolness,
    CoolnessType,
    Contract,
    StaffDivision,
    Badge
)
from utils import is_valid_uuid
from docx import Document

class HistoryEnum(BaseEnum):

    staff_unit_history = "staff_unit_history"
    rank_history = "rank_history"
    penalty_history = "penalty_history"
    emergency_service_history = "emergency_service_history"
    work_experience_history = "work_experience_history"
    secondment_history = "secondment_history"
    name_change_history = "name_change_history"
    attestation = "attestation"
    service_characteristic_history = "service_characteristic_history"
    status_history = "status_history"
    coolness_history = "coolness_history"
    contract_history = "contract_history"
    badge_history = "badge_history"


"""
    History

    Class is representation of user history. It is used to store information about
    user's history in different fields. For example, it is used to store information
    about user's rank changes, staff unit changes, etc.

    Must have implemented method:
        - **create_history** - method for creating history object from constructor
"""
class History(Model):

    __tablename__ = "histories"

    date_from = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    document_link = Column(TEXT, nullable=True)
    cancel_document_link = Column(TEXT, nullable=True)
    confirm_document_link = Column(TEXT, nullable=True)
    document_number = Column(String, nullable=True)
    type = Column(String, nullable=True)
    document_style = Column(String, nullable=True)
    date_credited = Column(TIMESTAMP, nullable=True)
    
    user = relationship("User", back_populates="history", foreign_keys=[user_id])

    @classmethod
    def create_history(self, **kwargs):
        raise NotSupportedException(detail="Method create_history must be implemented in child class")

    __mapper_args__ = {
        "polymorphic_identity": "history",
        "polymorphic_on": type,
    }


class RankHistory(History):

    rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"), nullable=True)
    rank = relationship("Rank", foreign_keys=[rank_id])
    
    rank_assigned_by = Column(String, nullable=True)

    @classmethod
    def create_history(cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last):
        rank = db.query(Rank).filter(Rank.id == id).first()
        if rank is None:
            raise NotFoundException(detail="Rank not found")
        finish_last(db, user_id, cls.__mapper_args__["polymorphic_identity"])
        obj = RankHistory(
            date_from=datetime.datetime.now(),
            date_to=None,
            user_id=user_id,
            rank_id=id,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    __mapper_args__ = {
        "polymorphic_identity": "rank_history",
    }

class BadgeHistory(History):

    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=True)
    badge = relationship("Badge")

    @classmethod
    def create_history(cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last):
        badge = db.query(Badge).filter(Badge.id == id).first()
        if badge is None:
            raise NotFoundException(detail="Badge not found")
        finish_last(db, user_id, cls.__mapper_args__["polymorphic_identity"])
        obj = BadgeHistory(
            date_from=datetime.datetime.now(),
            date_to=None,
            user_id=user_id,
            badge_id=id,
        )

        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    __mapper_args__ = {
        "polymorphic_identity": "badge_history",
    }


class PenaltyHistory(History):

    penalty_id = Column(UUID(as_uuid=True), ForeignKey("penalties.id"), nullable=True)
    penalty = relationship("Penalty")

    @classmethod
    def create_history(cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last):
        penalty = db.query(Penalty).filter(Penalty.id == id).first()
        if penalty is None:
            raise NotFoundException(detail="Penalty not found")
        finish_last(db, user_id, cls.__mapper_args__["polymorphic_identity"])
        obj = PenaltyHistory(
            date_from=datetime.datetime.now(),
            date_to=None,
            user_id=user_id,
            penalty_id=id,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    @classmethod
    def create_timeline_history(
        cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last, date_from, date_to
    ):
        penalty = db.query(Penalty).filter(Penalty.id == id).first()
        if penalty is None:
            raise NotFoundException(detail="Penalty not found")
        db.add(
            PenaltyHistory(
                date_from=date_from,
                date_to=date_to,
                user_id=user_id,
                penalty_id=id,
            )
        )
        db.flush()

    __mapper_args__ = {
        "polymorphic_identity": "penalty_history",
    }


class EmergencyServiceHistory(History):

    coefficient = Column(Double, nullable=True)
    percentage = Column(Integer, nullable=True)
    
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=True)
    position = relationship("Position", foreign_keys=[position_id])

    staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)
    staff_division = relationship("StaffDivision", foreign_keys=[staff_division_id])

    staff_division_name = Column(String, nullable=True)
    staff_division_nameKZ = Column(String, nullable=True)

    @classmethod
    def create_history(self, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last):
        staff_unit = db.query(StaffUnit).filter(StaffUnit.id == id).first()
        if staff_unit is None:
            raise NotFoundException(detail="Staff unit not found")
        last_history: EmergencyServiceHistory = finish_last(db, user_id, self.__mapper_args__["polymorphic_identity"])
        if last_history is not None:
            if last_history.staff_division is not None:
                last_history.staff_division_name = last_history.staff_division.name
                last_history.staff_division_nameKZ = last_history.staff_division.nameKZ

            db.add(last_history)

        obj = EmergencyServiceHistory(
                coefficient=1.5,
                percentage=0,
                position_id=staff_unit.position_id,
                staff_division_id=staff_unit.staff_division_id,
                user_id=user_id,
                date_from=datetime.datetime.now(),
            )
        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    
    __mapper_args__ = {
        'polymorphic_identity': 'emergency_service_history'
    }


class ContractHistory(History):

    experience_years = Column(Integer, nullable=True)

    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=True)
    contract = relationship("Contract")

    @classmethod
    def create_history(cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last):
        contract = db.query(Contract).filter(Contract.id == id).first()
        if contract is None:
            raise NotFoundException(detail="Contract not found")
        finish_last(db, user_id, cls.__mapper_args__["polymorphic_identity"])
        obj = ContractHistory(
            date_from=datetime.datetime.now(),
            date_to=None,
            user_id=user_id,
            contract_id=id,
            experience_years=contract.experience_years,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    @classmethod
    def create_timeline_history(
        cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last, date_from, date_to
    ):
        contract = db.query(Contract).filter(Contract.id == id).first()
        if contract is None:
            raise NotFoundException(detail="Contract not found")
        finish_last(db, user_id, cls.__mapper_args__["polymorphic_identity"])
        obj = ContractHistory(
            date_from=date_from,
            date_to=date_to,
            user_id=user_id,
            contract_id=id,
            experience_years=contract.experience_years,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    __mapper_args__ = {
        "polymorphic_identity": "contract_history",
    }

class CoolnessHistory(History):

    coolness_id = Column(UUID(as_uuid=True), ForeignKey("coolnesses.id"), nullable=True)
    coolness = relationship("Coolness", back_populates="history", uselist=False)


    @classmethod
    def create_history(cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last):
        if db.query(Coolness).filter(Coolness.id == id).first() is None:
            raise NotFoundException(detail="Coolness not found")
        finish_last(db, user_id, cls.__mapper_args__["polymorphic_identity"])
        obj = CoolnessHistory(
            date_from=datetime.datetime.now(),
            date_to=None,
            user_id=user_id,
            coolness_id=id,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    # coefficient = Column(Double, nullable=True)
    # percentage = Column(Integer, nullable=True)

    # staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'coolness_history'
    }


class WorkExperienceHistory(History):

    name_of_organization = Column(String, nullable=True)
    is_credited = Column(Boolean, nullable=True)
     
    position_work_experience = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "work_experience_history",
    }

class SecondmentHistory(History):

    secondment_id = Column(UUID(as_uuid=True), ForeignKey("secondments.id"), nullable=True)
    secondment = relationship("Secondment")

    @classmethod
    def create_history(cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last):
        secondment = db.query(Secondment).filter(Secondment.id == id).first()
        if secondment is None:
            raise NotFoundException(detail="Secondment not found")
        obj = SecondmentHistory(
            date_from=datetime.datetime.now(),
            date_to=None,
            user_id=user_id,
            secondment_id=id,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    @classmethod
    def create_timeline_history(
        cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last, date_from, date_to
    ):
        secondment = db.query(Secondment).filter(Secondment.id == id).first()
        if secondment is None:
            raise NotFoundException(detail="Secondment not found")
        db.add(
            SecondmentHistory(
                date_from=date_from,
                date_to=date_to,
                user_id=user_id,
                secondment_id=id,
            )
        )
        db.flush()

    __mapper_args__ = {
        "polymorphic_identity": "secondment_history",
    }


class NameChangeHistory(History):

    name_change_id = Column(UUID(as_uuid=True), ForeignKey("name_changes.id"), nullable=True)
    name_change = relationship("NameChange", back_populates="name_change_histories")
    
    __mapper_args__ = {
        "polymorphic_identity": "name_change_history",
    }

class AttestationHistory(History):

    attestation_id = Column(UUID(as_uuid=True), ForeignKey("attestations.id"), nullable=True)
    attestation = relationship("Attestation")

    attestation_status = Column(String, nullable=True)
    


    @classmethod
    def create_history(cls, db: Session, user_id: uuid.UUID, id: uuid.UUID, finish_last):
        attestation = db.query(Attestation).filter(Attestation.id == id).first()
        if attestation is None:
            raise NotFoundException(detail="Attestation not found")
        obj = AttestationHistory(
            date_from=datetime.datetime.now(),
            date_to=None,
            user_id=user_id,
            attestation_id=id,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    __mapper_args__ = {
        "polymorphic_identity": "attestation",
    } 
 


class ServiceCharacteristicHistory(History):

    characteristic_initiator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    characteristic_initiator = relationship("User", foreign_keys=[characteristic_initiator_id])
    
    __mapper_args__ = {
        "polymorphic_identity": "service_characteristic_history",
    }


class StatusHistory(History):

    status_id = Column(UUID(as_uuid=True), ForeignKey("statuses.id"), nullable=True)
    status = relationship("Status")
    status_name = Column(String, nullable=True)

    @classmethod
    def create_history(cls, db: Session, user_id: uuid.UUID, id: Union[uuid.UUID, str], finish_last):
        if isinstance(id, uuid.UUID):
            status = db.query(Status).filter(Status.id == id).first()
            if status is None:
                raise NotFoundException(detail="Status not found")
            obj = StatusHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                status_id=id,
            )
            db.add(obj)
        else:
            obj = StatusHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                status_id=None,
            )
            db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    @classmethod
    def create_timeline_history(
        cls,
        db: Session,
        user_id: uuid.UUID,
        id: uuid.UUID,
        finish_last,
        date_from,
        date_to,
    ):
        status = db.query(Status).filter(Status.id == id).first()
        if status is None:
            raise NotFoundException(detail="Status not found")
        db.add(
            StatusHistory(
                date_from=date_from,
                date_to=date_to,
                user_id=user_id,
                status_id=id,
            )
        )
        db.flush()

    __mapper_args__ = {
        "polymorphic_identity": "status_history",
    }
