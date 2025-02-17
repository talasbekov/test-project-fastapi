"""migration_30_11_2024_24_09

Revision ID: 253fbd40ddd9
Revises: 
Create Date: 2024-11-30 22:07:27.121428

"""
import re
import uuid
import json
import logging
from datetime import datetime, timedelta
import importlib

import oracledb
from oracledb import Cursor
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Session

from core import get_db, Base
from models import *

from typing import Union, Sequence


# revision identifiers, used by Alembic.
revision: str = '253fbd40ddd9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


oracledb.init_oracle_client()

logging.basicConfig(level=logging.INFO, filename='migration_debug.log', filemode='w')
log = logging.getLogger(__name__)

db = Session(bind=op.get_bind())


days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def convert_days(days):
    def is_leap_year(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    years = days // 365
    months = 0
    remaining_days = days % 365

    # Adjust for leap years
    for year in range(years):
        if is_leap_year(year + 1):
            remaining_days -= 1

    # Calculate the months and remaining days
    for i, days_in_current_month in enumerate(days_in_month):
        if remaining_days >= days_in_current_month:
            months += 1
            remaining_days -= days_in_current_month
        else:
            break

    return years, months, remaining_days

division_context = {}
rank_context = {}

def get_uuid():
    return str(uuid.uuid4())


def extract_integers(string):
    pattern = r"\d+(?:\.\d+)?"
    matches = re.findall(pattern, string)
    floats = [float(match.replace(",", ".")) for match in matches]
    if len(floats) > 1:
        return floats[0] + (floats[1] * 0.1)
    elif len(floats) == 0:
        return 0
    return floats[0]


blood = {  # Группа Крови
    "0-ПОЛОЖИТЕЛЬНЫЙ": BloodType.O_PLUS,
    "0-ОТРИЦАТЕЛЬНЫЙ": BloodType.O_MINUS,
    "А-ПОЛОЖИТЕЛЬНЫЙ": BloodType.A_PLUS,
    "А-ОТРИЦАТЕЛЬНЫЙ": BloodType.A_MINUS,
    "В-ПОЛОЖИТЕЛЬНЫЙ": BloodType.B_PLUS,
    "В-ОТРИЦАТЕЛЬНЫЙ": BloodType.B_MINUS,
    "АВ-ПОЛОЖИТЕЛЬНЫЙ": BloodType.AB_PLUS,
    "АВ-ОТРИЦАТЕЛЬНЫЙ": BloodType.AB_MINUS,
}

lang_level_dic = {
    '002': 1,
    '003': 2,
    '005': 3,
    '001': 4,
    '004': 5
}

competitions = {
 "ҚАЗАҚ КҮРЕСІ СГО":"ҚАЗАҚ КҮРЕСІ",
 "АРМРЕСТЛИНГ":"АРМРЕСТЛИНГ",
 "АШХАРА-КАРАТЭ":"АШХАРА-КАРАТЭ",
 "БОЕВАЯ СТРЕЛЬБА СГО":"БОЕВАЯ СТРЕЛЬБА",
 "БОРЬБА НА ПОЯСАХ":"борьба на поясах",
 "ВОЛЕЙБОЛ СГО":"ВОЛЕЙБОЛ",
 "ГИРЕВОЙ СПОРТ СГО":"ГИРЕВОЙ СПОРТ",
 "ГРЭППЛИНГ МС":"ГРЭППЛИНГ",
 "ГРЭППЛИНГ РК":"ГРЭППЛИНГ",
 "ДЖИУ-ДЖИТСУ":"джиу-джитсу",
 "ЖИМ ЛЕЖА СГО":"ЖИМ ЛЕЖА",
 "КИКБОКСИНГ КУБОК МИРА":"КИКБОКСИНГ",
 "КИКБОКСИНГ РК":"КИКБОКСИНГ",
 "КИКБОКСИНГ ЧА":"КИКБОКСИНГ",
 "КИКБОКСИНГ ЧМ":"КИКБОКСИНГ",
 "КУБОК НАЧАЛЬНИКА СГО РК ПО ПРАКТИЧЕСКОЙ СТРЕЛЬБЕ":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "КУБОК РК ПО ПРАКТИЧЕСКОЙ СТРЕЛЬБЕ":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "ЛИЧНЫЙ ЗАЧЕТ ПРАКТИЧЕСКАЯ СТРЕЛЬБА ГРУППА \"Б\"":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "НАСТОЛЬНЫЙ ТЕННИС СГО":"НАСТОЛЬНЫЙ ТЕННИС",
 "ПАНКРАТИОН РК":"ПАНКРАТИОН",
 "ПАУЭРЛИФТИНГ СГО":"ПАУЭРЛИФТИНГ",
 "ПЛАВАНИЕ СГО":"ПЛАВАНИЕ",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА ГРУППА \"А\" ЛИЧНЫЙ ЗАЧЕТ":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА КУБОК КАЗАКСТАНА":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА МЕЖДУНАРОДНОЕ СОРЕВНОВАНИЕ":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА СГО ГРУППА \"А\"":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА СГО ГРУППА \"Б\"":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА ЧЕМПИОНАТ КАЗАКСТАНА":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "РУКОПАШНЫЙ БОЙ":"РУКОПАШНЫЙ БОЙ",
 "РУКОПАШНЫЙ БОЙ КУБОК МИРА":"РУКОПАШНЫЙ БОЙ",
 "РУКОПАШНЫЙ БОЙ МС":"РУКОПАШНЫЙ БОЙ",
 "РУКОПАШНЫЙ БОЙ РК":"РУКОПАШНЫЙ БОЙ",
 "РУКОПАШНЫЙ БОЙ СГО":"РУКОПАШНЫЙ БОЙ",
 "РУКОПАШНЫЙ БОЙ ЧА":"РУКОПАШНЫЙ БОЙ",
 "РУКОПАШНЫЙ БОЙ ЧЕ":"РУКОПАШНЫЙ БОЙ",
 "РУКОПАШНЫЙ БОЙ ЧМ":"РУКОПАШНЫЙ БОЙ",
 "САМБО":"САМБО",
 "СОРЕВНОВАНИЯ ПО СНАЙПЕРСКИМ ПАРАМ":"СНАЙПЕРСКИЕ ПАРЫ",
 "СОРЕВНОВАНИЯ ПО СНАЙПЕРСКИМ ПАРАМ СГО РК":"СНАЙПЕРСКИЕ ПАРЫ",
 "ТЕЛОХРАНИТЕЛЬ СГО":"ТЕЛОХРАНИТЕЛЬ",
 "ТЕЛОХРАНИТЕЛЬ СГО ГРУППА \"А\"":"ТЕЛОХРАНИТЕЛЬ",
 "ТЕЛОХРАНИТЕЛЬ СГО ГРУППА \"Б\"":"ТЕЛОХРАНИТЕЛЬ",
 "ФУТБОЛ РК":"ФУТБОЛ",
 "ФУТБОЛ СГО":"ФУТБОЛ",
 "ШАХМАТЫ СГО":"ШАХМАТЫ",
 "ЛИЧНЫЙ ЗАЧЕТ \r\nПРАКТИЧЕСКАЯ СТРЕЛЬБА ГРУППА \"Б\"":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "ТРИАТЛОН":"Триатлон",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА С ПИСТОЛЕТА":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА",
 "ПАНКРАТИОН МС":"ПАНКРАТИОН",
 "КАЗАХСКАЯ БОРЬБА":"КАЗАХСКАЯ БОРЬБА",
 "ҚАЗАҚ КҮРЕСІ":"ҚАЗАҚ КҮРЕСІ",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА (ПИСТОЛЕТ) КУБОК РК 1 ЭТАП":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА (ПИСТОЛЕТ)",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА (ПИСТОЛЕТ) КУБОК РК 2 ЭТАП":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА (ПИСТОЛЕТ)",
 "БОКС":"БОКС",
 "РУКОПАШНЫЙ БОЙ ЧРК":"РУКОПАШНЫЙ БОЙ",
 "ЭКСТРЕМАЛЬНОЕ ВОЖДЕНИЕ":"ЭКСТРЕМАЛЬНОЕ ВОЖДЕНИЕ",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА СГО ГРУППА \"А\"":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА СГО ГРУППА \"А\"",
 "ПАНКРАТИОН РК":"ПАНКРАТИОН РК",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА СГО ГРУППА \"Б\"":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА СГО ГРУППА \"Б\"",
 "ТЕЛОХРАНИТЕЛЬ СГО ГРУППА \"А\"":"ТЕЛОХРАНИТЕЛЬ СГО ГРУППА \"А\"",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА (ПИСТОЛЕТ) КУБОК РК 2 ЭТАП":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА (ПИСТОЛЕТ) КУБОК РК 2 ЭТАП",
 "ВИД БОРЬБЫ \"КУРАШ\"":"ВИД БОРЬБЫ \"КУРАШ\"",
 "ЖЕНСКИЕ СОРЕВНОВАНИЯ \"8 МАРТА\"":"ЖЕНСКИЕ СОРЕВНОВАНИЯ \"8 МАРТА\"",
 "ҚОЯН-ҚОЛТЫҚ ҰРЫС MКҚ":"ҚОЯН-ҚОЛТЫҚ ҰРЫС MКҚ",
 "ФУТБОЛ МКҚ":"ФУТБОЛ МКҚ",
 "ЖҮЗУ МКҚ":"ЖҮЗУ МКҚ",
 "СТЕНДІК БАСУ МКҚ":"СТЕНДІК БАСУ МКҚ",
 "ЖЕКПЕ-ЖЕК ҰРЫСЫ ЕБ":"ЖЕКПЕ-ЖЕК ҰРЫСЫ ЕБ",
 "ЖЕКПЕ-ЖЕК ҰРЫСЫ ӘК":"ЖЕКПЕ-ЖЕК ҰРЫСЫ ӘК",
 "ТАЯҚ ТАРТУ":"ТАЯҚ ТАРТУ",
 "ЛИЧНЫЙ ЗАЧЕТ \nПРАКТИЧЕСКАЯ СТРЕЛЬБА ГРУППА \"Б\"":"ЛИЧНЫЙ ЗАЧЕТ \nПРАКТИЧЕСКАЯ СТРЕЛЬБА ГРУППА \"Б\"",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА (ПИСТОЛЕТ) КУБОК РК 1 ЭТАП":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА (ПИСТОЛЕТ) КУБОК РК 1 ЭТАП",
 "ЧЕМПИОНАТ ГОРОДА ПО ЖИМУ ЛЕЖА":"ЧЕМПИОНАТ ГОРОДА ПО ЖИМУ ЛЕЖА",
 "ФУТБОЛ ҚР":"ФУТБОЛ ҚР",
 "ВОЛЕЙБОЛ МКҚ":"ВОЛЕЙБОЛ МКҚ",
 "ПАНКРАТИОН ҚР":"ПАНКРАТИОН ҚР",
 "ҚАЗАҚ КҮРЕСІ МКҚ":"ҚАЗАҚ КҮРЕСІ МКҚ",
 "КИКБОКСИНГ ӘБ":"КИКБОКСИНГ ӘБ",
 "КИКБОКСИНГ РК":"КИКБОКСИНГ РК",
 "ШАХМАТЫ СГО":"ШАХМАТЫ СГО",
 "СОРЕВНОВАНИЯ ПО СНАЙПЕРСКИМ ПАРАМ СГО РК":"СОРЕВНОВАНИЯ ПО СНАЙПЕРСКИМ ПАРАМ СГО РК",
 "РУКОПАШНЫЙ БОЙ ЧА":"РУКОПАШНЫЙ БОЙ ЧА",
 "ДЖИУ-ДЖИТСУ":"ДЖИУ-ДЖИТСУ",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА ЧРК (ПИСТОЛЕТ)":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА ЧРК (ПИСТОЛЕТ)",
 "ПАУЭРЛИФТИНГ":"ПАУЭРЛИФТИНГ",
 "ТРИАТЛОН":"ТРИАТЛОН",
 "ЧМ THE UAE SWAT CHALLENGE (ДУБАЙ)":"ЧМ THE UAE SWAT CHALLENGE (ДУБАЙ)",
 "ДЖИУ-ДЖИТСУ МЕЖДУНАРОДНЫЙ ТУРНИР":"ДЖИУ-ДЖИТСУ МЕЖДУНАРОДНЫЙ ТУРНИР",
 "КИКБОКСИНГ ҚР":"КИКБОКСИНГ ҚР",
 "ЖЕКЕ БІРІНШІЛІК\nПРАКТИКАЛЫҚ АТЫС \"А\" ТОБЫ":"ЖЕКЕ БІРІНШІЛІК\nПРАКТИКАЛЫҚ АТЫС \"А\" ТОБЫ",
 "КИКБОКСИНГ ӘК":"КИКБОКСИНГ ӘК",
 "\"КУРАШ\" КҮРЕС ТҮРІ":"\"КУРАШ\" КҮРЕС ТҮРІ",
 "ВОЛЕЙБОЛ СГО":"ВОЛЕЙБОЛ СГО",
 "СОРЕВНОВАНИЯ ПО СНАЙПЕРСКИМ ПАРАМ":"СОРЕВНОВАНИЯ ПО СНАЙПЕРСКИМ ПАРАМ",
 "РУКОПАШНЫЙ БОЙ КУБОК МИРА":"РУКОПАШНЫЙ БОЙ КУБОК МИРА",
 "КУБОК РК ПО ПРАКТИЧЕСКОЙ СТРЕЛЬБЕ":"КУБОК РК ПО ПРАКТИЧЕСКОЙ СТРЕЛЬБЕ",
 "ЛЕДОВОЕ РАЛЛИ":"ЛЕДОВОЕ РАЛЛИ",
 "ҚАЗАҚ КҮРЕСІ":"ҚАЗАҚ КҮРЕСІ",
 "ПРАКТИКАЛЫҚ АТЫС МКҚ \"А\" ТОБЫ":"ПРАКТИКАЛЫҚ АТЫС МКҚ \"А\" ТОБЫ",
 "ҮСТЕЛ ТЕННИСІ МКҚ":"ҮСТЕЛ ТЕННИСІ МКҚ",
 "ПРАКТИКАЛЫҚ АТЫС МКҚ \"Б\" ТОБЫ":"ПРАКТИКАЛЫҚ АТЫС МКҚ \"Б\" ТОБЫ",
 "ПРАКТИКАЛЫҚ АТЫС ХАЛЫҚАРАЛЫҚ ЖАРЫС \"MOSKOV OPEN\"":"ПРАКТИКАЛЫҚ АТЫС ХАЛЫҚАРАЛЫҚ ЖАРЫС \"MOSKOV OPEN\"",
 "ЖЕКПЕ-ЖЕК ҰРЫСЫ АБ":"ЖЕКПЕ-ЖЕК ҰРЫСЫ АБ",
 "РУКОПАШНЫЙ БОЙ СГО":"РУКОПАШНЫЙ БОЙ СГО",
 "ФУТБОЛ СГО":"ФУТБОЛ СГО",
 "БОЕВАЯ СТРЕЛЬБА СГО":"БОЕВАЯ СТРЕЛЬБА СГО",
 "РУКОПАШНЫЙ БОЙ ЧМ":"РУКОПАШНЫЙ БОЙ ЧМ",
 "КИКБОКСИНГ ЧМ":"КИКБОКСИНГ ЧМ",
 "КИКБОКСИНГ КУБОК МИРА":"КИКБОКСИНГ КУБОК МИРА",
 "МАС-РЕСТЛИНГ":"МАС-РЕСТЛИНГ",
 "РУКОПАШНЫЙ БОЙ ДО 23 ЛЕТ":"РУКОПАШНЫЙ БОЙ ДО 23 ЛЕТ",
 "РУКОПАШНЫЙ БОЙ ЧРК":"РУКОПАШНЫЙ БОЙ ЧРК",
 "РУКОПАШНЫЙ БОЙ КУБОК КАЗАХСТАНА":"РУКОПАШНЫЙ БОЙ КУБОК КАЗАХСТАНА",
 "ГІР КӨТЕРУ МКҚ":"ГІР КӨТЕРУ МКҚ",
 "ЖАУЫНГЕРЛІК АТЫС МКҚ":"ЖАУЫНГЕРЛІК АТЫС МКҚ",
 "МЕРГЕНДІК ЖҰПТАР АРАСЫНДАҒЫ ЖАРЫСТАР МКҚ ҚР":"МЕРГЕНДІК ЖҰПТАР АРАСЫНДАҒЫ ЖАРЫСТАР МКҚ ҚР",
 "ПРАКТИКАЛЫҚ АТЫС ҚАЗАҚСТАН КУБОГІ":"ПРАКТИКАЛЫҚ АТЫС ҚАЗАҚСТАН КУБОГІ",
 "ПРАКТИКАЛЫҚ АТУДАН ҚР МКҚ БАСТЫҒЫНЫҢ КУБОГІ":"ПРАКТИКАЛЫҚ АТУДАН ҚР МКҚ БАСТЫҒЫНЫҢ КУБОГІ",
 "ОҚҚАҒАР МКҚ \"А\" ТОБЫ":"ОҚҚАҒАР МКҚ \"А\" ТОБЫ",
 "ПРАКТИКАЛЫҚ АТЫСТАН ҚР КУБГІ":"ПРАКТИКАЛЫҚ АТЫСТАН ҚР КУБГІ",
 "ҚОЯН-ҚОЛТЫҚ ҰРЫС 23 ЖАСҚА ДЕЙІН":"ҚОЯН-ҚОЛТЫҚ ҰРЫС 23 ЖАСҚА ДЕЙІН",
 "ТЕЛОХРАНИТЕЛЬ СГО":"ТЕЛОХРАНИТЕЛЬ СГО",
 "ҚАЗАҚ КҮРЕСІ СГО":"ҚАЗАҚ КҮРЕСІ СГО",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА ГРУППА \"А\" ЛИЧНЫЙ ЗАЧЕТ":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА ГРУППА \"А\" ЛИЧНЫЙ ЗАЧЕТ",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА КУБОК КАЗАКСТАНА":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА КУБОК КАЗАКСТАНА",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА (КАРБИН) ЧЕМПИОНАТ РК":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА (КАРБИН) ЧЕМПИОНАТ РК",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА ЧРК (ПИСТОЛЕТ) ЛИЧНЫЙ ЗАЧЕТ":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА ЧРК (ПИСТОЛЕТ) ЛИЧНЫЙ ЗАЧЕТ",
 "КИК-БОКСИНГ КУБОК КАЗАХСТАНА":"КИК-БОКСИНГ КУБОК КАЗАХСТАНА",
 "ОҚҚАҒАР МКҚ \"Б\" ТОБЫ":"ОҚҚАҒАР МКҚ \"Б\" ТОБЫ",
 "ШАХМАТ МКҚ":"ШАХМАТ МКҚ",
 "ЖЕКПЕ-ЖЕК ҰРЫСЫ MКҚ":"ЖЕКПЕ-ЖЕК ҰРЫСЫ MКҚ",
 "ПРАКТИКАЛЫҚ АТУ ҚРЧ (ТАПАНША)":"ПРАКТИКАЛЫҚ АТУ ҚРЧ (ТАПАНША)",
 "АРМРЕСТЛИНГ":"АРМРЕСТЛИНГ",
 "ГИРЕВОЙ СПОРТ СГО":"ГИРЕВОЙ СПОРТ СГО",
 "ЖИМ ЛЕЖА СГО":"ЖИМ ЛЕЖА СГО",
 "РУКОПАШНЫЙ БОЙ ЧЕ":"РУКОПАШНЫЙ БОЙ ЧЕ",
 "КИКБОКСИНГ ЧА":"КИКБОКСИНГ ЧА",
 "СМЕШАННЫЕ БОЕВЫЕ ИСКУССТВА ММА":"СМЕШАННЫЕ БОЕВЫЕ ИСКУССТВА ММА",
 "МАС-РЕСТЛИНГЕ":"МАС-РЕСТЛИНГЕ",
 "ЭКСТРЕМАЛЬНОЕ ВОЖДЕНИЕ":"ЭКСТРЕМАЛЬНОЕ ВОЖДЕНИЕ",
 "РУКОПАШНЫЙ БОЙ - МЕЖДУНАРОДНЫЙ ТУРНИР":"РУКОПАШНЫЙ БОЙ - МЕЖДУНАРОДНЫЙ ТУРНИР",
 "РУКОПАШНЫЙ БОЙ - САМООБОРОНА":"РУКОПАШНЫЙ БОЙ - САМООБОРОНА",
 "ОҚҚАҒАР МКҚ":"ОҚҚАҒАР МКҚ",
 "ПРАКТИКАЛЫҚ АТЫСТАН \"Б\" ТОБЫ\nЖЕКЕ БІРІНШІЛІК":"ПРАКТИКАЛЫҚ АТЫСТАН \"Б\" ТОБЫ\nЖЕКЕ БІРІНШІЛІК",
 "КИКБОКСИНГ АБ":"КИКБОКСИНГ АБ",
 "ПРАКТИКАЛЫҚ АТУ (КАРАБИН) ҚР ЧЕМПИОНАТЫ":"ПРАКТИКАЛЫҚ АТУ (КАРАБИН) ҚР ЧЕМПИОНАТЫ",
 "ММА АРАЛАС ЖЕКПЕ-ЖЕК":"ММА АРАЛАС ЖЕКПЕ-ЖЕК",
 "ЭКСТРЕМАЛДЫ ЖҮРГІЗҮ":"ЭКСТРЕМАЛДЫ ЖҮРГІЗҮ",
 "ФУТБОЛ РК":"ФУТБОЛ РК",
 "НАСТОЛЬНЫЙ ТЕННИС СГО":"НАСТОЛЬНЫЙ ТЕННИС СГО",
 "ТЕЛОХРАНИТЕЛЬ СГО ГРУППА \"Б\"":"ТЕЛОХРАНИТЕЛЬ СГО ГРУППА \"Б\"",
 "САМБО":"САМБО",
 "ПЛАВАНИЕ СГО":"ПЛАВАНИЕ СГО",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА ЧЕМПИОНАТ КАЗАКСТАНА":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА ЧЕМПИОНАТ КАЗАКСТАНА",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА МЕЖДУНАРОДНОЕ СОРЕВНОВАНИЕ":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА МЕЖДУНАРОДНОЕ СОРЕВНОВАНИЕ",
 "КУБОК НАЧАЛЬНИКА СГО РК ПО ПРАКТИЧЕСКОЙ СТРЕЛЬБЕ":"КУБОК НАЧАЛЬНИКА СГО РК ПО ПРАКТИЧЕСКОЙ СТРЕЛЬБЕ",
 "КИК-БОКСИН МЕЖДУНАРОДНЫЙ ТУРНИР":"КИК-БОКСИН МЕЖДУНАРОДНЫЙ ТУРНИР",
 "ПАУЭРЛИФТИНГ ЧЕМПИОНАТ АЗИИ":"ПАУЭРЛИФТИНГ ЧЕМПИОНАТ АЗИИ",
 "БОКС":"БОКС",
 "МЕРГЕНДІК ЖҰПТАР АРАСЫНДАҒЫ ЖАРЫСТАР":"МЕРГЕНДІК ЖҰПТАР АРАСЫНДАҒЫ ЖАРЫСТАР",
 "ПРАКТИКАЛЫҚ АТЫС ҚАЗАҚСТАН ЧЕМПИОНАТЫ":"ПРАКТИКАЛЫҚ АТЫС ҚАЗАҚСТАН ЧЕМПИОНАТЫ",
 "ЖЕКПЕ-ЖЕК ӘБ":"ЖЕКПЕ-ЖЕК ӘБ",
 "ПРАКТИКАЛЫҚ АТУ (ТАПАНША) ҚР КУБОГІ 1 КЕЗЕҢ":"ПРАКТИКАЛЫҚ АТУ (ТАПАНША) ҚР КУБОГІ 1 КЕЗЕҢ",
 "ПРАКТИКАЛЫҚ АТУ (ТАПАНША) ҚР КУБОГІ 2 КЕЗЕҢ":"ПРАКТИКАЛЫҚ АТУ (ТАПАНША) ҚР КУБОГІ 2 КЕЗЕҢ",
 "ПРАКТИКАЛЫҚ АТУ ҚРЧ (ТАПАНША) ЖЕКЕ БІРІНШІЛІК":"ПРАКТИКАЛЫҚ АТУ ҚРЧ (ТАПАНША) ЖЕКЕ БІРІНШІЛІК",
 "ДЗЮДО":"ДЗЮДО",
 "ЧЕМПИОНАТ МИРА":"ЧЕМПИОНАТ МИРА",
 "ГРЭППЛИНГ МС":"ГРЭППЛИНГ МС",
 "ГРЭППЛИНГ РК":"ГРЭППЛИНГ РК",
 "КАЗАХСКАЯ БОРЬБА":"КАЗАХСКАЯ БОРЬБА",
 "СМЕШАННЫЕ БОЕВЫЕ ИСКУССТВА ММА МС":"СМЕШАННЫЕ БОЕВЫЕ ИСКУССТВА ММА МС",
 "БОРЬБА НА ПОЯСАХ":"БОРЬБА НА ПОЯСАХ",
 "ЭКСТРЕМАЛЬНОЕ ВОЖДЕНИЕ":"ЭКСТРЕМАЛЬНОЕ ВОЖДЕНИЕ",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА (КАРАБИН) ЧЕМПИОНАТ РК":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА (КАРАБИН) ЧЕМПИОНАТ РК",
 "УНИВЕРСАЛЬНЫЕ БОИ":"УНИВЕРСАЛЬНЫЕ БОИ",
 "ПАУЭРЛИФТИНГ ЧЕМПИОНАТ АЗИИ":"ПАУЭРЛИФТИНГ ЧЕМПИОНАТ АЗИИ",
 "ВОЛЬНАЯ БОРЬБА":"ВОЛЬНАЯ БОРЬБА",
 "МЕЖДУНАРОДНЫЙ ТУРНИР":"МЕЖДУНАРОДНЫЙ ТУРНИР",
 "РУКОПАШНЫЙ БОЙ":"РУКОПАШНЫЙ БОЙ",
 "ТАЭКВОН-ДО":"ТАЭКВОН-ДО",
 "РУКОПАШНЫЙ БОЙ КУБОК КАЗАХСТАНА":"РУКОПАШНЫЙ БОЙ КУБОК КАЗАХСТАНА",
 "ЧЕМПИОНАТ ГОРОДА ПО ЖИМУ ЛЕЖА":"ЧЕМПИОНАТ ГОРОДА ПО ЖИМУ ЛЕЖА",
 "АБСОЛЮТНЫЙ РЕАЛЬНЫЙ БОЙ":"АБСОЛЮТНЫЙ РЕАЛЬНЫЙ БОЙ",
 "АШХАРА-КАРАТЭ":"АШХАРА-КАРАТЭ",
 "ПАУЭРЛИФТИНГ СГО":"ПАУЭРЛИФТИНГ СГО",
 "ПРАКТИЧЕСКАЯ СТРЕЛЬБА С ПИСТОЛЕТА":"ПРАКТИЧЕСКАЯ СТРЕЛЬБА С ПИСТОЛЕТА",
 "РУКОПАШНЫЙ БОЙ СГО":"РУКОПАШНЫЙ БОЙ СГО",
 "РУКОПАШНЫЙ БОЙ - САМООБОРОНА":"РУКОПАШНЫЙ БОЙ - САМООБОРОНА",
 "РУКОПАШНЫЙ БОЙ РК":"РУКОПАШНЫЙ БОЙ РК",
 "СОРЕВНОВАНИЯ ПО СТРЕЛЬБЕ":"СОРЕВНОВАНИЯ ПО СТРЕЛЬБЕ",
 "РУКОПАШНЫЙ БОЙ - МЕЖДУНАРОДНЫЙ ТУРНИР":"РУКОПАШНЫЙ БОЙ - МЕЖДУНАРОДНЫЙ ТУРНИР",
 "ПАНКРАТИОН МС":"ПАНКРАТИОН МС",
 "ПЕРЕТЯГИВАНИЕ КАНАТА":"ПЕРЕТЯГИВАНИЕ КАНАТА",
 "РУКОПАШНЫЙ БОЙ МС":"РУКОПАШНЫЙ БОЙ МС",
 "БОКС":"БОКС",
 "КИК-БОКСИНГ КУБОК КАЗАХСТАНА":"КИК-БОКСИНГ КУБОК КАЗАХСТАНА",
 "ЛЕДОВОЕ РАЛЛИ":"ЛЕДОВОЕ РАЛЛИ",
 "КИКБОКСИНГ МС":"КИКБОКСИНГ МС",
 "СМЕШАННЫЕ БОЕВЫЕ ИСКУССТВА ММА РК":"СМЕШАННЫЕ БОЕВЫЕ ИСКУССТВА ММА РК",
 "КИКБОКСИНГ":"КИКБОКСИНГ"

  
  
}


def get_age_group(birthdate):
    years, _, _ = convert_days((datetime.now() - birthdate).days)
    if years <= 25 or years is None:
        return AgeGroup.FIRST
    elif years <= 30:
        return AgeGroup.SECOND
    elif years <= 35:
        return AgeGroup.THIRD
    elif years <= 40:
        return AgeGroup.FOURTH
    elif years <= 45:
        return AgeGroup.FIFTH
    return AgeGroup.SIXTH

special_group_staff_division = StaffDivision(
    id=get_uuid(),
    name="Особая группа",
    nameKZ="Особая группа",
    is_combat_unit=1,
    staff_division_number=1
)
db.add(special_group_staff_division)
db.flush()

counter = 1

# new_contract_type = ContractType(
#     id=get_uuid(),
#     name="Контракт",
#     nameKZ="Келісімшарт",
#     years=-1,
#     is_finite=True,
# )
# db.add(new_contract_type)
# db.flush()

def create_user(
    cursor: Cursor,
    db: Session,
    e_id,
    surname,
    name,
    father_name,
    officer_number,
    iin,
    family_status_name,
    service_id_number,
    service_id_end_date,
    fact_address,
    reg_address,
    gender,
    position_name,
    division_id,
    post_order_confirmer,
    post_order_number,
    post_order_date,
    birthdate,
    birth_place,
    nationality,
    blood_group,
    height,
    weight,
    hat_size,
    clothes_size,
    shoes_size,
    position_id,
    group_id,
    staff_unit_id,
    actual_staff_unit_id,
    status_id,
    rank_id,
):
    id = get_uuid()

    sql = f"""select  distinct(emp.id),concat(emp.IIN,'@sgo.kz')as email,
FIRSTNAME, SURNAME,PATRONYMIC,pphone.phone_number as CALLSIGN,OFFICER_NUMBER,
phone.PHONE_NUMBER,
sphone.PHONE_NUMBER,iin,emp.BIRTHDATE
from HR_EMPLOYEES emp 
left join HR_EMP_PHONES phone on phone.EMPLOYEE_ID = emp.ID and phone.PHONE_TYPE_ID= 2 
left join dic_hr_rank dr on dr.id = emp.RANK_ID 
left join HR_EMP_PHONES sphone on sphone.EMPLOYEE_ID = emp.ID and sphone.PHONE_TYPE_ID=3
left join HR_EMP_PHONES pphone on pphone.EMPLOYEE_ID = emp.ID and pphone.PHONE_TYPE_ID=15
        where emp.id = {e_id}"""

    (
        emp_id,
        email,
        name,
        surname,
        father_name,
        callsign,
        officer_number,
        phone_number,
        sphone,
        iin,
        birthdate,
    ) = cursor.execute(sql).fetchone()
    
    v_actual_position_id = None
    actual_position_id = None
    position_status = None
    position_status_kz = None
    if status_id == 1:
        return None
        # division_id = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.CANDIDATES.value).first().id
        # position_id = db.query(Position).filter(Position.name == PositionNameEnum.CANDIDATE.value).first().id
    elif status_id == 2 or status_id == 3:
        position_sql = f"""SELECT 
t.POST_CATEGORY_ru CATEGORY, 
case when
  nvl(t.INSTEAD_OF_POST_ID,0)=0 then (select max_rank_id from hr_position_structure where id = t.post_id)
  else
(select max_rank_id from hr_position_structure where id = t.INSTEAD_OF_POST_ID) end as max_rank_id,
case
           when nvl(t.division_id, 0) = 0 and nvl(t.post_id, 0) = 0 and
                nvl(t.instead_of_post_id, 0) = 0 and
                nvl(t.dic_post_instd_id, 0) = 0 and
                nvl(t.order_begin_id, 0) = 0 and t.is_readonly = 0 then
            t.post_ru
           when nvl(t.instead_of_post_id, 0) <> 0 then
            (select dhp.name_ru
               from dic_hr_postname dhp
              where dhp.id = t.dic_post_instd_id)
           when nvl(t.post_id, 0) <> 0 then
            (select dhp.name_ru
               from hr_position_structure hps
               join dic_hr_postname dhp
                 on dhp.id = hps.position_id
              where hps.id = t.post_id)
           when nvl(t.dic_post_instd_id, 0) <> 0 then
            (select dhp.name_ru
               from dic_hr_postname dhp
              where dhp.id = t.dic_post_instd_id)
           when exists (select 1
                   from dic_hr_order_type dhot
                  where dhot.id = t.order_begin_type_id
                    and dhot.code in ('002', '006', '008')) then
            (select yn.name_ru
               from dic_adm_yes_no yn
              where yn.code = 'AT_COMMAND')
           else
            null
         end as position,
         
case
           when nvl(t.division_id, 0) = 0 and nvl(t.post_id, 0) = 0 and
                nvl(t.instead_of_post_id, 0) = 0 and
                nvl(t.dic_post_instd_id, 0) = 0 and
                nvl(t.order_begin_id, 0) = 0 and t.is_readonly = 0 then
            t.post_ru
           when nvl(t.instead_of_post_id, 0) <> 0 then
            (select dhp.name_kz
               from dic_hr_postname dhp
              where dhp.id = t.dic_post_instd_id)
           when nvl(t.post_id, 0) <> 0 then
            (select dhp.name_kz
               from hr_position_structure hps
               join dic_hr_postname dhp
                 on dhp.id = hps.position_id
              where hps.id = t.post_id)
           when nvl(t.dic_post_instd_id, 0) <> 0 then
            (select dhp.name_kz
               from dic_hr_postname dhp
              where dhp.id = t.dic_post_instd_id)
           when exists (select 1
                   from dic_hr_order_type dhot
                  where dhot.id = t.order_begin_type_id
                    and dhot.code in ('002', '006', '008')) then
            (select yn.name_kz
               from dic_adm_yes_no yn
              where yn.code = 'AT_COMMAND')
           else
            null
         end as position_kz,          
t.INSTEAD_OF_POST_ru INSTEAD_POSITION, 
t.INSTEAD_OF_POST_kz INSTEAD_POSITION_KZ, 
p.division_id DIVISION
FROM hr_emp_soprecords_v t
left join hr_position_structure p on 
t.instead_of_post_id = p.id or t.post_id = p.id 
WHERE t.EMPLOYEE_ID = {emp_id} and t.is_activ = 1 order by t.begin_date desc
        """


        position_res = cursor.execute(position_sql).fetchone()
        if position_res is None:
            return
        (
            category_name,
            pos_rank_id,
            my_position_name,
            my_position_name_kz,
			instead_position_name,
			instead_position_nameKZ,
            my_division_id,
        ) = position_res
        if instead_position_name is not None:
            # actual_division = db.query(StaffDivision).filter(StaffDivision.id == division_context.get(my_division_id)).first()
            # if actual_division is not None:
            #     actual_division_id = actual_division.id
            actual_position = db.query(Position).filter(func.lower(Position.name) == instead_position_name.lower()).first()
            if actual_position is None:
                actual_found_rank = db.query(Rank).filter(Rank.id == rank_context.get(pos_rank_id)).first()
                if actual_found_rank is not None:
                    actual_pos_rank_id = actual_found_rank.id
                else:
                    actual_pos_rank_id = None

                actual_position_id = str(get_uuid())
                op.bulk_insert(
                    Base.metadata.tables["hr_erp_positions"],
                    [{
                        "id": actual_position_id,
                        'name': my_position_name,
                        'namekz': my_position_name_kz,
                        'max_rank_id': actual_pos_rank_id,
                        'category_code': category_name,
                        'form': 'Форма 1'
                    }]
                )
            else:
                actual_position_id = actual_position.id
        else:
            actual_position_id = None

        division = db.query(StaffDivision).filter(StaffDivision.id == division_context.get(my_division_id)).first()
        if division is not None:
            division_id = division.id
        position = db.query(Position).filter(func.lower(Position.name) == my_position_name.lower()).first()
        if position is None:
            found_rank = db.query(Rank).filter(Rank.id == rank_context.get(pos_rank_id)).first()
            if found_rank is not None:
                pos_rank_id = found_rank.id
            else:
                pos_rank_id = None

            position_id = str(get_uuid())
            op.bulk_insert(
                Base.metadata.tables["hr_erp_positions"],
                [{
                    "id": position_id,
                    'name': my_position_name,
                    'namekz': my_position_name_kz,
                    'max_rank_id': pos_rank_id,
                    'category_code': category_name,
                    'form': 'Форма 1'
                }]
            )
        else:
            position_id = position.id
    elif status_id == 5:
        res_division = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.IN_RESERVE.value).first()
        if(res_division is not None):
            division_id = res_division.id
        else:
            division_id = None
        position = db.query(Position).filter(Position.name == PositionNameEnum.IN_RESERVE.value).first()
        if(position is not None):
            position_id = position.id
            position_status = position.name
            position_status_kz = position.nameKZ
    elif status_id == 7:
        division_id = None
        position = db.query(Position).filter(Position.name == PositionNameEnum.OUT_STAFF.value).first()
        if(position is not None):
            position_id = position.id
            position_status = position.name
            position_status_kz = position.nameKZ
    elif status_id == 8:
        division_id = None
        position = db.query(Position).filter(Position.name == PositionNameEnum.RETIRED.value).first()
        if(position is not None):
            position_id = position.id
            position_status = position.name
            position_status_kz = position.nameKZ
    elif status_id == 9:
        division_id = None
        position = db.query(Position).filter(Position.name == PositionNameEnum.DEAD.value).first()
        if(position is not None):
            position_id = position.id
            position_status = position.name
            position_status_kz = position.nameKZ
    if position_status is not None:
        type = db.query(StatusType).filter(
            func.to_char(func.lower(StatusType.name)) == position_status.lower()).first()
        if type is None:
            type_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_status_types"],
                [{
                    "id": type_id,
                    'name': position_status,
                    'namekz': position_status_kz,
                    'form': 'Форма 1'
                }]
            )
        else:
            type_id = type.id

        status_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_statuses"],
            [{
                "id": status_id,
                'user_id': id,
                'type_id': type_id,
            }]
        )
    #
    # if v_actual_position_id is not None:
    #     op.bulk_insert(
    #         Base.metadata.tables["hr_erp_staff_units"],
    #         [
    #             {
    #                 "id": actual_staff_unit_id,
    #                 "position_id": actual_position_id,
    #                 "staff_division_id": actual_division_id,
    #                 "user_replacing_id": " ",
    #                 "requirements": json.dumps([
    #                     {
    #                         "name": "Требования к образованию",
    #                         "nameKZ": "Білім талаптары",
    #                         "keys": [
    #                             {
    #                                 "text": ["Высшее профессиональное"],
    #                                 "lang": "ru",
    #                             },
    #                             {"text": ["Жоғары кәсіпкерлік"], "lang": "kz"},
    #                         ],
    #                     },
    #                     {
    #                         "name": "Требования к стажу",
    #                         "nameKZ": "Тәжірибе талаптары",
    #                         "keys": [
    #                             {
    #                                 "text": [
    #                                     "10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
    #                                     "4 года стажа работы на руководящих должностях",
    #                                 ],
    #                                 "lang": "ru",
    #                             },
    #                             {
    #                                 "text": [
    #                                     "Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
    #                                     "4 жыл басшы лауазымдардағы жұмыс өтілі",
    #                                 ],
    #                                 "lang": "kz",
    #                             },
    #                         ],
    #                     },
    #                     {
    #                         "name": "Практический опыт",
    #                         "nameKZ": "Практикалық тәжірибе",
    #                         "keys": [
    #                             {
    #                                 "text": [
    #                                     "Наличие обязательных знаний, умений и навыков"
    #                                 ],
    #                                 "lang": "ru",
    #                             },
    #                             {
    #                                 "text": [
    #                                     "Міндетті білімнің, іскерліктің және дағдылардың болуы"
    #                                 ],
    #                                 "lang": "kz",
    #                             },
    #                         ],
    #                     },
    #                     {
    #                         "name": "Требования по состоянию здоровья",
    #                         "nameKZ": "Денсаулық талаптары",
    #                         "keys": [
    #                             {
    #                                 "text": ["Пригодность по состоянию здоровья"],
    #                                 "lang": "ru",
    #                             },
    #                             {
    #                                 "text": [
    #                                     "Денсаулық жағдайы бойынша жарамдылық"
    #                                 ],
    #                                 "lang": "kz",
    #                             },
    #                         ],
    #                     },
    #                 ]),
    #             }
    #         ],
    #     )
    # else:
    #     actual_staff_unit_id = staff_unit_id

    if actual_position_id is not None:
        swap_position = position_id
        position_id = actual_position_id
        actual_position_id = swap_position

    op.bulk_insert(
        Base.metadata.tables["hr_erp_staff_units"],
        [
            {
                "id": staff_unit_id,
                "position_id": position_id,
                "actual_position_id": actual_position_id,
                "staff_division_id": division_id,
                "user_replacing_id": " ",
                "requirements": json.dumps([
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru",
                            },
                            {"text": ["Жоғары кәсіпкерлік"], "lang": "kz"},
                        ],
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": [
                                    "10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                    "4 года стажа работы на руководящих должностях",
                                ],
                                "lang": "ru",
                            },
                            {
                                "text": [
                                    "Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                    "4 жыл басшы лауазымдардағы жұмыс өтілі",
                                ],
                                "lang": "kz",
                            },
                        ],
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": [
                                    "Наличие обязательных знаний, умений и навыков"
                                ],
                                "lang": "ru",
                            },
                            {
                                "text": [
                                    "Міндетті білімнің, іскерліктің және дағдылардың болуы"
                                ],
                                "lang": "kz",
                            },
                        ],
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru",
                            },
                            {
                                "text": [
                                    "Денсаулық жағдайы бойынша жарамдылық"
                                ],
                                "lang": "kz",
                            },
                        ],
                    },
                ]),
            }
        ],
    )
    while (
        callsign is not None
        and db.query(User).filter(User.call_sign == callsign).first()
        is not None
    ):
        callsign = f"0{callsign}"

    found_rank = db.query(Rank).filter(Rank.id == rank_context.get(rank_id)).first()
    if found_rank is None:
        found_rank = db.query(Rank).filter(Rank.name == "рядовой").first()
    op.bulk_insert(
        Base.metadata.tables["hr_erp_users"],
        [
            {
                "id": id,
                "email": email,
                "password": "$2b$12$vhg69KJxWiGgetoLxGRvie3VxElPt45i4ELJiE/V2qOj30X3c3.7m",
                "first_name": name,
                "last_name": surname,
                "father_name": father_name,
                "staff_unit_id": staff_unit_id,
                "date_birth": birthdate,
                "supervised_by": " ",
                "call_sign": callsign,
                "id_number": officer_number,
                "phone_number": phone_number,
                "rank_id": str(found_rank.id),
                "actual_staff_unit_id": actual_staff_unit_id,
                "icon": f"https://10.15.3.180/s3/static/{iin}.jpg",
                "service_phone_number": sphone,
                "personal_id": str(emp_id),
                "is_military": True,
                "cabinet": "cabinet",
                "address": fact_address,
                "iin": str(iin),
                "is_active": 0 if status_id == 8 or status_id == 9 else 1,
            }
        ],
    )

    profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_profiles"],
        [
            {
                "id": profile_id,
                "user_id": id,
            }
        ],
    )

    personal_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_personal_profiles"],
        [
            {
                "id": personal_profile_id,
                "profile_id": profile_id,
            }
        ],
    )

    educational_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_educational_profiles"],
        [{"id": educational_profile_id, "profile_id": profile_id}],
    )

    medical_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_medical_profiles"],
        [{"id": medical_profile_id, "profile_id": profile_id}],
    )

    additional_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_additional_profiles"],
        [{"id": additional_profile_id, "profile_id": profile_id}],
    )

    family_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_family_profiles"],
        [{"id": family_profile_id, "profile_id": profile_id}],
    )

    # Medical Profile

    general_user_information_id = get_uuid()

    blood_group_enum = blood.get(blood_group, None)

    op.bulk_insert(
        Base.metadata.tables["hr_erp_general_user_info"],
        [
            {
                "id": general_user_information_id,
                "height": int(float(extract_integers(height)))
                if height is not None
                else None,
                "blood_group": blood_group_enum.value
                if blood_group_enum is not None
                else None,
                "age_group": get_age_group(birthdate),
                "profile_id": medical_profile_id,
                "weight": int(float(extract_integers(weight)))
                if weight is not None
                else None,
            }
        ],
    )

    anthropometric_data_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_anthropometric_data"],
        [
            {
                "id": anthropometric_data_id,
                "head_circumference": int(
                    float(
                        extract_integers(hat_size.split("-")[0].split("/")[0])
                    )
                )
                if hat_size is not None
                else None,
                "shoe_size": int(
                    float(
                        extract_integers(
                            shoes_size.split("-")[0].split("/")[0]
                        )
                    )
                )
                if shoes_size is not None
                else None,
                "neck_circumference": 35,
                "shape_size": int(
                    float(
                        extract_integers(
                            clothes_size.split("-")[0].split("/")[0]
                        )
                    )
                )
                if clothes_size is not None
                else None,
                "bust_size": 56,
                "profile_id": medical_profile_id,
            }
        ],
    )

    hospital_data_sql = f"""SELECT t.ID, 
                            t.BEGIN_DATE, 
                            t.END_DATE, 
                            t.DOCUMENT_ru AS DOCUMENT
                            FROM hr_emp_absences t WHERE t.ABSENCE_TYPE_ID = 3
                            AND t.EMPLOYEE_ID = {emp_id} order by t.BEGIN_DATE"""
    hospital_datas = cursor.execute(hospital_data_sql).fetchall()

    for hospital_data in hospital_datas:
        (absence_id,
         begin_date,
         end_date,
         document_name
         ) = hospital_data



        hospital_data_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_hospital_datas"],
            [
                {
                    "id": hospital_data_id,
                    "profile_id": medical_profile_id,
                    "start_date": begin_date,
                    "end_date": end_date,
                    "reason": document_name,
                    "reasonkz": document_name,
                    "code": str(absence_id),
                    "document_link": 'https://10.15.3.180',
                    "medical_profile_id": medical_profile_id,
                    "place": " ",
                    "placekz": " ",
                    "illness_type_id": ""

                }
            ],
        )

    # Personal Profile

    f_status = (
        db.query(FamilyStatus)
        .filter(
            func.lower(FamilyStatus.name).contains(family_status_name.lower())
        )
        .first()
    )

    biographic_info_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_biographic_infos"],
        [
            {
                "id": biographic_info_id,
                "place_birth": birth_place,
                "gender": gender,
                "citizenship": "Казахстан",
                "nationality": nationality,
                "family_status_id": str(f_status.id) if f_status else None,
                "address": reg_address,
                "residence_address": fact_address if fact_address else '',
                "profile_id": personal_profile_id,
                "personal_profile_id": personal_profile_id
            }
        ],
    )

    tax_declaration1_id = get_uuid()
    tax_declaration2_id = get_uuid()
    tax_declaration3_id = get_uuid()
    tax_declaration4_id = get_uuid()
    tax_declaration5_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_tax_declarations"],
        [
            {
                "id": tax_declaration1_id,
                "year": "2019",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
            {
                "id": tax_declaration2_id,
                "year": "2020",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
            {
                "id": tax_declaration3_id,
                "year": "2021",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
            {
                "id": tax_declaration4_id,
                "year": "2022",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
            {
                "id": tax_declaration5_id,
                "year": "2023",
                "is_paid": True,
                "profile_id": personal_profile_id,
            },
        ],
    )

    user_financial_info_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables["hr_erp_user_financial_infos"],
        [
            {
                "id": user_financial_info_id,
                "iban": "KZ200155980950859874",
                "housing_payments_iban": "KZ200155980950859874",
                "profile_id": personal_profile_id,
            }
        ],
    )

    ids_sql = f"""select hecd.cert_document_type_id, hecd.doc_number, hecd.begin_date, hecd.end_date, dco.name_ru from HR_EMP_CERT_DOCUMENTS hecd 
         left join hr_employees emmp on emmp.id = hecd.employee_id left join DIC_CERT_ORGAN dco on dco.id = hecd.issue_organ_id where emmp.id = {emp_id} and hecd.cert_document_type_id in (1000000001, 1000000003, 1000000008) and hecd.end_date > sysdate order by hecd.cert_document_type_id"""

    ids = cursor.execute(ids_sql).fetchall()

    for personal_id in ids:
        (
            document_type_id,
            document_number,
            date_of_issue,
            date_to,
            issued_by,
        ) = personal_id

        if document_type_id == 1000000003:
            identification_card_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_identification_cards"],
                [
                    {
                        "id": identification_card_id,
                        "document_number": document_number,
                        "date_of_issue": date_of_issue,
                        "date_to": date_to,
                        "issued_by": issued_by,
                        "document_link": " ",
                        "profile_id": personal_profile_id,
                    }
                ],
            )
        if document_type_id == 1000000001:
            passport_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_passports"],
                [
                    {
                        "id": passport_id,
                        "document_number": document_number,
                        "date_of_issue": date_of_issue,
                        "date_to": date_to,
                        "issued_by": issued_by,
                        "document_link": " ",
                        "profile_id": personal_profile_id,
                    }
                ],
            )
        if document_type_id == 1000000008:
            driving_sql = f"""select 
         case when auto_category_a = 1 then 'A,' else '' end || 
           case when auto_category_b = 1 then 'B,' else '' end || 
             case when auto_category_c=1 then 'C,' else '' end ||
               case when auto_category_d=1 then 'D,' else '' end || 
                 case when auto_category_e=1 then 'E' else '' end  as auto_category
                   from hr_employees where id = {emp_id}"""
            category_res = cursor.execute(driving_sql).fetchone()
            category = category_res[0]
            category_array = []
            if category is not None:
                category = "".join([i for i in category_res])
                if category[len(category) - 1] == ",":
                    category = category[: len(category) - 1]
                category_array = category.split(",")
            driving_licence_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_driving_licenses"],
                [
                    {
                        "id": driving_licence_id,
                        "document_number": document_number,
                        "category": json.dumps(category_array),
                        "date_of_issue": date_of_issue,
                        "date_to": date_to,
                        "document_link": " ",
                        "profile_id": personal_profile_id,
                    }
                ],
            )

    special_check_sql = f"""SELECT t.ID, t.DOPSP_DATE
                             FROM hr_emp_dopsp t WHERE t.EMPLOYEE_ID = {emp_id} and IS_EXECUTED = 1 ORDER BY t.DOPSP_DATE"""
    special_checks = cursor.execute(special_check_sql).fetchall()

    for special_check in special_checks:
        (dopsp_id,
         date_of_issue) = special_check

        special_check_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_special_checks"],
            [
                {
                    "id": special_check_id,
                    "profile_id": additional_profile_id,
                    "date_of_issue": date_of_issue,
                    "special_number": dopsp_id,
                    "document_link": " ",
                    "issued_by": " "
                }
            ],
        )

    # Sport Degrees and Achievements
    sport_degrees_sql = f"""SELECT
                                 dsr.NAME_ru AS SPORT_RANK,
                                 dsk.NAME_ru AS SPORT_KIND,
                                 dsr.NAME_KZ AS sport_rank_kz,
                                 dsk.NAME_KZ AS sport_kind_kz,
								 s.CHD as assignment_date
                                 FROM HR_EMP_SPORTS s
                                 LEFT JOIN DIC_HR_SPORT_RANK dsr ON (dsr.ID = s.SPORT_RANK_ID)
                                 LEFT JOIN DIC_HR_SPORT_KIND dsk ON (dsk.ID = s.SPORT_KIND_ID)
                                 left join hr_employees emmp on emmp.id = s.EMPLOYEE_ID
                                 WHERE emmp.id = {emp_id}"""

    sport_degrees = cursor.execute(sport_degrees_sql).fetchall()
    for i in sport_degrees:
        sport_rank, sport_kind, sport_rank_kz, sport_kind_kz, assignment_date = i
        found_sport = (
            db.query(SportType)
            .filter(func.lower(SportType.name) == (sport_kind.lower()))
            .first()
        )
        if found_sport is None:
            found_sport_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_sport_types"],
                [
                    {
                        "id": found_sport_id,
                        "name": sport_kind,
                        "namekz": sport_kind_kz if sport_kind_kz else sport_kind,
                    }
                ],
            )
        else:
            found_sport_id = found_sport.id

        found_sport_degree_type = (
            db.query(SportDegreeType)
            .filter(func.lower(SportDegreeType.name) == (sport_rank.lower()))
            .first()
        )
        if found_sport_degree_type is None:
            found_sport_degree_type_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_sport_degree_types"],
                [
                    {
                        "id": found_sport_degree_type_id,
                        "name": sport_rank,
                        "namekz": sport_rank_kz,
                    }
                ],
            )
        else:
            found_sport_degree_type_id = found_sport_degree_type.id
        op.bulk_insert(
            Base.metadata.tables["hr_erp_sport_degrees"],
            [
                {
                    "id": get_uuid(),
                    "profile_id": personal_profile_id,
                    "name": f"{sport_rank} {sport_kind}",
                    "namekz": f"{sport_rank_kz} {sport_kind_kz}",
                    "assignment_date": assignment_date,
                    "document_link": " ",
                    "sport_type_id": str(found_sport_id),
                    "sport_degree_type_id": str(found_sport_degree_type_id)
                }
            ],
        )

    sport_achievements_sql = f"""SELECT
                                (SELECT tp.NAME_ru FROM dic_hr_type_competition tp WHERE tp.ID = t.COMPET_TYPE_ID) TYPE,
                                t.BEGIN_DATE,
                                t.END_DATE,
                                (SELECT rz.NAME_ru FROM dic_hr_result_partic_compet rz WHERE rz.ID = t.REZULT_ID) REZULT
                                FROM hr_emp_competition t
                                left join hr_employees hr on hr.id = t.emp_id
                                where hr.id = {emp_id}
                                UNION
                                select cv.NAME as type,cv.begin_date,cv.end_date, (SELECT rz.NAME_ru FROM dic_hr_result_partic_compet rz WHERE rz.ID = c.result_id) rezult from BSP_EMP_PARTIC_COMPET c
                                left join bsp_competitions_v cv on cv.id = c.compet_id
                                left join hr_employees hr on hr.id = c.emp_id where lower(cv.lang) = 'ru' and hr.id = {emp_id}"""

    sport_achievements = cursor.execute(sport_achievements_sql).fetchall()
    for i in sport_achievements:
        competition_type, start_date, end_date, result = i

        sport_kind = competitions[competition_type.lstrip().rstrip().upper()]

        found_sport = (
            db.query(SportType)
            .filter(func.lower(SportType.name) == (sport_kind.lower()))
            .first()
        )
        if found_sport is None:
            found_sport_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_sport_types"],
                [
                    {
                        "id": found_sport_id,
                        "name": sport_kind,
                        "namekz": " ",
                    }
                ],
            )
        else:
            found_sport_id = found_sport.id

        op.bulk_insert(
            Base.metadata.tables["hr_erp_sport_achievements"],
            [
                {
                    "id": get_uuid(),
                    "profile_id": personal_profile_id,
                    "name": result,
                    "namekz": result,
                    "assignment_date": end_date,
                    "document_link": " ",
                    "sport_type_id": str(found_sport_id),
                }
            ],
        )

    # Education Profile
    education_sql = f"""SELECT
                            'CE' AS EDU_TYPE,
                            ce.START_DATE,
                            ce.FINISH_DATE,
                            del.name_ru,
                            del.NAME_KZ,
                            (ce.INSTITUTION_ru) AS INSTITUTION,
                            (ce.INSTITUTION_KZ) as INSTITUTION_kz,
                            ce.SPECIALITY_RU,
                            ce.SPECIALITY_KZ
                            FROM HR_EMP_CIVIL_EDUCATION ce
                            LEFT JOIN DIC_HR_EDUCATION_FORM def ON (def.ID = ce.EDUCATION_FORM_ID)
                            LEFT JOIN DIC_HR_EDUCATION_LEVEL del ON (del.ID = ce.EDUCATION_LEVEL_ID)
                            left join hr_employees emmp on emmp.id = ce.employee_id
                            WHERE del.CODE IN ('003', '004', '005') AND def.CODE IN ('001') AND emmp.ID = {emp_id} 
                            UNION
                            SELECT
                            'ME',
                            me.START_DATE,
                            me.FINISH_DATE,
                            (del.name_ru),
                            (del.NAME_KZ),
                            dmi.NAME_ru,
                            dmi.NAME_KZ,
                            dms.NAME_RU,
                            dms.NAME_KZ
                            FROM HR_EMP_MILITARY_EDUCATION me
                            LEFT JOIN DIC_HR_MILITARY_INSTITUTION dmi ON (dmi.ID = me.MILITARY_INSTITUTION_ID)
                            LEFT JOIN DIC_HR_MILITARY_SPECIALITY dms ON (dmi.ID = me.MILITARY_SPECIALITY_ID)
                            LEFT JOIN DIC_HR_EDUCATION_FORM def ON (def.ID = me.EDUCATION_FORM_ID)
                            LEFT JOIN DIC_HR_EDUCATION_LEVEL del ON (del.ID = me.EDUCATION_LEVEL_ID)
                            left join hr_employees emmp on emmp.id = me.employee_id
                            WHERE del.CODE IN ('003', '004', '005') AND def.CODE IN ('001') AND emmp.ID = {emp_id} 
                            ORDER BY START_DATE DESC"""

    # TODO: Очное неочное 

    educations = cursor.execute(education_sql).fetchall()

    for education in educations:
        (
            edu_type,
            start_date,
            end_date,
            nameRU,
            nameKZ,
            institutionRU,
            institutionKZ,
            specialtyRU,
            specialtyKZ
        ) = education
        institution = (
            db.query(Institution).filter(Institution.name == institutionRU).first()
        )
        if institution is None:
            institution_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_institutions"],
                [
                    {
                        "id": institution_id,
                        "name": institutionRU,
                        "namekz": institutionKZ,
                    }
                ],
            )
        else:
            institution_id = institution.id

        inst_degree_type = (
            db.query(InstitutionDegreeType).filter(func.to_char(InstitutionDegreeType.name) == func.to_char(nameRU)).first()
        )
        if inst_degree_type is None:
            inst_degree_type_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_inst_degree_types"],
                [
                    {
                        "id": inst_degree_type_id,
                        "name": nameRU,
                        "namekz": nameKZ,
                    }
                ],
            )
        else:
            inst_degree_type_id = inst_degree_type.id

        if specialtyRU is None:
            if edu_type == 'ME':
                is_military_school = True
            else:
                is_military_school = False

            education_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_educations"],
                [
                    {
                        "id": education_id,
                        "profile_id": educational_profile_id,
                        "institution_id": str(institution_id),
                        "degree_id": inst_degree_type_id,
                        "specialty_id": " ",
                        "is_military_school": is_military_school,
                        "start_date": start_date,
                        "end_date": end_date,
                        "document_link": " ",
                        "educational_profile_id": educational_profile_id
                    }
                ],
            )
            continue

        specialty = (
            db.query(Specialty).filter(func.to_char(Specialty.name) == func.to_char(specialtyRU)).first()
        )
        if specialty is None:
            specialty_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_specialties"],
                [
                    {
                        "id": specialty_id,
                        "name": specialtyRU,
                        "namekz": specialtyKZ
                    }
                ],
            )
        else:
            specialty_id = specialty.id

        if edu_type == 'ME':
            is_military_school = True
        else:
            is_military_school = False

        education_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_educations"],
            [
                {
                    "id": education_id,
                    "profile_id": educational_profile_id,
                    "institution_id": str(institution_id),
                    "degree_id": inst_degree_type_id,
                    "specialty_id": specialty_id,
                    "is_military_school": is_military_school,
                    "start_date": start_date,
                    "end_date": end_date,
                    "document_link": " ",
                    "educational_profile_id": educational_profile_id
                }
            ],
        )

    courses_sql = f"""SELECT
                            c.BEGIN_DATE,
                            c.END_DATE,
                            NVL((dmi.NAME_ru), (c.ORGANISATION_ru)) AS ORGANIZATION,
                            NVL((dmi.NAME_KZ), (c.ORGANISATION_KZ)) as ORGANIZATION_KZ,
                            (c.COURSE_NAME_ru) AS COURSE_NAME,
                            (c.COURSE_NAME_KZ) AS COURSE_NAME_KZ
                            FROM HR_EMP_ADD_COURSES c
                            LEFT JOIN DIC_HR_MILITARY_INSTITUTION dmi ON (dmi.ID = c.MILITARY_INSTITUTION_ID)
                            LEFT JOIN DIC_HR_ADD_COURSE_TYPE dct ON (dct.ID = c.COURSES_TYPE_ID)
                            LEFT JOIN HR_EMPLOYEES emmp on c.EMPLOYEE_ID = emmp.ID
                            WHERE emmp.ID = {emp_id}
                            ORDER BY BEGIN_DATE"""

    courses = cursor.execute(courses_sql).fetchall()

    for course in courses:
        course_id = get_uuid()
        (
            start_date,
            end_date,
            organizationRU,
            organizationKZ,
            course_nameRU,
            course_nameKZ,
        ) = course
        if (
            organizationRU is None
            or organizationKZ is None
            or course_nameRU is None
            or course_nameKZ is None
        ):
            continue
        provider = (
            db.query(CourseProvider)
            .filter(func.lower(CourseProvider.name) == organizationRU.lower())
            .first()
        )
        if provider is None:
            course_provider_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_course_providers"],
                [
                    {
                        "id": course_provider_id,
                        "name": organizationRU,
                        "namekz": organizationKZ,
                    }
                ],
            )
        else:
            course_provider_id = provider.id
        op.bulk_insert(
            Base.metadata.tables["hr_erp_courses"],
            [
                {
                    "id": course_id,
                    "profile_id": educational_profile_id,
                    "course_provider_id": str(course_provider_id),
                    "name": course_nameRU,
                    "namekz": course_nameKZ,
                    "start_date": start_date,
                    "end_date": end_date,
                    "document_link": " ",
                    "educational_profile_id": educational_profile_id
                }
            ],
        )

    # # Language Proficiencies
    language_proficiencies_sql = f"""SELECT
                                 (dl.NAME_ru) AS LANG_NAME,
                                 (dl.NAME_KZ) as lang_name_kz,
                                 dlk.CODE AS LANG_LEVEL
                                 FROM HR_EMP_LANGUAGES l
                                 LEFT JOIN DIC_HR_LANGUAGES dl ON (dl.ID = l.LANGUAGE_ID)
                                 LEFT JOIN DIC_HR_LANGUAGE_LEVEL_KNOWS dlk ON (dlk.ID = l.LEVEL_KNOWS_ID)
                                 LEFT JOIN HR_EMPLOYEES emmp on emmp.id = l.employee_id
                                 where emmp.id = {emp_id}"""

    languages = cursor.execute(language_proficiencies_sql).fetchall()

    for lang in languages:
        (lang_name, lang_name_kz, lang_level) = lang
        found_lang = (
            db.query(Language)
            .filter(func.lower(Language.name).contains(lang_name.lower()))
            .first()
        )
        if found_lang is None:
            found_lang = Language(
                id=get_uuid(),
                name=lang_name,
                nameKZ=lang_name_kz,
            )
            db.add(found_lang)



        language_proficiency_id = get_uuid()
        proficiency_in_lang = LanguageProficiency(
            id=language_proficiency_id,
            profile_id=educational_profile_id,
            language_id=str(found_lang.id),
            level=lang_level_dic[lang_level],
            document_link='',
            educational_profile_id=educational_profile_id
        )
        db.add(proficiency_in_lang)

    # Academic Degrees

    academic_degree_sql = f"""SELECT ad.GIVE_DATE, dsf.NAME_RU as science_name, dsf.NAME_KZ as science_namekz,
                       dad.NAME_RU as degree_name, dad.NAME_KZ as degree_namekz
                       FROM hr_emp_academic_degrees ad
                       JOIN DIC_HR_ACADEMIC_DEGREE dad ON ad.academic_degree_id = dad.id
                       JOIN DIC_HR_SCIENTIFIC_FIELD dsf ON ad.scientific_field_id = dsf.id
                       LEFT JOIN hr_employees e on ad.EMPLOYEE_ID = e.ID
                       WHERE e.ID = {emp_id}"""
    academic_degrees = cursor.execute(academic_degree_sql).fetchall()

    for academic_degree in academic_degrees:
        (assignment_date,
         science_name,
         science_nameKZ,
         degree_name,
         degree_nameKZ) = academic_degree

        academic_degree_degree = (db.query(AcademicDegreeDegree)
                                  .filter(func.to_char(func.lower(AcademicDegreeDegree.name)) == func.to_char(degree_name.lower()))
                                  .first())
        if academic_degree_degree is None:
            degree_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["dic_hr_erp_academic_degree_degrees"],
                [
                    {
                        "id": degree_id,
                        "name": degree_name,
                        "namekz": degree_nameKZ,
                    }
                ],
            )
        else:
            degree_id = academic_degree_degree.id

        science = (db.query(Science)
                   .filter(func.to_char(func.lower(Science.name)) == func.to_char(science_name.lower()))
                   .first())
        if science is None:
            science_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_sciences"],
                [
                    {
                        "id": science_id,
                        "name": science_name,
                        "namekz": science_nameKZ,
                    }
                ],
            )
        else:
            science_id = science.id

        academic_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_academic_degrees"],
            [
                {
                    "id": academic_id,
                    "profile_id": educational_profile_id,
                    "assignment_date": assignment_date,
                    "science_id": science_id,
                    "degree_id": degree_id,
                    "document_link": " ",
                    "educational_profile_id": educational_profile_id
                }
            ],
        )

    # Academic Title

    academic_title_sql = f"""SELECT e.AS_DATE, acs.NAME_RU as title_name, acs.NAME_KZ as title_namekz
                       FROM hr_employees e
                       JOIN dic_hr_academic_status acs on e.as_academic_status = acs.ID
                       WHERE e.ID = {emp_id}"""
    academic_titles = cursor.execute(academic_title_sql).fetchall()

    for academic_title in academic_titles:
        (assignment_date,
         tilte_degree_name,
         tilte_degree_nameKZ) = academic_title

        academic_title_degree = (db.query(AcademicTitleDegree)
                                  .filter(func.to_char(func.lower(AcademicTitleDegree.name)) == func.to_char(tilte_degree_name.lower()))
                                  .first())
        if academic_title_degree is None:
            title_degree_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_academic_title_degrees"],
                [
                    {
                        "id": title_degree_id,
                        "name": tilte_degree_name,
                        "namekz": tilte_degree_nameKZ,
                    }
                ],
            )
        else:
            title_degree_id = academic_title_degree.id

        academic_title_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_academic_titles"],
            [
                {
                    "id": academic_title_id,
                    "profile_id": educational_profile_id,
                    "assignment_date": assignment_date,
                    "degree_id": title_degree_id,
                    "document_link": " ",
                    "educational_profile_id": educational_profile_id
                }
            ],
        )

    # Vehicles
    vehicles_sql = f"""select ((br.NAME_RU) || ' ' || t.TRANSPORT_MODEL) as nameRU, ((br.NAME_KZ)|| ' ' || t.TRANSPORT_MODEL) as nameKZ, NVL(ISSUE_YEAR, 1970), TRANSPORT_NUMBER from HR_EMP_TRANSPORTS t
    left join DIC_TRANSPORT_BRAND br on br.id = t.TRANSPORT_BRAND_ID
    left join hr_employees emp on t.EMPLOYEE_ID = emp.ID
    where emp.ID = {emp_id}"""

    vehicles = cursor.execute(vehicles_sql).fetchall()

    for vehicle in vehicles:
        (nameRU, nameKZ, issue_date, vehicle_number) = vehicle
        issue_date = datetime(year=issue_date, month=1, day=1)
        vehicle_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_user_vehicles"],
            [
                {
                    "id": vehicle_id,
                    "profile_id": additional_profile_id,
                    "vin_code": "JN1WNYD21U0000001",
                    "date_from": issue_date,
                    "number": vehicle_number,
                    "name": nameRU,
                    "namekz": nameKZ,
                    "document_link": " ",
                }
            ],
        )

    # Family Profile
    family_sql = f"""select (rs.name_ru), (rs.name_kz), r.surname,r.firstname, r.patronymic, r.iin, r.BIRTHDATE, r.DEADDATE,
       (dc.NAME_ru)|| ' '||lower(te1.NAME_ru)||' '||(r.BIRTHPLACE_TE1_ru)||' '||lower(te2.NAME_ru)||' '||(r.BIRTHPLACE_TE2_RU)||' '||lower(dst.NAME_ru)||' '||(r.BIRTHPLACE_SETTLEMENT_ru) as birthplace,
       ADDRESS_RU,
       workplace_ru from HR_EMP_RELATIVES r
left join hr_employees emp on emp.id = r.employee_id
LEFT JOIN DIC_COUNTRY dc ON (dc.ID = r.CITIZENSHIP_ID)
LEFT JOIN DIC_TE1_TYPE te1 ON (te1.ID = r.BIRTHPLACE_TE1_TYPE_ID)
LEFT JOIN DIC_TE2_TYPE te2 ON (te2.ID = r.BIRTHPLACE_TE2_TYPE_ID)
LEFT JOIN DIC_SETTLEMENT_TYPE dst ON (dst.ID = r.BIRTHPLACE_SETTLEMENT_TYPE_ID)
left join DIC_HR_RELATIVE_STATUS rs on rs.id = r.relative_status_id
where emp.ID = {emp_id}"""

    families = cursor.execute(family_sql).fetchall()

    for family_member in families:
        (
            relative_status,
            relative_status_kz,
            surname,
            firstname,
            patronymic,
            iin,
            birthdate,
            deathdate,
            birthplace,
            address,
            workplace,
        ) = family_member

        if birthplace is not None:
            birthplace = " ".join(birthplace.split(" "))
        if address is not None:
            address = " ".join(address.split(" "))
        if workplace is not None:
            workplace = " ".join(workplace.split(" "))

        relation = (
            db.query(FamilyRelation)
            .filter(func.lower(FamilyRelation.name) == relative_status.lower())
            .first()
        )
        if relation is None:
            relation = FamilyRelation(
                id=get_uuid(), name=relative_status, nameKZ=relative_status_kz
            )
            db.add(relation)
        family_member_id = get_uuid()
        relation_id = relation.id
        db.add(
            Family(
                id=family_member_id,
                profile_id=family_profile_id,
                first_name=firstname,
                last_name=surname,
                father_name=patronymic,
                birthday=birthdate,
                death_day=deathdate,
                birthplace_text=birthplace if birthplace is not None else "",
                address=address if address is not None else "",
                workplace=workplace if workplace is not None else "",
                relation_id=relation_id,
                IIN=iin
            )
        )
    # Abroad travels
    abroad_travels_sql = f"""SELECT ea.BEGIN_DATE, ea.END_DATE,
                       ap.NAME_RU as purpose_name, ap.NAME_KZ as purpose_nameKZ,
                       dc.FULL_NAME_RU as country_name, dc.FULL_NAME_KZ as country_nameKZ
                       FROM hr_emp_abroad ea
                       JOIN dic_hr_abroad_purpose ap on ea.purpose_id = ap.ID
                       JOIN dic_country dc on ea.country_id = dc.ID
                       WHERE ea.EMPLOYEE_ID = {emp_id}
                       AND ea.IS_PERSONALLY = 1"""
    abroad_travels = cursor.execute(abroad_travels_sql).fetchall()

    for abroad_travel in abroad_travels:
        (begin_date,
         end_date,
         purpose_name,
         purpose_nameKZ,
         country_name,
         country_nameKZ) = abroad_travel

        country = (db.query(Country)
                   .filter(func.to_char(func.lower(Country.name)) == func.to_char(country_name.lower()))
                   .first())
        if country is None:
            country_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_countries"],
                [
                    {
                        "id": country_id,
                        "name": country_name,
                        "namekz": country_nameKZ,
                    }
                ],
            )
        else:
            country_id = country.id

        abroad_travel_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_abroad_travels"],
            [
                {
                    "id": abroad_travel_id,
                    "date_from": begin_date,
                    "date_to": end_date,
                    "destination_country_id": country_id,
                    "vehicle_type": 'Самолет',
                    "document_link": " ",
                    "profile_id": additional_profile_id,
                    "reason": purpose_name,
                    "reasonKZ": purpose_nameKZ if purpose_nameKZ else purpose_name
                }
            ],
        )

    family_abroad_travels_sql = f"""SELECT ea.BEGIN_DATE, ea.END_DATE,
                       ap.NAME_RU as purpose_name, ap.NAME_KZ as purpose_nameKZ,
                       dc.FULL_NAME_RU as country_name, dc.FULL_NAME_KZ as country_nameKZ,
                       r.iin
                       FROM hr_emp_abroad ea
                       JOIN hr_emp_relatives r on r.id = ea.RELATIVE_ID
                       JOIN dic_hr_abroad_purpose ap on ea.purpose_id = ap.ID
                       JOIN dic_country dc on ea.country_id = dc.ID
                       WHERE ea.EMPLOYEE_ID = {emp_id}
                       AND ea.IS_PERSONALLY = 0
                       AND r.iin is not null"""
    family_abroad_travels = cursor.execute(family_abroad_travels_sql).fetchall()

    for family_abroad_travel in family_abroad_travels:
        (begin_date,
         end_date,
         purpose_name,
         purpose_nameKZ,
         country_name,
         country_nameKZ,
         relative_iin) = family_abroad_travel

        family = db.query(Family).filter(func.to_char(Family.IIN) == func.to_char(relative_iin)).first()
        if family is None:
            continue
        else:
            family_id = family.id
        country = (db.query(Country)
                   .filter(func.to_char(func.lower(Country.name)) == func.to_char(country_name.lower()))
                   .first())
        if country is None:
            country_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_countries"],
                [
                    {
                        "id": country_id,
                        "name": country_name,
                        "namekz": country_nameKZ,
                    }
                ],
            )
        else:
            country_id = country.id

        family_abroad_travel_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_abroad_travels"],
            [
                {
                    "id": family_abroad_travel_id,
                    "date_from": begin_date,
                    "date_to": end_date,
                    "destination_country_id": country_id,
                    "vehicle_type": 'Самолет',
                    "document_link": " ",
                    "reason": purpose_name,
                    "reasonKZ": purpose_nameKZ if purpose_nameKZ else purpose_name
                }
            ],
        )
        op.bulk_insert(
            Base.metadata.tables["hr_erp_family_abroad_travels"],
            [
                {
                    "family_id": family_id,
                    "abroad_travel_id": family_abroad_travel_id,
                }
            ],
        )

    # Service Profile

    coolness_sql = f"""select 
(select name_ru from dic_hr_class_qualification dhcq where t.classiness_id = dhcq.id ) as coolness_type_name,  
(select name_kz from dic_hr_class_qualification dhcq where t.classiness_id = dhcq.id ) as coolness_type_namekz
,t.order_number as document_number, t.order_date as date_credited, 
t.order_confirmer_ru as contractor_signer_name, t.order_confirmer_kz as contractor_signer_namekz,
case 
  when t.status_id =1 then 'granted'
    when t.status_id =1 then 'confirmed'
      when t.status_id =1 then 'removed'
        else 'demoted' end as coolnessStatusEnum
    from hr_emp_class_qualification t
    where t.emp_id={emp_id}"""
    coolnesses = cursor.execute(coolness_sql).fetchall()

    for i in coolnesses:
        (
            coolness_type_name,
            coolness_type_namekz,
            document_number,
            date_credited,
            contractor_signer_name,
            contractor_signer_namekz,
            coolness_status
        ) = i

        found_coolness_type = (
            db.query(CoolnessType)
            .filter(func.lower(CoolnessType.name) == coolness_type_name.lower())
            .first()
        )
        if found_coolness_type is None:
            found_coolness_type_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_coolness_types"],
                [
                    {
                        "id": found_coolness_type_id,
                        "name": coolness_type_name,
                        "namekz": coolness_type_namekz,
                        "coolness_order": 1
                    }
                ]
            )
        else:
            found_coolness_type_id = found_coolness_type.id
        
        coolness_id = get_uuid()
        new_coolness = Coolness(
            id=coolness_id,
            type_id=str(found_coolness_type_id),
            user_id=id,
            coolness_status=coolness_status
        )
        db.add(new_coolness)
        new_coolness_history = CoolnessHistory(
            document_number=document_number,
            date_credited=date_credited,
            # contractor_signer_name=contractor_signer_name,
            # contractor_signer_namekz=contractor_signer_namekz,
            user_id=id
        )
        db.add(new_coolness_history)


    oath_id = get_uuid()
    op.bulk_insert(
        Base.metadata.tables["hr_erp_user_oaths"],
        [
            {
                "id": oath_id,
                "user_id": id,
                "military_unit": " ",
                "oath_date": datetime.now()
            }
        ]
    )


    badge_sql = f"""SELECT
                    (SELECT dhat.NAME_ru FROM dic_hr_award_type dhat WHERE dhat.ID = t.AWARD_NAME_ID) AWARD_NAME,
                    (SELECT dhat.NAME_kz FROM dic_hr_award_type dhat WHERE dhat.ID = t.AWARD_NAME_ID) AWARD_NAME_KZ,
                    t.DOC_NUMBER,
                    t.DOC_DATE
                    FROM hr_emp_awards t where t.employee_id = {emp_id} order by t.DOC_DATE"""

    badges = cursor.execute(badge_sql).fetchall()

    for i in badges:
        (
            award_name,
            award_nameKZ,
            doc_number,
            doc_date,
        ) = i
        found_badge_type = (
            db.query(BadgeType)
            .filter(func.lower(BadgeType.name) == award_name.lower())
            .first()
        )
        if found_badge_type is None:
            found_badge_type_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_badge_types"],
                [
                    {
                        "id": found_badge_type_id,
                        "name": award_name,
                        "namekz": award_nameKZ,
                        "url": "https://10.15.3.180/s3/static/award-placeholder.png",
                        "badge_order": 1
                    }
                ],
            )
        else:
            found_badge_type_id = found_badge_type.id
        badge_id = get_uuid()
        new_badge = Badge(
            id=badge_id,
            user_id=id,
            type_id=str(found_badge_type_id),
        )
        db.add(new_badge)
        new_badge_history = BadgeHistory(
            date_from=doc_date,
            date_to=None,
            user_id=id,
            date_credited=doc_date,
            document_number=doc_number,
            badge_id=str(badge_id),
        )
        db.add(new_badge_history)

    badge1_sql = f"""SELECT
                    (SELECT it.NAME_ru FROM dic_hr_incentive_type it WHERE it.ID = t.incentive_type_id) incentive_name,
                    (SELECT it.NAME_kz FROM dic_hr_incentive_type it WHERE it.ID = t.incentive_type_id) incentive_name_kz,
                    t.reason_ru,
                    t.reason_kz,
                    t.order_number,
                    t.order_date
                    FROM hr_emp_incentive t where t.employee_id = {emp_id} order by t.order_date"""

    badges1 = cursor.execute(badge1_sql).fetchall()

    for i in badges1:
        (
            incentive_name,
            incentive_nameKZ,
            reason_ru,
            reason_kz,	
            doc_number1,
            doc_date1,
        ) = i
        found_badge_type1 = (
            db.query(BadgeType)
            .filter(func.lower(BadgeType.name) == incentive_name.lower())
            .first()
        )
        if found_badge_type1 is None:
            awrd_name = None
            awrd_nameKZ = None
            if incentive_name is not None and reason_ru is not None:
                awrd_name = incentive_name+' '+reason_ru 
            elif incentive_name is not None and reason_ru is None: 
                awrd_name = incentive_name
            elif incentive_name is None and reason_ru is not None: 
                awrd_name = reason_ru

            if incentive_nameKZ is not None and reason_kz is not None:
                awrd_nameKZ = incentive_nameKZ+' '+reason_kz 
            elif incentive_name is not None and reason_kz is None: 
                awrd_nameKZ = incentive_nameKZ
            elif incentive_name is None and reason_kz is not None: 
                awrd_nameKZ = reason_kz 
            found_badge_type_id1 = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_badge_types"],
                [
                    {
                        "id": found_badge_type_id1,
                        "name": awrd_name,
                        "namekz": awrd_nameKZ,
                        "url": "https://10.15.3.180/s3/static/award-placeholder.png",
                        "badge_order": 1
                    }
                ],
            )
        else:
            found_badge_type_id1 = found_badge_type1.id
        badge_id1 = get_uuid()
        new_badge1 = Badge(
            id=badge_id1,
            user_id=id,
            type_id=str(found_badge_type_id1),
        )
        db.add(new_badge1)
        new_badge1_history = BadgeHistory(
            date_from=doc_date1,
            date_to=None,
            user_id=id,
            date_credited=doc_date1,
            document_number=doc_number1,
            badge_id=str(badge_id1),
        )
        db.add(new_badge1_history)

    penalty_sql = f"""SELECT
                (SELECT pt.NAME_ru FROM dic_hr_penalty_type pt WHERE pt.ID = t.PENALTY_TYPE_ID) PENALTY_TYPE, 
                (SELECT pt.NAME_kz FROM dic_hr_penalty_type pt WHERE pt.ID = t.PENALTY_TYPE_ID) PENALTY_TYPE_KZ, 
                t.ORDER_BEGIN_NUMBER, 
                t.ORDER_BEGIN_DATE, 
                t.ORDER_END_NUMBER, 
                t.ORDER_END_DATE
                FROM hr_emp_penalty t 
                WHERE t.EMPLOYEE_ID = {emp_id} order by t.ORDER_BEGIN_DATE"""

    penalties = cursor.execute(penalty_sql).fetchall()

    for i in penalties:
        (
            penalty_name,
            penalty_nameKZ,
            pen_number,
            date_from,
            pen_end_number,
            date_to,
        ) = i
        found_penalty_type = (
            db.query(PenaltyType)
            .filter(func.lower(PenaltyType.name) == penalty_name.lower())
            .first()
        )
        if found_penalty_type is None:
            found_penalty_type_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_penalty_types"],
                [
                    {
                        "id": found_penalty_type_id,
                        "name": penalty_name,
                        "namekz": penalty_nameKZ,
                    }
                ],
            )
        else:
            found_penalty_type_id = found_penalty_type.id
        new_penalty = Penalty(
            id=get_uuid(),
            type_id=str(found_penalty_type_id),
            user_id=id,
        )
        db.add(new_penalty)
        if date_to is not None:
            date_to = date_to
        elif date_from is None:
            date_to = None
        else:
            date_to = date_from + timedelta(weeks=25)
        new_penalty_history = PenaltyHistory(
            id=get_uuid(),
            date_from=date_from,
            document_number=pen_number,
            date_credited=date_from,
            date_to=date_to,
            penalty_id=str(new_penalty.id),
            user_id=id
        )
        db.add(new_penalty_history)

    attestation_sql = f"""SELECT
                t.ATTESTATION_DATE,
                t.CONCLUSION_KZ,
                t.CONCLUSION_RU
                FROM hr_emp_attestation t where t.employee_id = {emp_id} order by t.attestation_date"""

    attestations = cursor.execute(attestation_sql).fetchall()

    for i in attestations:
        (date_from, conclusionKZ, conclusion) = i
        new_attestation = Attestation(id=get_uuid(), user_id=id)
        db.add(new_attestation)
        new_history = AttestationHistory(
            id=get_uuid(),
            date_from=date_from,
            date_to=date_from + timedelta(weeks=156),
            date_credited=date_from,
            attestation_id=str(new_attestation.id),
            attestation_status=conclusion,
            user_id=id
        )
        db.add(new_history)

    emergency_service_sql = f"""SELECT 
t.BEGIN_DATE, 
t.END_DATE, 
case
           when nvl(t.division_id, 0) = 0 and nvl(t.post_id, 0) = 0 and
                nvl(t.instead_of_post_id, 0) = 0 and
                nvl(t.dic_post_instd_id, 0) = 0 and
                nvl(t.order_begin_id, 0) = 0 and t.is_readonly = 0 then
            t.post_ru
           when nvl(t.instead_of_post_id, 0) <> 0 then
            (select dhp.name_ru
               from dic_hr_postname dhp
              where dhp.id = t.dic_post_instd_id)
           when nvl(t.post_id, 0) <> 0 then
            (select dhp.name_ru
               from hr_position_structure hps
               join dic_hr_postname dhp
                 on dhp.id = hps.position_id
              where hps.id = t.post_id)
           when nvl(t.dic_post_instd_id, 0) <> 0 then
            (select dhp.name_ru
               from dic_hr_postname dhp
              where dhp.id = t.dic_post_instd_id)
           when exists (select 1
                   from dic_hr_order_type dhot
                  where dhot.id = t.order_begin_type_id
                    and dhot.code in ('002', '006', '008')) then
            (select yn.name_ru
               from dic_adm_yes_no yn
              where yn.code = 'AT_COMMAND')
           else
            null
         end as position,
         
case
           when nvl(t.division_id, 0) = 0 and nvl(t.post_id, 0) = 0 and
                nvl(t.instead_of_post_id, 0) = 0 and
                nvl(t.dic_post_instd_id, 0) = 0 and
                nvl(t.order_begin_id, 0) = 0 and t.is_readonly = 0 then
            t.post_ru
           when nvl(t.instead_of_post_id, 0) <> 0 then
            (select dhp.name_kz
               from dic_hr_postname dhp
              where dhp.id = t.dic_post_instd_id)
           when nvl(t.post_id, 0) <> 0 then
            (select dhp.name_kz
               from hr_position_structure hps
               join dic_hr_postname dhp
                 on dhp.id = hps.position_id
              where hps.id = t.post_id)
           when nvl(t.dic_post_instd_id, 0) <> 0 then
            (select dhp.name_kz
               from dic_hr_postname dhp
              where dhp.id = t.dic_post_instd_id)
           when exists (select 1
                   from dic_hr_order_type dhot
                  where dhot.id = t.order_begin_type_id
                    and dhot.code in ('002', '006', '008')) then
            (select yn.name_kz
               from dic_adm_yes_no yn
              where yn.code = 'AT_COMMAND')
           else
            null
         end as position_kz,          
t.INSTEAD_OF_POST_ru INSTEAD_POSITION, 
t.INSTEAD_OF_POST_kz INSTEAD_POSITION_KZ, 
(select nvl(sum(pct_value),0) from hr_emp_soprecord_pcts where soprecord_id =t.id) as percent,
1.5 as koef,
case when 
 nvl(t.division_id, 0) = 0 AND nvl(t.post_id, 0) = 0 AND nvl(t.instead_of_post_id, 0) = 0 then t.division_ru 
 else
(select full_name_ru from HR_DIVISION_STRUCTURE str where t.division_id = str.id) 
 end as div_full_name, 
t.ORDER_BEGIN_NUMBER, 
t.ORDER_BEGIN_DATE, 
t.ORDER_BEGIN_CONFIRMER_ru BEGIN_CONFIRMER
FROM hr_emp_soprecords_v t WHERE t.EMPLOYEE_ID = {emp_id} order by t.begin_date, t.id
"""

    emergency_services = cursor.execute(emergency_service_sql).fetchall()

    for i in emergency_services:
        (
            begin_date,
            end_date,
            position_name,
            position_nameKZ,
			instead_position_name,
			instead_position_nameKZ,
            percent,
            coeff,
            division_name,
            doc_number,
            doc_date,
            confirmer,
        ) = i
        found_position = (
            db.query(Position)
            .filter(func.lower(Position.name) == position_name)
            .first()
        )

        if instead_position_name is not None:
             found_instead_position = (
                  db.query(Position)
                  .filter(func.lower(Position.name) == instead_position_name)
                  .first()
             )

        new_history = EmergencyServiceHistory(
            id=get_uuid(),
            date_from=begin_date,
            date_to=end_date,
            user_id=id,
            document_number=doc_number,
            date_credited=begin_date,
            coefficient=coeff,
            percentage=percent,
            staff_division_name=division_name,
            staff_division_nameKZ=division_name,
            contractor_signer_name=confirmer,
            contractor_signer_nameKZ=confirmer,
        )
        if instead_position_name is not None:
            if found_position is None:
                new_history.actual_position_name = position_name
                new_history.actual_position_nameKZ = position_nameKZ
            else:
                new_history.actual_position_id = found_position.id
            if found_instead_position is None:
                new_history.position_name = instead_position_name
                new_history.position_nameKZ = instead_position_nameKZ
            else:
                new_history.position_id = found_instead_position.id
        else:
            if found_position is None:
                new_history.position_name = position_name
                new_history.position_nameKZ = position_nameKZ
            else:
                new_history.position_id = found_position.id
				
        db.add(new_history)


    rank_sql = f"""SELECT
                   t.ORDER_DATE,
                   d.NAME_RU,
                   d.NAME_KZ,
                   t.ORDER_CONFIRMER_RU,
                   t.ORDER_NUMBER
                   FROM hr_emp_ranks t
                   JOIN dic_hr_rank d ON t.rank_id = d.id
                   where t.employee_id = {emp_id} order by t.ORDER_DATE"""


    rank_histories = cursor.execute(rank_sql).fetchall()

    for i in rank_histories:
        (
            order_date,
            rank_name,
            rank_nameKZ,
            order_confirmer_ru,
            order_number
        ) = i
        found_rank = (
            db.query(Rank)
            .filter(func.lower(Rank.name) == rank_name)
            .first()
        )
        new_history = RankHistory(
            id=str(uuid.uuid4()),
            date_from=order_date,
            document_number=order_number,
            rank_assigned_by=order_confirmer_ru,
            user_id=id
        )
        if found_rank is None:
            new_history.rank_name = rank_name
            new_history.rank_nameKZ = rank_nameKZ
        else:
            new_history.rank_id = found_rank.id
        db.add(new_history)

    # Work Experience
    work_experience_sql = f"""
    select BEGIN_DATE, END_DATE, ORGANIZATION_RU, POSITION_RU, IS_USED from HR_EMP_WORKRECORDS
    WHERE EMPLOYEE_ID = {emp_id}
    """
    
    work_experiences = cursor.execute(work_experience_sql).fetchall()
    
    for i in work_experiences:
        (
            date_from,
            date_to,
            org_name,
            pos_name,
            is_credited,
        ) = i
        
        new_work_experience = WorkExperienceHistory(
            date_from=date_from,
            date_to=date_to,
            user_id=id,
            name_of_organization=org_name,
            position_work_experience=pos_name,
            is_credited=is_credited,
        )
        
        db.add(new_work_experience)

    secondments_sql = f"""select t.begin_date,t.end_date, t.div_name_ru division, t.div_name_kz
                from HR_EMP_ATTACHMENTS_V t where t.employee_id = {emp_id}"""
    
    secondments = cursor.execute(secondments_sql).fetchall()
    for i in secondments:
        (
            date_from,
            date_to,
            div_name,
            div_nameKZ,
        ) = i
        
        new_secondment = Secondment(
            id=get_uuid(),
            name=div_name,
            nameKZ=div_nameKZ,
            staff_division_id=None,
            state_body_id=None,
            user_id=id,
        )
        db.add(new_secondment)
        new_secondment_history = SecondmentHistory(
            id=get_uuid(),
            date_from=date_from,
            date_to=date_to,
            secondment_id=new_secondment.id,
            user_id=id,
            staff_division_name=div_name,
            staff_division_nameKZ=div_nameKZ,
            document_number=''
        )
        db.add(new_secondment_history)

    # Service IDS
    service_id_sql = f"""select oc_number, oc_begin_date, oc_end_date, token from HR_EMPLOYEES
    where ID = {emp_id}"""
    
    service_ids = cursor.execute(service_id_sql).fetchall()
    for i in service_ids:
        (
            number,
            date_from,
            date_to,
            token
        ) = i
        ServiceID(
            id=get_uuid(),
            number=number,
            date_to=date_to,
            token_status=ServiceIDStatus.RECEIVED,
            id_status=ServiceIDStatus.RECEIVED,
            user_id=id
        )
    # Leaves
    leave_sql = f"""select l.leave_type_id, l.begin_date, l.end_date, l.order_number, l.order_date, l.order_confirmer_ru, l.order_confirmer_kz,t.name_ru, t.name_kz
from HR_EMP_LEAVES l
left join dic_hr_leave_type t on t.id = l.leave_type_id 
where l.employee_id = {emp_id}

union
select 0,rl.begin_date,rl.end_date,rl.report_order_number,rl.report_date, rl.report_order_confirmer_ru,rl.report_order_confirmer_kz, 'Ежегодный отпуск', 'Жыл сайынғы демалыс' from HR_EMP_REGLEAVES rl
where rl.employee_id = {emp_id}
"""
    leaves = cursor.execute(leave_sql).fetchall()
    
    for i in leaves:
        (
            leave_type_id,
            date_from,
            date_to,
            order_number,
            order_date,
            confirmer,
            confirmerKZ,
            nameRU,
            nameKZ,
        ) = i 
        type = db.query(StatusType).filter(
            func.to_char(func.lower(StatusType.name)) == nameRU.lower()).first()
        if type is None:
            type_id = get_uuid()
            op.bulk_insert(
                Base.metadata.tables["hr_erp_status_types"],
                [{
                    "id": type_id,
                    'name': nameRU,
                    'namekz': nameKZ,
                    'form': 'Форма 1'
                }]
            )
        else:
            type_id = type.id
        new_status = Status(
            id=get_uuid(),
            user_id=id,
            type_id=type_id
        )
        db.add(new_status)
        new_status_history = StatusHistory(
            id=get_uuid(),
            status_name=nameRU,
            status_nameKZ=nameKZ,
            status_id=new_status.id,
            document_number=order_number,
            date_from=date_from,
            date_to=date_to,
            user_id=id
        )
        db.add(new_status_history)

    # Contracts
    contract_sql = f"""select * from (SELECT
                (SELECT dayn.NAME_ru FROM dic_adm_yes_no dayn WHERE dayn.YES_NO_TYPE = 'D' AND dayn.TRUTH_VALUE = t.UNDER_LIMIT_AGE) UNDER_LIMIT_NAME, 
                (SELECT dayn.NAME_ru FROM dic_adm_yes_no dayn WHERE dayn.YES_NO_TYPE = 'D' AND dayn.TRUTH_VALUE = t.OVER_LIMIT_AGE) OVER_LIMIT_NAME, 
                t.UNDER_LIMIT_AGE, 
                t.OVER_LIMIT_AGE, 
                t.BEGIN_DATE, 
                t.END_DATE, 
                floor(months_between(t.end_date,t.begin_date)/12) as years,
                t.ORDER_NUMBER, 
                t.ORDER_DATE, 
                t.ORDER_CONFIRMER_KZ, 
                t.ORDER_CONFIRMER_RU
                 FROM hr_emp_contracts t where t.employee_id = {emp_id})where years > 0
"""
    contracts = cursor.execute(contract_sql).fetchall()

    for i in contracts:
        (
            under_limit_name,
            over_limit_name,
            under_limit_age,
            over_limit_age,
            date_from,
            date_to,
            years,
            doc_number,
            doc_date,
            confirmerKZ,
            confirmer,
        ) = i

        if years == 10 and not under_limit_age:
            new_contract_type = ContractType(
                id=get_uuid(),
                name="Контракт на 10 лет",
                nameKZ="10 жылғы келісімшарт ",
                years=10,
                is_finite=True,
            )
            db.add(new_contract_type)
        elif years == 5 and not under_limit_age:
            new_contract_type = ContractType(
                id=get_uuid(),
                name="Контракт на 5 лет",
                nameKZ="5 жылғы келісімшарт",
                years=5,
                is_finite=True,
            )
            db.add(new_contract_type)
        elif years == 3 and not under_limit_age:
            new_contract_type = ContractType(
                id=get_uuid(),
                name="Контракт на 3 года",
                nameKZ="3 жылғы келісімшарт",
                years=3,
                is_finite=True,
            )
            db.add(new_contract_type) 
        elif years == 2 and not under_limit_age:
            new_contract_type = ContractType(
                id=get_uuid(),
                name="Контракт на 2 года",
                nameKZ="2 жылғы келісімшарт",
                years=2,
                is_finite=True,
            )
            db.add(new_contract_type) 
        elif years == 2 and not under_limit_age:
            new_contract_type = ContractType(
                id=get_uuid(),
                name="Контракт на 2 года",
                nameKZ="2 жылғы келісімшарт",
                years=2,
                is_finite=True,
            )
            db.add(new_contract_type) 
        elif under_limit_age:
            new_contract_type = ContractType(
                id=get_uuid(),
                name="Контракт до предельного возраста",
                nameKZ="Шетки жаска дейнги келісімшарт",
                years=0,
                is_finite=True,
            )
            db.add(new_contract_type)
        else:
            new_contract_type = ContractType(
                id=get_uuid(),
                name="Контракт на неопределенный срок",
                nameKZ="Белгісіз мерзімді келісімшарт",
                years=-1,
                is_finite=True,
            )
            db.add(new_contract_type)

        new_contract = Contract(
            id=get_uuid(),
            type_id=new_contract_type.id,
            user_id=id,
        )
        db.add(new_contract)

        new_contract_history = ContractHistory(
            id=get_uuid(),
            date_from=date_from,
            date_to=date_to,
            contract_id=new_contract.id,
            experience_years=years,
            document_number=doc_number,
            user_id=id
        )
        db.add(new_contract_history)
        
    db.flush()


