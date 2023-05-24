import enum

from sqlalchemy import Column, ForeignKey, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class PositionNameEnum(str, enum.Enum):
    CONSCRIPT_SOLDIER = 'Военно-служащий срочной службы'
    SECUTIRY_OFFICER = 'Офицер охраны'
    SECURITY_OFFICER_1_LEVEL = 'Сотрудник охраны 1-категории'
    SECURITY_OFFICER_2_LEVEL = 'Сотрудник охраны 2-категории'
    SECURITY_OFFICER_3_LEVEL = 'Сотрудник охраны 3-категории'
    PERSONNEL_HEAD = 'Начальник кадров'
    DEPUTY_PERSONNEL_HEAD = 'Заместители начальника кадров'
    CANDIDATE_MANAGEMENT_HEAD = 'Начальник управления кандидатами'
    POLITICS_GOVERNMENT_SERVANT = 'Политический гос. служащий'
    PSYCHOLOGIST = 'Психолог'
    REPRESENTATIVE_OF_SECURITY_DEPARTMENT = 'Представитель Управление собственной безопасности'
    POLYGRAPH_EXAMINER = 'Полиграфолог'
    INSTRUCTOR = 'Инструктор'
    DEAD = "Умер"
    RETIRED = "В отставке"
    IN_RESERVE = "В запасе"
    REMOVED_FROM_LIST = "Исключен из списков личного состава"
    SECONDMENT_OTHER = "Откомандирован в другой гос. орган"
    PERISHED = "Погиб"
    HR = "HR-менеджер"


class Position(NamedModel):

    __tablename__ = "positions"

    max_rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"),
                         nullable=True)
    
    rank = relationship("Rank", cascade="all,delete")
