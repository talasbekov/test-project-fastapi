import enum

from sqlalchemy import Column, ForeignKey, Enum, String
from sqlalchemy.orm import relationship

from models import Model


class SurveyJurisdictionTypeEnum(str, enum.Enum):
    STAFF_DIVISION = "Штатное подразделение"
    CERTAIN_MEMBER = "Определенный участник"


class SurveyStaffPositionEnum(str, enum.Enum):
    EVERYONE = "Все"
    ONLY_PERSONNAL_STURCTURE = "Только личный состав"
    ONLY_MANAGING_STRUCTURE = "Только руководящий состав"


class SurveyJurisdiction(Model):
    
    __tablename__ = "hr_erp_surveys_jurisdictions"
    
    jurisdiction_type = Column(Enum(SurveyJurisdictionTypeEnum), nullable=False)
    staff_position = Column(Enum(SurveyStaffPositionEnum),
                            nullable=True,
                            server_default=SurveyStaffPositionEnum.EVERYONE.value)
    survey_id = Column(String(), ForeignKey("hr_erp_surveys.id"))
    staff_division_id = Column(String(), ForeignKey("hr_erp_staff_divisions.id"))
    certain_member_id = Column(String(), ForeignKey("hr_erp_users.id"))

    survey = relationship("Survey",
                          back_populates="jurisdictions",
                          foreign_keys=[survey_id])
