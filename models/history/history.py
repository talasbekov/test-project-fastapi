from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Double, Integer
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship
from models import NamedModel
from enum import Enum as BaseEnum

class HistoryEnum(BaseEnum):
    staff_unit_history = "staff_unit_history"
    rank_history = "rank_history"
    position_history = "position_history"
    penalty_history = "penalty_history"
    contact_history = "contact_history"
    emergency_service_history = "emergency_service_history"
    work_experience_history = "work_experience_history"
    secondment_history = "secondment_history"
    name_change_history = "name_change_history"
    attestation = "attestation"
    service_characteristic_history = "service_characteristic_history"
    holiday_review_history = "holiday_review_history"
     

class History(NamedModel):

    __tablename__ = "histories"

    date_from = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    document_link = Column(TEXT, nullable=True)
    document_number = Column(String, nullable=True)
    type = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "history",
        "polymorphic_on": type,
    }


class StaffUnitHistory(History):

    staff_unit_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "staff_unit_history",
    }


class RankHistory(History):

    rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "rank_history",
    }


class PositionHistory(History):

    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "position_history",
    }


class PenaltyHistory(History):

    __mapper_args__ = {
        "polymorphic_identity": "penalty_history",
    }


class ContactHistory(History):

    experience_years = Column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "contact_history",
    }


class EmergencyServiceHistory(History):

    coefficient = Column(Double, nullable=True)
    percentage = Column(Integer, nullable=True)

    staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'emergency_service_history'
    }


class WorkExperienceHistory(History):
    name_of_organization = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "work_experience_history",
    }


class SecondmentHistory(History):

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
    
    attestation_status = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "attestation",
    }


class ServiceCharacteristicHistory(History):
    characteristic_initiator = Column(String, nullable=True)


    __mapper_args__ = {
        "polymorphic_identity": "service_characteristic_history",
    }


class HolidayReviewHistory(History):

    __mapper_args__ = {
        "polymorphic_identity": "holiday_review_history",
    }
 
