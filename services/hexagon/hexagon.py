import random

from sqlalchemy.orm import Session
from sqlalchemy import func
from enum import Enum

from datetime import datetime
from exceptions.client import NotFoundException
from models import Hexagon
# from schemas import HexagonRead, StatRead, HexagonAveragesRead
from services.base import ServiceBase
from typing import List


class StatsEnum(Enum):
    KP = {'name': 'Заполнение бланка компетенций руководителями',
          'nameKZ': 'Басшылардың құзыреттілік нысанын толтыруы',
          'abb': 'КП'}
    LS = {'name': 'Заполнение бланка компетенций коллегами (личным составом)',
          'nameKZ': 'Әріптестерінің (кадрлардың) құзыреттілік нысанын толтыруы',
          'abb': 'ЛС'}
    EC = {'name': 'Активность в ИС "Талдау"',
          'nameKZ': 'Талдау АЖ-дағы белсенділігі',
          'abb': 'ИС'}
    PZ = {'name': 'Посещаемость занятий по огневой и физической подготовке',
          'nameKZ': 'Өрт және дене шынықтыру даярлығы сабақтарына қатысу',
          'abb': 'ПЗ'}
    OP = {'name': 'Средний балл по огневой подготовке',
          'nameKZ': 'Средний балл по огневой подготовке',
          'abb': 'ОП'}
    FP = {'name': 'Средний балл по физической подготовке',
          'nameKZ': 'Дене дайындығы бойынша GP',
          'abb': 'ФП'}


class HexagonService(ServiceBase):

    # def get_by_user_id(self, db: Session, user_id: str) -> HexagonRead:
    #
    #     hexagon = (db.query(Hexagon)
    #                .filter(Hexagon.user_id == user_id)
    #                .order_by(Hexagon.created_at.desc())
    #                .first())
    #
    #     if not hexagon:
    #         raise NotFoundException(f"Hexagon for user not found")
    #
    #     stats_dict = self.__get_stats_dict(db, hexagon)
    #
    #     hexagon_read = HexagonRead(
    #         id=hexagon.id,
    #         created_at=hexagon.created_at,
    #         updated_at=hexagon.updated_at,
    #         KP=stats_dict['KP'],
    #         LS=stats_dict['LS'],
    #         EC=stats_dict['EC'],
    #         PZ=stats_dict['PZ'],
    #         OP=stats_dict['OP'],
    #         FP=stats_dict['FP']
    #     )
    #     return hexagon_read

    # def get_by_user_id_and_date(self,
    #                             db: Session,
    #                             user_id: str,
    #                             date_from: datetime) -> List[HexagonRead]:
    #     hexagons = (db.query(Hexagon)
    #                 .filter(Hexagon.user_id == user_id,
    #                         Hexagon.created_at >= date_from)
    #                 .order_by(Hexagon.created_at.desc())
    #                 .all())
    #
    #     if not hexagons:
    #         raise NotFoundException(f"Hexagons for user and date not found")
    #
    #     hexagons_read = []
    #
    #     for hexagon in hexagons:
    #         stats_dict = self.__get_stats_dict(db, hexagon)
    #
    #         hexagons_read.append(HexagonRead(
    #             id=hexagon.id,
    #             created_at=hexagon.created_at,
    #             updated_at=hexagon.updated_at,
    #             KP=stats_dict['KP'],
    #             LS=stats_dict['LS'],
    #             EC=stats_dict['EC'],
    #             PZ=stats_dict['PZ'],
    #             OP=stats_dict['OP'],
    #             FP=stats_dict['FP']
    #         ))
    #
    #     return hexagons_read

    def get_average(self, db: Session):
        # avg_values = db.query(
        #     func.avg(Hexagon.KP),
        #     func.avg(Hexagon.LS),
        #     func.avg(Hexagon.EC),
        #     func.avg(Hexagon.PZ),
        #     func.avg(Hexagon.OP),
        #     func.avg(Hexagon.FP)
        # )
        #
        # averages = avg_values.one()
        #
        # avg_KP, avg_LS, avg_EC, avg_PZ, avg_OP, avg_FP = averages

        # averages_read = HexagonAveragesRead(
        #     # KP=avg_KP,
        #     # LS=avg_LS,
        #     # EC=avg_EC,
        #     # PZ=avg_PZ,
        #     # OP=avg_OP,
        #     # FP=avg_FP
        # )
        averages_read = {
            "KP": round(random.uniform(1.01, 5.00), 1),
            "LS": round(random.uniform(1.01, 5.00), 1),
            "EC": round(random.uniform(1.01, 5.00), 1),
            "PZ": round(random.uniform(1.01, 5.00), 1),
            "OP": round(random.uniform(1.01, 5.00), 1),
            "FP": round(random.uniform(1.01, 5.00), 1)
        }

        return averages_read

    # def __get_stats_dict(self, db: Session, obj) -> dict:
    #     stats_dict = {}
    #     for enum_member in StatsEnum:
    #         stats_dict[enum_member.name] = StatRead(
    #             name=enum_member.value['name'],
    #             nameKZ=enum_member.value['nameKZ'],
    #             abb=enum_member.value['abb'],
    #             score=getattr(obj, enum_member.name)
    #         )
    #     return stats_dict


hexagon_service = HexagonService(Hexagon)
