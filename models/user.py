from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship

from models import isActiveModel, History
from .association import hr_documents_users


class User(isActiveModel):
    __tablename__ = "users"

    # Properties
    email = Column(String(150), nullable=True, unique=True)
    password = Column(String(255), nullable=True)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    father_name = Column(String(150), nullable=True)
    icon = Column(TEXT(), nullable=True)
    call_sign = Column(String(255), unique=True)
    id_number = Column(String(255), unique=True)
    phone_number = Column(String(32))
    address = Column(String(255))
    rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"), nullable=True)
    last_signed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    staff_unit_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=False)
    actual_staff_unit_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=False)
    supervised_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    description = Column(TEXT, nullable=True)
    cabinet = Column(String(255), nullable=True)
    service_phone_number = Column(String(32), nullable=True)
    is_military = Column(Boolean, nullable=True)
    personal_id = Column(String(255), nullable=True)
    iin = Column(String(255), nullable=True)
    date_birth = Column(TIMESTAMP(timezone=True))

    # Relationships
    rank = relationship("Rank")
    badges = relationship("Badge", back_populates="user", cascade="all,delete")

    staff_unit = relationship("StaffUnit", back_populates="users", foreign_keys=staff_unit_id)
    staff_unit_replacing = relationship(
        "StaffUnit", back_populates="user_replacing", foreign_keys="StaffUnit.user_replacing_id"
    )
    archive_staff_unit_replacing = relationship(
        "ArchiveStaffUnit", back_populates="user_replacing", foreign_keys="ArchiveStaffUnit.user_replacing_id"
    )
    actual_staff_unit = relationship("StaffUnit", back_populates="actual_users", foreign_keys=actual_staff_unit_id)

    hr_documents = relationship(
        "HrDocument", secondary=hr_documents_users, back_populates="users", cascade="all,delete"
    )
    hr_vacancies = relationship(
        "HrVacancyCandidate",
        back_populates="user"
    )

    staff_list = relationship("StaffList", back_populates="user", cascade="all,delete")

    profile = relationship("Profile", back_populates="user", uselist=False)
    histories = relationship("History", back_populates="user", foreign_keys=[History.user_id])

    statuses = relationship("Status", back_populates="user", cascade="all,delete")
    secondments = relationship("Secondment", back_populates="user", cascade="all,delete")
    attestations = relationship("Attestation", back_populates="user", cascade="all,delete")
    coolnesses = relationship("Coolness", back_populates="user", cascade="all,delete")
    penalties = relationship("Penalty", back_populates="user", cascade="all,delete")
    privelege_emergencies = relationship("PrivilegeEmergency", back_populates="user", cascade="all,delete")
    contracts = relationship("Contract", back_populates="user", cascade="all,delete")
    equipments = relationship("Equipment", back_populates="user", cascade="all,delete")
    
    answers = relationship("Answer", cascade="all,delete", back_populates="user")
