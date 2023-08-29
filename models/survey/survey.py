import enum

from sqlalchemy import (Column, ForeignKey, CLOB,
                        TIMESTAMP, Boolean, Enum,
                        String)
from sqlalchemy.orm import relationship

from models import NamedModel


class SurveyStatusEnum(str, enum.Enum):
    ACTIVE = "Активный"
    ARCHIVE = "Архивный"
    DRAFT = "Черновик"


class SurveyTypeEnum(str, enum.Enum):
    SURVEY = "Опрос"
    QUIZ = "Тест"
    

class SurveyRepeatTypeEnum(str, enum.Enum):
    NEVER = "Никогда"
    EVERY_WEEK = "Каждую неделю"
    EVERY_MONTH = "Каждый месяц"
    EVERY_YEAR = "Каждый год"


class Survey(NamedModel):

    __tablename__ = "hr_erp_surveys"
    
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.nameKZ = kwargs.get("nameKZ")
        self.description = kwargs.get("description")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.is_anonymous = kwargs.get("is_anonymous")
        self.is_kz_translate_required = kwargs.get("is_kz_translate_required")
        self.status = SurveyStatusEnum.ACTIVE.value
        self.owner_id = kwargs.get("owner_id")
        self.type = kwargs.get("type")
        self.repeat_type = kwargs.get("repeat_type")
    
    description = Column(CLOB, nullable=True)
    start_date = Column(TIMESTAMP(timezone=True), nullable=True)
    end_date = Column(TIMESTAMP(timezone=True), nullable=True)
    is_anonymous = Column(Boolean(), default=False, nullable=True)
    is_kz_translate_required = Column(Boolean(), default=False, nullable=True)
    status = Column(
        Enum(SurveyStatusEnum),
        server_default=SurveyStatusEnum.ACTIVE.value,
        nullable=False
    )
    owner_id = Column(String(), ForeignKey("hr_erp_users.id"))
    type = Column(Enum(SurveyTypeEnum), nullable=False)
    repeat_type = Column(Enum(SurveyRepeatTypeEnum), nullable=False,
                         server_default=SurveyRepeatTypeEnum.NEVER.value)
        
    questions = relationship(
        "Question", cascade="all, delete", back_populates="survey")
    jurisdictions = relationship(
        "SurveyJurisdiction", cascade="all, delete", back_populates="survey")