def upgrade() -> None:

    conn = oracledb.connect(
        user="admin_sop", password="welcome1", dsn="10.15.3.31/SOPPROD"
    )
    cursor: Cursor = conn.cursor()

    db = Session(bind=op.get_bind())

    # with op.batch_alter_table('hr_division_structure') as batch_op:
         # batch_op.add_column(sa.Column('alias_staff_division_id', sa.VARCHAR(length=36), nullable=True))

    rank_sql = """select d.id, d.name_ru, d.name_kz, (select case when rank_order is null then 1 else rank_order end from hr_erp_ranks her where lower(her.name) = lower(d.name_ru)) as rank_order from dic_hr_rank d"""
    
    for i in cursor.execute(rank_sql).fetchall():
        (
            rank_id,
            rank_name,
            rank_nameKZ,
            rank_order
        ) = i
        new_rank_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_ranks"],
            [{
                "id": new_rank_id,
                'name': rank_name,
                'namekz': rank_nameKZ,
                'rank_order': rank_order
            }]
        )
        rank_context[rank_id] = new_rank_id

    status_type_sql = """select name_ru, name_kz from dic_hr_leave_type"""

    for i in cursor.execute(status_type_sql).fetchall():
        (
            status_type_name,
            status_type_nameKZ,
        ) = i
        new_status_type_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_status_types"],
            [{
                "id": new_status_type_id,
                'name': status_type_name,
                'namekz': status_type_nameKZ,
            }]
        )

    academic_degree_degree_sql = """select name_ru, name_kz from DIC_HR_ACADEMIC_DEGREE"""

    for i in cursor.execute(academic_degree_degree_sql).fetchall():
        (
            academic_degree_degree_name,
            academic_degree_degree_nameKZ,
        ) = i
        new_academic_degree_degree_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["dic_hr_erp_academic_degree_degrees"],
            [{
                "id": new_academic_degree_degree_id,
                'name': academic_degree_degree_name,
                'namekz': academic_degree_degree_nameKZ,
            }]
        )

    academic_title_degree_sql = """select name_ru, name_kz from dic_hr_academic_status"""

    for i in cursor.execute(academic_title_degree_sql).fetchall():
        (
            academic_title_degree_name,
            academic_title_degree_nameKZ,
        ) = i
        new_academic_title_degree_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_academic_title_degrees"],
            [{
                "id": new_academic_title_degree_id,
                'name': academic_title_degree_name,
                'namekz': academic_title_degree_name,
            }]
        )

    sport_type_sql = """select name_ru, name_kz from DIC_HR_SPORT_KIND"""

    for i in cursor.execute(sport_type_sql).fetchall():
        (
            sport_type_name,
            sport_type_nameKZ,
        ) = i
        new_sport_type_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_sport_types"],
            [{
                "id": new_sport_type_id,
                'name': sport_type_name,
                'namekz': sport_type_nameKZ,
            }]
        )

    country_sql = """select full_name_ru, full_name_kz from DIC_COUNTRY"""

    for i in cursor.execute(country_sql).fetchall():
        (
            country_name,
            country_nameKZ,
        ) = i
        new_country_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_countries"],
            [{
                "id": new_country_id,
                'name': country_name,
                'namekz': country_nameKZ,
            }]
        )


    sport_degree_type_sql = """select name_ru, name_kz from DIC_HR_SPORT_RANK"""

    for i in cursor.execute(sport_degree_type_sql).fetchall():
        (
            sport_degree_type_name,
            sport_degree_type_nameKZ,
        ) = i
        new_sport_degree_type_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_sport_degree_types"],
            [{
                "id": new_sport_degree_type_id,
                'name': sport_degree_type_name,
                'namekz': sport_degree_type_nameKZ,
            }]
        )

    housing_sql = """select name_ru, name_kz from DIC_HR_DOMICILE_KIND"""

    for i in cursor.execute(housing_sql).fetchall():
        (
            property_type_name,
            property_type_nameKZ,
        ) = i
        new_property_type_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_property_types"],
            [{
                "id": new_property_type_id,
                'name': property_type_name,
                'namekz': property_type_nameKZ,
            }]
        )

    specialty_sql = """select distinct speciality_ru, speciality_kz from HR_EMP_CIVIL_EDUCATION"""

    for i in cursor.execute(specialty_sql).fetchall():
        (
            specialty_name,
            specialty_nameKZ,
        ) = i
        new_specialty_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_specialties"],
            [{
                "id": new_specialty_id,
                'name': specialty_name,
                'namekz': specialty_nameKZ,
            }]
        )

    science_sql = """select name_ru, name_kz from DIC_HR_SCIENTIFIC_FIELD"""

    for i in cursor.execute(science_sql).fetchall():
        (
            science_name,
            science_nameKZ,
        ) = i
        new_science_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_sciences"],
            [{
                "id": new_science_id,
                'name': science_name,
                'namekz': science_nameKZ,
            }]
        )

    penalty_type_sql = """select name_ru, name_kz from dic_hr_penalty_type"""

    for i in cursor.execute(penalty_type_sql).fetchall():
        (
            penalty_type_name,
            penalty_type_nameKZ,
        ) = i
        new_penalty_type_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_penalty_types"],
            [{
                "id": new_penalty_type_id,
                'name': penalty_type_name,
                'namekz': penalty_type_nameKZ,
            }]
        )

    division_sql = """select id, case when parent_id = 0 then null else parent_id end, name_ru,name_kz
    from hr_division_structure where status = 3 order by tree_level"""

    for i in cursor.execute(division_sql).fetchall():
        (
            id,
            parent_id,
            name,
            nameKZ
        ) = i
        new_division_id = get_uuid()
        op.bulk_insert(
            Base.metadata.tables["hr_erp_staff_divisions"],
            [{
                'id': new_division_id,
                'name': name,
                'namekz': nameKZ,
                'parent_group_id': division_context.get(parent_id, None),
                'is_combat_unit': True,
                'description': json.dumps({"name": " ", "nameKZ": " "}),
                'leader_id': ''
            }]
        )
        division_context[id] = new_division_id
        division_update_sql = (f"update hr_division_structure set staff_division_id = '{new_division_id}' where id = '{id}'")
        cursor.execute(division_update_sql)

    special_group = db.query(StaffDivision).filter(StaffDivision.name == StaffDivisionEnum.SPECIAL_GROUP.value).first()
    for i in special_group.children:
        division_context[i.id] = i.id

    overall_sql = f"""select e.ID,
    e.SURNAME,
    e.FIRSTNAME,
    e.PATRONYMIC,
    e.OFFICER_NUMBER,
    e.IIN,
    dfs.name_ru,
    e.oc_number as securityId,e.oc_end_date securityId_endDate,
    (select 
                 ADDRESS_SETTLEMENT_ru || ', ' || ADDRESS_GEONIM_ru || ' ' || ADDRESS_HOUSE || ', ' || ADDRESS_FLAT as address
                 from hr_emp_addresses where employee_id = e.id and address_type_id = 1000000002 and rownum = 1) as fact_address,
    (select ADDRESS_SETTLEMENT_ru || ', ' || ADDRESS_GEONIM_ru || ' ' || ADDRESS_HOUSE || ', ' || ADDRESS_FLAT as address
                from hr_emp_addresses where employee_id = e.id and address_type_id = 1000000001 and rownum = 1) as reg_address,
    case when e.sex_id = 1000000001 then 1 else 0 end as gender,
    
    NVL(dpn.NAME_ru, sr.POST_ru) AS POST_NAME,
    sr.division_id,
    sr.ORDER_BEGIN_CONFIRMER_ru AS POST_ORDER_CONFIRMER,
--         case
--             when oc.POSITION_NAME_RU like '%аспоряж%'
--                 then (select dhrp.name_short_ru as POST_ORDER_CONFIRMER_POST from hr_position_structure hrps
--                                                                                       left join dic_hr_postname dhrp on dhrp.id = hrps.position_id
--                       where hrps.id = (select post_id from (select sop.post_id, row_number() over (order by sop.id desc)as rn from  HR_EMP_SOPRECORDS sop where employee_id = (select order_approver_id from hr_order_caption where id = sr.ORDER_BEGIN_ID) ) where rn = 2 ))
--             else oc.POSITION_NAME_ru
--             end as POST_ORDER_CONFIRMER_POST,
    sr.ORDER_BEGIN_NUMBER AS POST_ORDER_NUMBER,
    sr.ORDER_BEGIN_DATE AS POST_ORDER_DATE,
    e.BIRTHDATE,
    (dc.NAME_ru)||' '||lower(te1.NAME_ru)|| ' '||(e.BIRTH_TE1_ru)||' '||lower(te2.NAME_ru)||' '||(e.BIRTH_TE2_ru)||' '||lower(dst.NAME_ru)||' '||(e.BIRTH_SETTLEMENT_ru) as birthplace,
    case
        when e.sex_id = 1000000001 then (dn.NAME_ru)
        else (dn.f_name_ru) end AS NATIONALITY_NAME,
    concat(concat(dbg.NAME_ru,'-'), drf.name_ru) AS BLOOD_GROUP,
    e.HEIGHT,
    e.WEIGHT,
    e.SIZE_OF_HAT,
    e.CLOTHING_SIZE,
    e.SHOES_SIZE,
    e.status_id,
    vvv.rank_id
FROM HR_EMPLOYEES e
         LEFT JOIN HR_EMP_SOPRECORDS sr ON (sr.EMPLOYEE_ID = e.ID AND sr.IS_ACTIV = 1)
         LEFT JOIN HR_EMPLOYEES_EASY_V vvv on vvv.EMPLOYEE_ID = e.id
         LEFT JOIN HR_DIVISION_STRUCTURE ds ON (TO_NUMBER(ds.ID) = NVL2(sr.ID, sr.DIVISION_ID, TO_NUMBER(e.DIVISION_ID)))
         LEFT JOIN HR_POSITION_STRUCTURE ps ON (TO_NUMBER(ps.ID) = sr.POST_ID)
         LEFT JOIN DIC_HR_POSTNAME dpn ON (dpn.ID = NVL(ps.POSITION_ID, sr.DIC_POST_INSTD_ID))
         LEFT JOIN DIC_COUNTRY dc ON (dc.ID = e.BIRTH_COUNTRY_ID)
         LEFT JOIN DIC_TE1_TYPE te1 ON (te1.ID = e.BIRTH_TE1_TYPE_ID)
         LEFT JOIN DIC_TE2_TYPE te2 ON (te2.ID = e.BIRTH_TE2_TYPE_ID)
         LEFT JOIN DIC_SETTLEMENT_TYPE dst ON (dst.ID = e.BIRTH_SETTLEMENT_TYPE_ID)
         LEFT JOIN DIC_NATIONALITY dn ON (dn.ID = e.NATIONALITY_ID)
         LEFT JOIN DIC_BLOOD_GROUP dbg ON (dbg.ID = e.BLOOD_GROUP_ID)
         LEFT JOIN DIC_RHESUS_FACTOR drf ON (drf.ID = e.RHESUS_FACTOR_ID)
         LEFT JOIN HR_ORDER_CAPTION o ON (o.ID = sr.ORDER_BEGIN_ID)
         LEFT JOIN HR_EMPLOYEES_EASY_V oc ON (oc.EMPLOYEE_ID = o.ORDER_APPROVER_ID)
         left join DIC_FAMILY_STATUS dfs on dfs.id = e.family_status_id
         left join hr_emp_status hes on hes.id = e.status_id
         where hes.id in (2,3,5,7,8,9)"""

    found_position = db.query(Position).first()
    found_division = (
        db.query(StaffDivision)
        .filter(StaffDivision.name == StaffDivisionEnum.SPECIAL_GROUP.value)
        .first()
    )

    for row in cursor.execute(overall_sql).fetchall():
        (
            e_id,
            surname,
            name,
            father_name,
            officer_number,
            iin,
            family_status_name,
            service_id_number,
            service_id_end_date,
            fact_address,
            reg_address,
            gender,
            position_name,
            division_id,
            post_order_confirmer,
            post_order_number,
            post_order_date,
            birthdate,
            birth_place,
            nationality,
            blood_group,
            height,
            weight,
            hat_size,
            clothes_size,
            shoes_size,
            status_id,
            rank_id,
        ) = row
        staff_unit_id = get_uuid()
        create_user(
            cursor,
            db,
            e_id,
            surname,
            name,
            father_name,
            officer_number,
            iin,
            family_status_name,
            service_id_number,
            service_id_end_date,
            fact_address,
            reg_address,
            gender,
            position_name,
            division_id,
            post_order_confirmer,
            post_order_number,
            post_order_date,
            birthdate,
            birth_place,
            nationality,
            blood_group,
            height,
            weight,
            hat_size,
            clothes_size,
            shoes_size,
            found_position.id if found_position else None,
            found_division.id,
            staff_unit_id,
            staff_unit_id,
            status_id,
            rank_id,
        )

    recommender_sql = f"""select e.ID,
                      e.iin,
                      e.RECOMMENDANT_ID,
                      e.RECOMMENDANT FROM HR_EMPLOYEES e
                      where e.RECOMMENDANT_ID is not null"""

    for row in cursor.execute(recommender_sql).fetchall():
        (
            e_id,
            user_iin,
            recommendant_id,
            recommendant_name
        ) = row
        user = db.query(User).filter(User.iin == str(user_iin).lstrip().rstrip()).first()
        if user is None:
            continue
        recommender_iin_sql = f"""SELECT e.iin
                          FROM HR_EMPLOYEES e
                          where e.ID = {recommendant_id}"""
        (recommender_iin) = cursor.execute(recommender_iin_sql).fetchone()
        recommender = db.query(User).filter(User.iin == str(recommender_iin).lstrip().rstrip()).first()
        if recommender is None:
            continue
        op.bulk_insert(
            Base.metadata.tables["hr_erp_recommender_users"],
            [{
                'id': get_uuid(),
                'user_id': user.id,
                'recommendant': recommendant_name,
                'researcher': " ",
                'researcher_id'
                'user_by_id': recommender.id,
            }]
        )

    resarcher_sql = f"""select e.ID,
                      e.iin,
                      ec.CURATOR_ID
                      FROM HR_EMPLOYEES e
                      JOIN HR_EMP_CURATORS ec ON ec.EMPLOYEE_ID = e.ID
                      where ec.CURATOR_ID is not null"""

    for row in cursor.execute(resarcher_sql).fetchall():
        (
            e_id,
            user_iin,
            curator_id
        ) = row
        user = db.query(User).filter(User.iin == str(user_iin).lstrip().rstrip()).first()
        if user is None:
            continue
        curator_sql = f"""SELECT e.iin, e.full_name
                          FROM HR_EMPLOYEES e
                          where e.ID = {curator_id}"""
        (curator_iin, curator_full_name) = cursor.execute(curator_sql).fetchone()
        curator = db.query(User).filter(User.iin == str(curator_iin).lstrip().rstrip()).first()
        if curator is None:
            continue
        recommender = db.query(RecommenderUser).filter(RecommenderUser.user_id == user.id).first()
        if recommender is not None:
            recommender.researcher = curator_full_name
            recommender.researcher_id = curator_id
            db.add(recommender)
            db.flush()
        else:
            op.bulk_insert(
                Base.metadata.tables["hr_erp_recommender_users"],
                [{
                    'id': get_uuid(),
                    'user_id': user.id,
                    'recommendant': " ",
                    'researcher': curator_full_name,
                    'researcher_id': curator.id,
                    'user_by_id': " ",
                }]
            )


    conn.commit()


def downgrade() -> None:
    pass #test
