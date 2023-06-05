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
    SUPERVISOR = "Начальник"


class CategoryCodeEnum(str, enum.Enum):
    C_S_1 = "C-S-1"
    C_S_2 = "C-S-2"
    C_S_3 = "C-S-3"
    C_S_4 = "C-S-4"
    C_S_5 = "C-S-5"
    C_S_6 = "C-S-6"
    C_S_7 = "C-S-7"
    C_S_8 = "C-S-8"
    C_S_9 = "C-S-9"
    C_S_10 = "C-S-10"
    C_S_11 = "C-S-11"
    C_S_12 = "C-S-12"

    C_RG_1 = "C-RG-1"
    C_RG_2 = "C-RG-2"
    C_RG_3 = "C-RG-3"
    C_RG_4 = "C-RG-4"
    C_RG_5 = "C-RG-5"
    C_RG_6 = "C-RG-6"
    C_RG_7 = "C-RG-7"
    C_RG_8 = "C-RG-8"
    C_RG_9 = "C-RG-9"
    C_RG_10 = "C-RG-10"
    C_RG_11 = "C-RG-11"
    C_RG_12 = "C-RG-12"
    C_RG_13 = "C-RG-13"


class Position(NamedModel):

    __tablename__ = "positions"

    max_rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"),
                         nullable=True)
    max_rank = relationship("Rank", cascade="all,delete")
    category_code = Column(String()) # TODO: enum was deleted because of LookupError: "C-S-1" is not among the defined enum values pls fix it
