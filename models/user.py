from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship, Mapped

from models import isActiveModel, History
from .association import hr_documents_users


class User(isActiveModel):
    __tablename__ = "hr_erp_users"

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
    rank_id = Column(String(), ForeignKey("hr_erp_ranks.id"), nullable=True)
    last_signed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    staff_unit_id = Column(
        String(),
        ForeignKey("hr_erp_staff_units.id"),
        nullable=False,)
    actual_staff_unit_id = Column(
        String(),
        ForeignKey("hr_erp_staff_units.id"),
        nullable=False)
    supervised_by = Column(
        String(),
        ForeignKey("hr_erp_users.id"),
        nullable=True)

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

    staff_unit = relationship(
        "StaffUnit",
        back_populates="users",
        foreign_keys=staff_unit_id,
        lazy="select")
    staff_unit_replacing = relationship(
        "StaffUnit",
        back_populates="user_replacing",
        foreign_keys="StaffUnit.user_replacing_id",
        lazy="select"
    )
    archive_staff_unit_replacing = relationship(
        "ArchiveStaffUnit",
        back_populates="user_replacing",
        foreign_keys="ArchiveStaffUnit.user_replacing_id",
        lazy="select"
    )
    actual_staff_unit = relationship(
        "StaffUnit",
        back_populates="actual_users",
        foreign_keys=actual_staff_unit_id,
        lazy="select")

    hr_documents = relationship(
        "HrDocument",
        secondary=hr_documents_users,
        back_populates="users",
        cascade="all,delete",
        lazy="select"
    )
    hr_vacancies = relationship(
        "HrVacancyCandidate",
        back_populates="user",
        lazy="select"
    )

    staff_list = relationship(
        "StaffList",
        back_populates="user",
        cascade="all,delete",
        lazy="select")

    profile = relationship("Profile", back_populates="user", uselist=False)
    histories = relationship(
        "History",
        back_populates="user",
        foreign_keys=[
            History.user_id],
        lazy="select")

    statuses = relationship(
        "Status",
        back_populates="user",
        cascade="all,delete",
        lazy="select")
    secondments = relationship(
        "Secondment",
        back_populates="user",
        cascade="all,delete",
        lazy="select")
    attestations = relationship(
        "Attestation",
        back_populates="user",
        cascade="all,delete",
        lazy="select")
    coolnesses = relationship(
        "Coolness",
        back_populates="user",
        cascade="all,delete",
        lazy="select")
    penalties = relationship(
        "Penalty",
        back_populates="user",
        cascade="all,delete",
        lazy="select")
    privelege_emergencies = relationship(
        "PrivilegeEmergency",
        back_populates="user",
        cascade="all,delete",
        lazy="select")
    contracts = relationship(
        "Contract",
        back_populates="user",
        cascade="all,delete",
        lazy="select")
    equipments = relationship(
        "Equipment",
        back_populates="user",
        cascade="all,delete",
        lazy="select")
    answers = relationship(
        "Answer",
        cascade="all,delete",
        back_populates="user",
        lazy="select")
    exam_results = relationship("ExamResult",
                                back_populates="user",
                                lazy="select")
    activities = relationship("UserLoggingActivity",
                              back_populates="user",
                              cascade="all,delete",
                              lazy="select")
