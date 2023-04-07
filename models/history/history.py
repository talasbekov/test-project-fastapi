import datetime
import uuid
from enum import Enum as BaseEnum

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Double, Integer
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship, Session

from exceptions import NotSupportedException, NotFoundException
from models import (
    NamedModel,
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
    StaffDivision
)
from utils import is_valid_uuid

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


"""
    History

    Class is representation of user history. It is used to store information about
    user's history in different fields. For example, it is used to store information
    about user's rank changes, staff unit changes, etc.

    Must have implemented method:
        - **create_history** - method for creating history object from contstructor
"""
class History(NamedModel):

    __tablename__ = "histories"

    date_from = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    document_link = Column(TEXT, nullable=True)
    document_number = Column(String, nullable=True)
    type = Column(String, nullable=True)

    def create_history(self, **kwargs):
        raise NotSupportedException(detail="Method create_history must be implemented in child class")

    __mapper_args__ = {
        "polymorphic_identity": "history",
        "polymorphic_on": type,
    }


class StaffUnitHistory(History):

    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=True)
    position = relationship("Position")

    def create_history(self, db: Session, user_id: uuid.UUID, staff_unit_id: uuid.UUID, finish_last):
        staff_unit = db.query(StaffUnit).filter(StaffUnit.id == staff_unit_id).first()
        if staff_unit is None:
            raise NotFoundException(detail="Staff unit not found")
        finish_last(db, user_id, self.__mapper_args__["polymorphic_identity"])
        db.add(StaffUnitHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                position_id=staff_unit.position_id,
                name='',
            )
        )

    __mapper_args__ = {
        "polymorphic_identity": "staff_unit_history",
    }


class RankHistory(History):

    rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"), nullable=True)
    rank = relationship("Rank")

    def create_history(self, db: Session, user_id: uuid.UUID, rank_id: uuid.UUID, finish_last):
        rank = db.query(Rank).filter(Rank.id == rank_id).first()
        if rank is None:
            raise NotFoundException(detail="Rank not found")
        finish_last(db, user_id, self.__mapper_args__["polymorphic_identity"])
        db.add(RankHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                rank_id=rank_id,
                name=rank.name,
            )
            )

    __mapper_args__ = {
        "polymorphic_identity": "rank_history",
    }


class PenaltyHistory(History):

    penalty_id = Column(UUID(as_uuid=True), ForeignKey("penalties.id"), nullable=True)
    penalty = relationship("Penalty")

    def create_history(self, db: Session, user_id: uuid.UUID, penalty_id: uuid.UUID, finish_last):
        penalty = db.query(Penalty).filter(Penalty.id == penalty_id).first()
        if penalty is None:
            raise NotFoundException(detail="Penalty not found")
        finish_last(db, user_id, self.__mapper_args__["polymorphic_identity"])
        db.add(PenaltyHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                penalty_id=penalty_id,
                name=penalty.name,
            )
        )

    __mapper_args__ = {
        "polymorphic_identity": "penalty_history",
    }


class EmergencyServiceHistory(History):

    coefficient = Column(Double, nullable=True)
    percentage = Column(Integer, nullable=True)

    staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'emergency_service_history'
    }


class ContractHistory(History):

    experience_years = Column(Integer, nullable=True)

    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=True)
    contract = relationship("Contract")

    def create_history(self, db: Session, user_id: uuid.UUID, contract_id: uuid.UUID, finish_last):
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if contract is None:
            raise NotFoundException(detail="Contract not found")
        finish_last(db, user_id, self.__mapper_args__["polymorphic_identity"])
        db.add(ContractHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                contract_id=contract_id,
                name=contract.name,
                experience_years=contract.experience_years,
            )
        )

    __mapper_args__ = {
        "polymorphic_identity": "contract_history",
    }

class CoolnessHistory(History):

    coolness_id = Column(UUID(as_uuid=True), ForeignKey("coolnesses.id"), nullable=True)
    coolness = relationship("Coolness")

    def create_history(self, db: Session, user_id: uuid.UUID, coolness_id: uuid.UUID, finish_last):
        if db.query(Coolness).filter(Coolness.id == coolness_id).first() is None:
            raise NotFoundException(detail="Coolness not found")
        finish_last(db, user_id, self.__mapper_args__["polymorphic_identity"])
        db.add(CoolnessHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                coolness_id=coolness_id,
                name='',
            )
        )               

    # coefficient = Column(Double, nullable=True)
    # percentage = Column(Integer, nullable=True)

    # staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'coolness_history'
    }


class WorkExperienceHistory(History):

    name_of_organization = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "work_experience_history",
    }


class SecondmentHistory(History):

    secondment_id = Column(UUID(as_uuid=True), ForeignKey("secondments.id"), nullable=True)
    secondment = relationship("Secondment")

    def create_history(self, db: Session, user_id: uuid.UUID, value: uuid.UUID, finish_last):
        secondment = db.query(Secondment).filter(Secondment.id == value).first()
        if secondment is None:
            raise NotFoundException(detail="Secondment not found")
        db.add(SecondmentHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                secondment_id=value,
                name="",
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

    def create_history(self, db: Session, user_id: uuid.UUID, value: uuid.UUID, finish_last):
        attestation = db.query(Attestation).filter(Attestation.id == value).first()
        if attestation is None:
            raise NotFoundException(detail="Attestation not found")
        db.add(AttestationHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                attestation_id=value,
                name="",
            )
        )
        db.flush()

    __mapper_args__ = {
        "polymorphic_identity": "attestation",
    }


class ServiceCharacteristicHistory(History):

    characteristic_initiator = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "service_characteristic_history",
    }


class StatusHistory(History):

    status_id = Column(UUID(as_uuid=True), ForeignKey("statuses.id"), nullable=True)
    status = relationship("Status")

    def create_history(self, db: Session, user_id: uuid.UUID, value: uuid.UUID, finish_last):
        status = db.query(Status).filter(Status.id == value).first()
        if status is None:
            raise NotFoundException(detail="Status not found")
        db.add(StatusHistory(
                date_from=datetime.datetime.now(),
                date_to=None,
                user_id=user_id,
                status_id=value,
                name="",
            )
        )
        db.flush()

    __mapper_args__ = {
        "polymorphic_identity": "status_history",
    }
