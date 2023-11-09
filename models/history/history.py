import datetime
import uuid
from enum import Enum as BaseEnum

from typing import Union

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Double, Integer, Boolean
from sqlalchemy.dialects.oracle import NCLOB, CLOB
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import text

from exceptions import NotSupportedException, NotFoundException
from models import (
    Model,
    Rank,
    Penalty,
    Coolness,
    Contract,
    Secondment,
    Attestation,
    Status,
    Badge
)


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

    __tablename__ = "hr_erp_histories"

    date_from = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)
    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    document_link = Column(CLOB, nullable=True)
    cancel_document_link = Column(CLOB, nullable=True)
    confirm_document_link = Column(CLOB, nullable=True)
    document_number = Column(String, nullable=True)
    type = Column(String, nullable=True)
    document_style = Column(String, nullable=True)
    date_credited = Column(TIMESTAMP, nullable=True)
    staff_division_name = Column(String, nullable=True)
    staff_division_nameKZ = Column(
        'staff_division_namekz', String, nullable=True)
    reason = Column(String, nullable=True, )
    reasonKZ = Column("reasonkz", String, nullable=True)

    user = relationship(
        "User",
        back_populates="histories",
        foreign_keys=[user_id])

    @classmethod
    def create_history(self, **kwargs):
        raise NotSupportedException(
            detail="Method create_history must be implemented in child class")

    __mapper_args__ = {
        "polymorphic_identity": "history",
        "polymorphic_on": type,
    }


class RankHistory(History):

    rank_id = Column(String(), ForeignKey("hr_erp_ranks.id"), nullable=True)
    rank = relationship("Rank", foreign_keys=[rank_id])

    rank_assigned_by = Column(String, nullable=True)
    rank_name = Column(String, nullable=True)
    rank_nameKZ = Column('rank_namekz', String, nullable=True)\
        
    early_promotion = Column(Boolean, nullable=True, default=False)

    @classmethod
    def create_history(cls, db: Session, user_id: str,
                       id: str, finish_last):
        rank = db.query(Rank).filter(Rank.id == id).first()
        if rank is None:
            raise NotFoundException(detail="Rank not found")
        finish_last(db, user_id, cls.__mapper_args__["polymorphic_identity"])
        obj = RankHistory(
            date_from=datetime.datetime.now(),
            date_to=None,
            user_id=user_id,
            rank_id=id
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    __mapper_args__ = {
        "polymorphic_identity": "rank_history",
    }


class BadgeHistory(History):

    badge_id = Column(
        String(),
        ForeignKey("hr_erp_badges.id"),
        nullable=True)
    badge = relationship("Badge", back_populates="history")

    @classmethod
    def create_history(cls, db: Session, user_id: str,
                       id: str, finish_last):
        badge = db.query(Badge).filter(Badge.id == id).first()
        if badge is None:
            raise NotFoundException(detail="Badge not found")
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

    penalty_id = Column(
        String(),
        ForeignKey("hr_erp_penalties.id"),
        nullable=True)
    penalty = relationship("Penalty")

    @classmethod
    def create_history(cls, db: Session, user_id: str,
                       id: str, finish_last):
        penalty = db.query(Penalty).filter(Penalty.id == id).first()
        if penalty is None:
            raise NotFoundException(detail="Penalty not found")
        finish_last(db,
                    user_id,
                    cls.__mapper_args__["polymorphic_identity"])
        obj = PenaltyHistory(
            date_from=datetime.datetime.now(),
            date_to=datetime.datetime.now() + datetime.timedelta(days=180),
            user_id=user_id,
            penalty_id=id,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    @classmethod
    def create_timeline_history(
        cls,
        db: Session,
        user_id: str,
        id: str,
        finish_last,
        date_from,
        date_to
    ):
        penalty = db.query(Penalty).filter(Penalty.id == id).first()
        if penalty is None:
            raise NotFoundException(detail="Penalty not found")
        history = PenaltyHistory(
            date_from=date_from,
            date_to=date_to,
            user_id=user_id,
            penalty_id=id,
        )
        db.add(history)
        db.flush()
        return history

    __mapper_args__ = {
        "polymorphic_identity": "penalty_history",
    }


class EmergencyServiceHistory(History):

    coefficient = Column(Double, nullable=True)
    percentage = Column(Integer, nullable=True)

    position_id = Column(
        String(),
        ForeignKey("hr_erp_positions.id"),
        nullable=True)
    position = relationship("Position", foreign_keys=[position_id])

    staff_division_id = Column(
        String(),
        ForeignKey("hr_erp_staff_divisions.id"),
        nullable=True)
    staff_division = relationship(
        "StaffDivision",
        foreign_keys=[staff_division_id])

    position_name = Column(String, nullable=True)
    position_nameKZ = Column('position_namekz', String, nullable=True)

    position_name = Column(String, nullable=True)
    position_nameKZ = Column('position_namekz', String, nullable=True)

    contractor_signer_name = Column(String, nullable=True)
    contractor_signer_nameKZ = Column(
        'contractor_signer_namekz', String, nullable=True)

    @classmethod
    def create_history(self, db: Session, user_id: str,
                       id: str, finish_last):
        query = db.execute(text(
            f"SELECT HR_ERP_STAFF_UNITS.id, HR_ERP_STAFF_UNITS.position_id, HR_ERP_STAFF_UNITS.staff_division_id FROM HR_ERP_STAFF_UNITS JOIN HR_ERP_USERS ON HR_ERP_STAFF_UNITS.id=HR_ERP_USERS.staff_unit_id WHERE HR_ERP_STAFF_UNITS.id = '{id}' AND HR_ERP_USERS.id = '{user_id}'"))
        staff_unit = query.fetchone()
        if staff_unit is None:
            raise NotFoundException(detail="Staff unit not found")
        last_history: EmergencyServiceHistory = finish_last(
            db, user_id, self.__mapper_args__["polymorphic_identity"])
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
        'polymorphic_identity': 'emergency_history'
    }


class ContractHistory(History):

    experience_years = Column(Integer, nullable=True)

    contract_id = Column(
        String(),
        ForeignKey("hr_erp_contracts.id"),
        nullable=True)
    contract = relationship("Contract")

    @classmethod
    def create_history(cls, db: Session, user_id: str,
                       id: str, finish_last):
        contract = db.query(Contract).filter(Contract.id == id).first()
        if contract is None:
            raise NotFoundException(detail="Contract not found")
        finish_last(db, user_id, cls.__mapper_args__["polymorphic_identity"])
        obj = ContractHistory(
            date_from=datetime.datetime.now(),
            date_to=None,
            user_id=user_id,
            contract_id=id,
            experience_years=contract.type.years,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    @classmethod
    def create_timeline_history(
        cls,
        db: Session,
        user_id: str,
        id: str,
        finish_last,
        date_from, date_to
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
            experience_years=contract.type.years,
        )
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    __mapper_args__ = {
        "polymorphic_identity": "contract_history",
    }


class CoolnessHistory(History):

    coolness_id = Column(
        String(),
        ForeignKey("hr_erp_coolnesses.id"),
        nullable=True)
    coolness = relationship(
        "Coolness",
        back_populates="history",
        uselist=False)

    @classmethod
    def create_history(cls, db: Session, user_id: str,
                       id: str, finish_last):
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

    # staff_division_id = Column(String(),
    # ForeignKey("hr_erp_staff_divisions.id"), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'coolness_history'
    }


class WorkExperienceHistory(History):

    name_of_organization = Column(String, nullable=True)
    name_of_organizationKZ = Column(
        "name_of_organizationkz", String, nullable=True)

    is_credited = Column(Boolean, nullable=True)

    position_work_experience = Column(String, nullable=True)
    position_work_experienceKZ = Column(
        "position_work_experiencekz", String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "work_experience_history",
    }


class SecondmentHistory(History):

    secondment_id = Column(
        String(),
        ForeignKey("hr_erp_secondments.id"),
        nullable=True)
    secondment = relationship("Secondment")

    @classmethod
    def create_history(cls, db: Session, user_id: str,
                       id: str, finish_last):
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
        cls,
        db: Session,
        user_id: str,
        id: str,
        finish_last,
        date_from,
        date_to
    ):
        secondment = db.query(Secondment).filter(Secondment.id == id).first()
        if secondment is None:
            raise NotFoundException(detail="Secondment not found")
        history = SecondmentHistory(
            date_from=date_from,
            date_to=date_to,
            user_id=user_id,
            secondment_id=id,
        )
        db.add(history)
        db.flush()
        return history

    __mapper_args__ = {
        "polymorphic_identity": "secondment_history",
    }


