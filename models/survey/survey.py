import enum

from sqlalchemy import (Column, ForeignKey, TEXT,
                        TIMESTAMP, Boolean, Enum)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class SurveyStatusEnum(str, enum.Enum):
    ACTIVE = "Активный"
    ARCHIVE = "Архивный"
    DRAFT = "Черновик"


class SurveyJurisdictionTypeEnum(str, enum.Enum):
    STAFF_DIVISION = "Штатное подразделение"
    CERTAIN_MEMBER = "Определенный участник"


class SurveyStaffPositionEnum(str, enum.Enum):
    EVERYONE = "Все"
    ONLY_PERSONNAL_STURCTURE = "Только личный состав"
    ONLY_MANAGING_STRUCTURE = "Только руководящий состав"


class SurveyTypeEnum(str, enum.Enum):
    SURVEY = "Опрос"
    QUIZ = "Тест"

class Survey(NamedModel):

    __tablename__ = "surveys"
    
    description = Column(TEXT, nullable=True)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(
        Enum(SurveyStatusEnum),
        default=SurveyStatusEnum.ACTIVE.value,
        nullable=False
    )
    jurisdiction_type = Column(Enum(SurveyJurisdictionTypeEnum), nullable=False)
    is_kz_translate_required = Column(Boolean(), default=False, nullable=True)
    is_anonymous = Column(Boolean(), default=False, nullable=True)
    certain_member_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"))
    staff_position = Column(Enum(SurveyStaffPositionEnum), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Enum(SurveyTypeEnum), nullable=False)
        
    questions = relationship(
        "Question", cascade="all, delete", back_populates="survey")
