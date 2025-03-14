from enum import Enum as EnumBase

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from models import NamedModel
import logging

logger = logging.getLogger(__name__)


class PositionNameEnum(str, EnumBase):
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
    REPRESENTATIVE_OF_SECURITY_DEPARTMENT = (
        'Представитель Управление собственной безопасности'
    )
    POLYGRAPH_EXAMINER = 'Полиграфолог'
    INSTRUCTOR = 'Инструктор'
    DEAD = "Исключен из списков в связи со смертью"
    RETIRED = "Уволенный сотрудник"
    IN_RESERVE = "В распоряжении"
    REMOVED_FROM_LIST = "Исключен из списков личного состава"
    SECONDMENT_OTHER = "Откомандирован в другой гос. орган"
    PERISHED = "Погиб"
    HR = "HR-менеджер"
    SUPERVISOR = "Начальник"
    HEAD_OF_SERVICE = "Начальник Службы"
    HEAD_OF_SERVICE_INSTEAD = "Заместитель начальника СГО"
    HEAD_OF_SERVICE_SHORT = "Зам Нач СГО"
    HEAD_OF_DEPARTMENT = 'Начальник департамента'
    MANAGEMENT_HEAD = 'Начальник управления'
    HEAD_OF_OTDEL = 'Начальник отдела'
    CANDIDATE = 'Кандидат'
    OUT_STAFF = 'Внештатный сотрудник'


class CategoryCodeEnum(str, EnumBase):
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


class FormEnum(EnumBase):
    form1 = "Форма 1"
    form2 = "Форма 2"
    form3 = "Форма 3"


class PositionType(NamedModel):

    __tablename__ = "hr_erp_position_types"

    positions = relationship("Position", back_populates="type")

class Position(NamedModel):

    __tablename__ = "hr_erp_positions"

    max_rank_id = Column(String(), ForeignKey("hr_erp_ranks.id"),
                         nullable=True)
    max_rank = relationship("Rank", cascade="all,delete")
    # TODO: enum was deleted because of LookupError: "C-S-1" is not among the
    # defined enum values pls fix it
    category_code = Column(String())
    form = Column(String(), nullable=True)
    position_order = Column(Integer)
    type_id = Column(String(), ForeignKey("hr_erp_position_types.id"))
    type = relationship("PositionType", back_populates="positions")

    @property
    def shortened_max_rank_name(self):
        if self.category_code is None:
            logger.warning("category_code is None for Position ID: %s", self.id)
            return "Unknown Rank"
        if self.category_code.startswith("C-RG"):
            return self.max_rank.name[:-6] if self.max_rank else "Unknown Rank"
        return self.max_rank.name if self.max_rank else "Unknown Rank"

    @property
    def shortened_nameKZ(self):
        if self.category_code is None:
            logger.warning("category_code is None for Position ID: %s", self.id)
            return "Unknown NameKZ"
        if self.category_code.startswith("C-RG"):
            return self.nameKZ[:-6] if self.nameKZ else "Unknown NameKZ"
        return self.nameKZ if self.nameKZ else "Unknown NameKZ"