class NameChangeHistory(History):

    name_change_id = Column(
        String(),
        ForeignKey("hr_erp_name_changes.id"),
        nullable=True)
    name_change = relationship("NameChange",
                               back_populates="name_change_histories")

    __mapper_args__ = {
        "polymorphic_identity": "name_change_history",
    }


class AttestationHistory(History):

    attestation_id = Column(
        String(),
        ForeignKey("hr_erp_attestations.id"),
        nullable=True)
    attestation = relationship("Attestation")

    attestation_status = Column(String, nullable=True)
    attestation_statusKZ = Column(
        "attestation_statuskz", String, nullable=True)

    @classmethod
    def create_history(cls, db: Session, user_id: str,
                       id: str, finish_last):
        attestation = db.query(Attestation).filter(
            Attestation.id == id).first()
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

    characteristic_initiator_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"),
        nullable=True)
    characteristic_initiator = relationship(
        "User", foreign_keys=[characteristic_initiator_id])

    __mapper_args__ = {
        "polymorphic_identity": "service_characteristic_history",
    }


class StatusHistory(History):

    status_id = Column(
        String(),
        ForeignKey("hr_erp_statuses.id"),
        nullable=True)
    status = relationship("Status", back_populates="history")
    status_name = Column(NCLOB, nullable=True)
    status_nameKZ = Column('status_namekz', String, nullable=True)

    @classmethod
    def create_history(cls, db: Session, user_id: str,
                       id: Union[str, str], finish_last):
        if isinstance(id, str):
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
        user_id: str,
        id: str,
        finish_last,
        date_from,
        date_to,
    ):
        status = db.query(Status).filter(Status.id == id).first()
        if status is None:
            raise NotFoundException(detail="Status not found")
        history = StatusHistory(
            date_from=date_from,
            date_to=date_to,
            user_id=user_id,
            status_id=id,
        )
        db.add(history)
        db.flush()
        return history

    __mapper_args__ = {
        "polymorphic_identity": "status_history",
    }
