"""migration

Revision ID: bd9403c8f894
Revises: 461e308e6b57
Create Date: 2023-04-14 01:48:31.033124

"""
import datetime
import uuid

from alembic import op
from core import Base

from models import SpecialtyEnum

# revision identifiers, used by Alembic.
revision = 'bd9403c8f894'
down_revision = '576296a7cdac'
branch_labels = None
depends_on = None


def get_uuid():
    return str(uuid.uuid4())


# Base URL for s3
base_s3_url = 'http://192.168.0.169:8083'

# Personal
sport_type1_id = get_uuid()
sport_type2_id = get_uuid()
sport_type3_id = get_uuid()

family_status_id = get_uuid()
family_status2_id = get_uuid()
family_status3_id = get_uuid()
family_status4_id = get_uuid()

family_relation_id = get_uuid()
family_relation1_id = get_uuid()
family_relation2_id = get_uuid()
family_relation3_id = get_uuid()
family_relation4_id = get_uuid()
family_relation5_id = get_uuid()
family_relation6_id = get_uuid()
family_relation7_id = get_uuid()
family_relation8_id = get_uuid()
family_relation9_id = get_uuid()
family_relation10_id = get_uuid()
family_relation11_id = get_uuid()
family_relation12_id = get_uuid()
family_relation13_id = get_uuid()
family_relation14_id = get_uuid()
family_relation15_id = get_uuid()
family_relation16_id = get_uuid()

# Medical
liberation_id = get_uuid()
liberation2_id = get_uuid()

# Education
academic_degree_degree1_id = get_uuid()
academic_degree_degree2_id = get_uuid()

academic_title_degree1_id = get_uuid()
academic_title_degree2_id = get_uuid()

course_provider1_id = get_uuid()
course_provider2_id = get_uuid()
course_provider3_id = get_uuid()

institution_degree_type1_id = get_uuid()
institution_degree_type2_id = get_uuid()
institution_degree_type3_id = get_uuid()

science1_id = get_uuid()
science2_id = get_uuid()

specialty1_id = get_uuid()
specialty2_id = get_uuid()
specialty3_id = get_uuid()

language1_id = get_uuid()
language2_id = get_uuid()
language3_id = get_uuid()

institution1_id = get_uuid()
institution2_id = get_uuid()
institution3_id = get_uuid()
# Additional

country_id = get_uuid()

property_type1_id = get_uuid()
property_type2_id = get_uuid()
property_type3_id = get_uuid()

options = {
    'adilet@mail.ru': {
        'first_name': 'Самат',
        'father_name': 'Наурызбекович'
    },
    'ahat@mail.ru': {
        'first_name': 'Бауыржан',
        'father_name': 'Ганыбаевич'
    },
    'aset@mail.ru': {
        'first_name': 'Аслан',
        'father_name': 'Султанович'
    },
    'a_kibataev@sgo.kz': {
        'first_name': 'Козы',
        'father_name': 'Кибатаевич'
    },
    'anuar@mail.ru': {
        'first_name': 'Аманкелди',
        'father_name': 'Наурызбевович'
    },
    'a_amankeldiuly@sgo.kz': {
        'first_name': 'Гани',
        'father_name': 'Бахтиярович'
    },
    'erden@mail.ru': {
        'first_name': 'Алмат',
        'father_name': 'Ескендирович'
    },
    'erkin@mail.ru': {
        'first_name': 'Серик',
        'father_name': 'Рахатович'
    },
    's_isabekov@sgo.kz': {
        'first_name': 'Саин',
        'father_name': 'Исабекович'
    },
    'b_abdyshev@sgo.kz': {
        'first_name': 'Кадырбек',
        'father_name': 'Абдышович'
    },
    'admin@mail.com': {
        'first_name': 'Админ',
        'father_name': 'Админович'
    },
    'elena@mail.ru': {
        'first_name': 'Елена',
        'father_name': 'Петрова'
    },
    'aidar@mail.ru': {
        'first_name': 'Айдар',
        'father_name': 'Жакупов'
    },
    'kuat@mail.ru': {
        'first_name': 'Куат',
        'father_name': 'Жанатов'
    },
    'daulet@mail.ru': {
        'first_name': 'Даулет',
        'father_name': 'Кайратұлы'
    },
    'akzhol@mail.ru': {
        'first_name': 'Ақжол',
        'father_name': 'Бекмұхаметов'
    },
    'kairat@mail.ru': {
        'first_name': 'Қайрат',
        'father_name': 'Мақсұтұлы'
    },
    'sanzhar@mail.ru': {
        'first_name': 'Санжар',
        'father_name': 'Бекжанов'
    },
    'koktem@mail.ru': {
        'first_name': 'Көктем',
        'father_name': 'Исмаилова'
    },
    'alishev@mail.ru': {
        'first_name': 'Нейл',
        'father_name': 'Алишев'
    },
    'batyrbek@mail.ru': {
        'first_name': 'Батырбек',
        'father_name': 'Бакыткерей'
    },
    'kassymkhan@mail.ru': {
        'first_name': 'Касымхан',
        'father_name': 'Тлеуов'
    },
    'farkhat@mail.ru': {
        'first_name': 'Фархат',
        'father_name': 'Максатов'
    },
    'yerkebulan@mail.ru': {
        'first_name': 'Еркебулан',
        'father_name': 'Ескендиров'
    },
    'beibarys@mail.ru': {
        'first_name': 'Бейбарыс',
        'father_name': 'Телжанов'
    },
    'baltabay@mail.ru': {
        'first_name': 'Балтабай',
        'father_name': 'Баржаксы'
    },
    'askar@mail.ru': {
        'first_name': 'Аскар',
        'father_name': 'Абдурахманов'
    },
    'super.raha2002@mail.ru': {
        'first_name': 'Рахат',
        'father_name': 'Шаяхметов'
    }
}

type_of_histories = [
    "staff_unit_history",
    "rank_history",
    "penalty_history",
    "emergency_service_history",
    "work_experience_history",
    "secondment_history",
    "name_change_history",
    "attestation",
    "service_characteristic_history",
    "status_history",
    "coolness_history",
    "contract_history",
    "badge_history"
]


def create_candidate_stage_info(candidate_id,
                                candidate_stage_type_id):
    op.bulk_insert(
        Base.metadata.tables['candidate_stage_infos'],
        [{
            'id': get_uuid(),
            'candidate_stage_type_id': candidate_stage_type_id,
            'candidate_id': candidate_id,
        }]
    )


def upgrade() -> None:
    badgetype1_id = get_uuid()
    badgetype3_id = get_uuid()
    badgetype4_id = get_uuid()
    badgetype5_id = get_uuid()
    badgetype6_id = get_uuid()
    badgetype7_id = get_uuid()
    badgetype8_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['badge_types'],
        [{
            "id": badgetype1_id,
            "name": "Черный Берет",
            "nameKZ": "Қара Берет",
            "url": f"{base_s3_url}/static/black_beret.jpg"
        }, {
            "id": badgetype3_id,
            "name": "Нагрудный знак 'Ұлттық ұлан қызметінің үздігі'",
            "nameKZ": "'Ұлттық ұлан қызметінің үздігі' төсбелгісі",
            "url": f"{base_s3_url}/static/badge1.png"
        }, {
            "id": badgetype4_id,
            "name": "Нагрудный знак 'Құрметті шекарашы'",
            "nameKZ": "'Құрметті шекарашы' төсбелгісі",
            "url": f"{base_s3_url}/static/badge2.png"
        }, {
            "id": badgetype5_id,
            "name": "'Отличник Пограничной службы' 2 степени",
            "nameKZ": "2 дәрежелі 'Шекара қызметінің үздігі'",
            "url": f"{base_s3_url}/static/badge3.png"
        }, {
            "id": badgetype6_id,
            "name": "МЕДАЛЬ 'МВД РК'",
            "nameKZ": "МЕДАЛЬ 'МВД РК'",
            "url": f"{base_s3_url}/static/badge4.png"
        }, {
            "id": badgetype7_id,
            "name": "Медаль за храбрость",
            "nameKZ": "Ерлігі үшін",
            "url": f"http://193.106.99.68:2287/static/static/badge5.png"
        }, {
            "id": badgetype8_id,
            "name": "Медаль за достойную работу",
            "nameKZ": "Ерен еңбегі үшін",
            "url": f"http://193.106.99.68:2287/static/static/badge6.png"
        }]
    )

    rank1_id = get_uuid()
    rank2_id = get_uuid()
    rank3_id = get_uuid()
    rank4_id = get_uuid()
    rank5_id = get_uuid()
    rank6_id = get_uuid()
    rank7_id = get_uuid()
    rank8_id = get_uuid()
    rank9_id = get_uuid()
    rank10_id = get_uuid()
    rank11_id = get_uuid()
    rank12_id = get_uuid()
    rank13_id = get_uuid()
    rank14_id = get_uuid()
    rank15_id = get_uuid()
    rank16_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['ranks'],
        [{
            'id': rank1_id,
            'name': 'Рядовой',
            'nameKZ': 'Қатардағы жауынгер',
            'order': 1,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A0%D1%8F%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': None
        }, {
            'id': rank2_id,
            'name': 'Младший сержант',
            'nameKZ': "Кіші сержант",
            'order': 2,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9C%D0%BB%D0%B0%D0%B4%D1%88%D0%B8%D0%B9%20%D1%81%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9C%D0%BB%D0%B0%D0%B4%D1%88%D0%B8%D0%B9%20%D1%81%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank3_id,
            'name': 'Сержант',
            'nameKZ': 'Сержант',
            'order': 3,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank14_id,
            'name': 'Сержант 1-го класса',
            'nameKZ': '1-сыныпты сержант',
            'order': 4,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82%201-%D0%B3%D0%BE%20%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B0_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': None
        }, {
            'id': rank15_id,
            'name': 'Сержант 2-го класса',
            'nameKZ': '2-сыныпты сержант',
            'order': 5,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82%202-%D0%B3%D0%BE%20%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B0_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': None
        }, {
            'id': rank16_id,
            'name': 'Сержант 3-го класса',
            'nameKZ': '3-сыныпты сержант',
            'order': 6,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82%203-%D0%B3%D0%BE%20%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B0_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': None
        }, {
            'id': rank4_id,
            'name': 'Старший сержант',
            'nameKZ': 'Аға сержант',
            'order': 7,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D1%82%D0%B0%D1%80%D1%88%D0%B8%D0%B9%20%D1%81%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D1%82%D0%B0%D1%80%D1%88%D0%B8%D0%B9%20%D1%81%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank5_id,
            'name': 'Лейтенант',
            'nameKZ': 'Лейтенант',
            'order': 8,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9B%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9B%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank6_id,
            'name': 'Старший лейтенант',
            'nameKZ': 'Аға лейтенант',
            'order': 9,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D1%82%D0%B0%D1%80%D1%88%D0%B8%D0%B9%20%D0%BB%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D1%82%D0%B0%D1%80%D1%88%D0%B8%D0%B9%20%D0%BB%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank7_id,
            'name': 'Капитан',
            'nameKZ': 'Капитан',
            'order': 10,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9A%D0%B0%D0%BF%D0%B8%D1%82%D0%B0%D0%BD_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9A%D0%B0%D0%BF%D0%B8%D1%82%D0%B0%D0%BD.png"
        }, {
            'id': rank8_id,
            'name': 'Майор',
            'nameKZ': 'Майор',
            'order': 11,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9C%D0%B0%D0%B9%D0%BE%D1%80_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9C%D0%B0%D0%B9%D0%BE%D1%80.png"
        }, {
            'id': rank9_id,
            'name': 'Подполковник',
            'nameKZ': 'Подполковник',
            'order': 12,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9F%D0%BE%D0%B4%D0%BF%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9F%D0%BE%D0%B4%D0%BF%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA.png"
        }, {
            'id': rank10_id,
            'name': 'Полковник',
            'nameKZ': 'Полковник',
            'order': 13,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9F%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9F%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA.png"
        }, {
            'id': rank11_id,
            'name': 'Генерал-майор',
            'nameKZ': 'Генерал-майор',
            'order': 14,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BC%D0%B0%D0%B9%D0%BE%D1%80.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BC%D0%B0%D0%B9%D0%BE%D1%80.png"
        }, {
            'id': rank12_id,
            'name': 'Генерал-лейтенант',
            'nameKZ': 'Генерал-лейтенант',
            'order': 15,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BB%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BB%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank13_id,
            'name': 'Генерал-полковник',
            'nameKZ': 'Генерал-полковник',
            'order': 16,
            'military_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BF%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA.png",
            'employee_url': f"{base_s3_url}/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BF%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA.png"
        }]
    )

    position1_id = get_uuid()
    position2_id = get_uuid()
    position3_id = get_uuid()
    position4_id = get_uuid()
    position5_id = get_uuid()
    position6_id = get_uuid()
    position7_id = get_uuid()
    position8_id = get_uuid()
    position9_id = get_uuid()
    position10_id = get_uuid()
    position11_id = get_uuid()
    position12_id = get_uuid()
    position13_id = get_uuid()
    position14_id = get_uuid()
    position15_id = get_uuid()
    position16_id = get_uuid()
    position17_id = get_uuid()
    position18_id = get_uuid()
    position19_id = get_uuid()
    position20_id = get_uuid()
    position21_id = get_uuid()
    position22_id = get_uuid()  # Психолог
    position23_id = get_uuid()  # УСБ
    position24_id = get_uuid()  # Полиграфолог
    position25_id = get_uuid()  # Инструктор
    position26_id = get_uuid()  # Умер
    position27_id = get_uuid()  # В отставке
    position28_id = get_uuid()  # В запасе
    position29_id = get_uuid()  # Исключен из списков личного состава
    position30_id = get_uuid()  # Откомандирован в другой гос. орган
    position31_id = get_uuid()  # Погиб
    position32_id = get_uuid()  # HR

    op.bulk_insert(
        Base.metadata.tables['positions'],
        [{
            'id': position1_id,
            'name': 'Военно-служащий срочной службы',
            'nameKZ': 'Мерзімді қызмет әскери қызметшісі',
            'category_code': 'C-RG-10',
            'form': 'Форма 1',
            'max_rank_id': rank1_id,
        }, {
            'id': position2_id,
            'name': 'Сотрудник охраны 3-категории',
            'nameKZ': '3-санатты күзет қызметкері',
            'form': 'Форма 1',
            'category_code': 'C-S-12',
            'max_rank_id': rank2_id
        }, {
            'id': position3_id,
            'name': 'Сотрудник охраны 2-категории',
            'nameKZ': '2-санатты күзет қызметкері',
            'form': 'Форма 1',
            'category_code': 'C-S-11',
            'max_rank_id': rank3_id
        }, {
            'id': position4_id,
            'name': 'Сотрудник охраны 1-категории',
            'nameKZ': '1-санатты күзет қызметкері',
            'form': 'Форма 1',
            'category_code': 'C-S-10',
            'max_rank_id': rank4_id
        }, {
            'id': position5_id,
            'name': 'Офицер охраны',
            'nameKZ': 'Күзет офицері',
            'form': 'Форма 1',
            'category_code': 'C-S-9',
            'max_rank_id': rank7_id
        }, {
            'id': position6_id,
            'name': 'Старший офицер охраны',
            'nameKZ': 'Аға күзет офицері',
            'form': 'Форма 1',
            'category_code': 'C-S-8',
            'max_rank_id': rank8_id
        }, {
            'id': position7_id,
            'name': 'Старший офицер',
            'nameKZ': 'Аға офицері',
            'form': 'Форма 1',
            'category_code': 'C-RG-7',
            'max_rank_id': rank8_id
        }, {
            'id': position8_id,
            'name': 'Инспектор',
            'nameKZ': 'Инспектор',
            'form': 'Форма 1',
            'category_code': 'C-S-6',
            'max_rank_id': rank9_id
        }, {
            'id': position9_id,
            'name': 'Старший инспектор',
            'nameKZ': 'Аға инспектор',
            'form': 'Форма 1',
            'category_code': 'C-S-5',
            'max_rank_id': rank9_id
        }, {
            'id': position10_id,
            'name': 'Начальник отдела',
            'nameKZ': 'Бөлім бастығы',
            'form': 'Форма 1',
            'category_code': 'C-S-5',
            'max_rank_id': rank9_id
        }, {
            'id': position11_id,
            'name': 'Заместитель начальника управления - Начальник отдела',
            'nameKZ': 'Басқарма басытығының орынбасары - Бөлім бастығы',
            'category_code': 'C-S-6',
            'form': 'Форма 1',
            'max_rank_id': rank10_id
        }, {
            'id': position12_id,
            'name': 'Главный инспектор',
            'nameKZ': 'Бас инспектор',
            'form': 'Форма 1',
            'category_code': 'C-S-3',
            'max_rank_id': rank10_id
        }, {
            'id': position13_id,
            'name': 'Начальник управления',
            'nameKZ': 'Басқарма бастығы',
            'form': 'Форма 1',
            'category_code': 'C-S-3',
            'max_rank_id': rank10_id
        }, {
            'id': position14_id,
            'name': 'Заместитель начальника департамента',
            'nameKZ': 'Департамент бастығының орынбасары',
            'form': 'Форма 1',
            'category_code': 'C-S-2',
            'max_rank_id': rank10_id
        }, {
            'id': position15_id,
            'name': 'Начальник департамента',
            'nameKZ': 'Департамент бастығы',
            'form': 'Форма 1',
            'category_code': 'C-S-1',
            'max_rank_id': rank10_id
        }, {
            'id': position16_id,
            'name': 'Заместитель начальника Службы',
            'nameKZ': 'Қызмет бастығының орынбасары',
            'form': 'Форма 1',
            'category_code': 'C-RG-5',
            'max_rank_id': rank12_id
        }, {
            'id': position17_id,
            'name': 'Начальник Службы',
            'nameKZ': 'Қызмет бастығы',
            'form': 'Форма 1',
            'category_code': 'C-RG-5',
            'max_rank_id': rank13_id
        },
            {
                'id': position18_id,
                'name': 'Начальник кадров',
                'nameKZ': 'Кадрлар басқармасының бастығы',
                'category_code': 'C-S-4',
                'form': 'Форма 1',
                'max_rank_id': rank10_id
        }, {
            'id': position19_id,
            'name': 'Заместители начальника кадров',
            'nameKZ': 'Кадр бастығының орынбасары',
            'category_code': 'C-S-5',
            'form': 'Форма 1',
            'max_rank_id': rank10_id
        }, {
            'id': position20_id,
            'name': 'Начальник управления кандидатами',
            'nameKZ': 'Кандидаттар басқармасының бастығы',
            'category_code': 'C-S-4',
            'form': 'Форма 1',
            'max_rank_id': rank10_id
        }, {
            'id': position21_id,
            'name': 'Политический гос. служащий',
            'nameKZ': 'Саяси мемлекеттік қызметші',
            'category_code': 'C-S-4',
            'form': 'Форма 1',
            'max_rank_id': rank16_id
        }, {
            'id': position22_id,
            'name': 'Психолог',
            'nameKZ': 'Психолог',
            'category_code': 'C-S-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position23_id,
            'name': 'Представитель Управление собственной безопасности',
            'nameKZ': 'Өкіл жеке қауіпсіздік басқармасы',
            'category_code': 'C-S-6',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position24_id,
            'name': 'Полиграфолог',
            'nameKZ': 'Полиграфолог',
            'category_code': 'C-S-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position25_id,
            'name': 'Инструктор',
            'nameKZ': 'Инструктор',
            'category_code': 'C-S-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position26_id,
            'name': "Умер",
            'nameKZ': 'Өлі',
            'category_code': 'C-RG-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position27_id,
            'name': "В отставке",
            'nameKZ': 'Зейнеткер',
            'category_code': 'C-RG-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position28_id,
            'name': "В запасе",
            'nameKZ': 'Резервте',
            'category_code': 'C-RG-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position29_id,
            'name': "Исключен из списков личного состава",
            'nameKZ': 'Кадрлар тізімінен шығарылған',
            'category_code': 'C-RG-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position30_id,
            'name': "Откомандирован в другой гос. орган",
            'nameKZ': 'Басқа мемлекеттік органға жіберілді',
            'category_code': 'C-RG-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position31_id,
            'name': "Погиб",
            'nameKZ': 'Қайтыс болды',
            'category_code': 'C-RG-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }, {
            'id': position32_id,
            'name': "HR-менеджер",
            'nameKZ': 'HR-менеджері',
            'category_code': 'C-RG-10',
            'form': 'Форма 1',
            'max_rank_id': rank9_id
        }]
    )

    hr_document_status_id = get_uuid()
    hr_document_status2_id = get_uuid()
    hr_document_status3_id = get_uuid()
    hr_document_status4_id = get_uuid()
    hr_document_status5_id = get_uuid()
    hr_document_status6_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_document_statuses'],
        [{
            'id': hr_document_status_id,
            'name': "Иницилизирован",
            'nameKZ': "Басталды",
        }, {
            'id': hr_document_status2_id,
            'name': "В процессе",
            'nameKZ': 'Үдерісте',
        }, {
            'id': hr_document_status3_id,
            'name': "Завершен",
            'nameKZ': 'Аяқталды',
        }, {
            'id': hr_document_status4_id,
            'name': "Отменен",
            'nameKZ': 'Күші жойылды'
        }, {
            'id': hr_document_status5_id,
            'name': "На доработке",
            'nameKZ': 'Қайта қаралуда'
        }, {
            'id': hr_document_status6_id,
            'name': "Черновик",
            'nameKZ': 'Бастаулық'
        }]
    )

    staff_division_type_id = get_uuid()
    staff_division_type2_id = get_uuid()
    staff_division_type3_id = get_uuid()
    staff_division_type4_id = get_uuid()
    staff_division_type5_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['staff_division_types'],
        [{
            'id': staff_division_type_id,
            'name': "Департамент",
            'nameKZ': "Департамент",
        }, {
            'id': staff_division_type2_id,
            'name': "Управление",
            'nameKZ': 'Управление',
        }, {
            'id': staff_division_type3_id,
            'name': "Отдел",
            'nameKZ': 'Отдел',
        }, {
            'id': staff_division_type4_id,
            'name': "Универсал",
            'nameKZ': 'Универсал'
        }, {
            'id': staff_division_type5_id,
            'name': "Группа",
            'nameKZ': 'Группа'
        }]
    )

    doc_type1_id = get_uuid()
    doc_type2_id = get_uuid()
    doc_type3_id = get_uuid()
    doc_type4_id = get_uuid()
    doc_type5_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['document_function_types'],
        [{
            'id': doc_type1_id,
            'name': "Согласующий",
            'nameKZ': "Келісуші",
            'can_cancel': True
        }, {
            'id': doc_type2_id,
            'name': "Эксперт",
            'nameKZ': "Сарапшы",
            'can_cancel': False
        }, {
            'id': doc_type3_id,
            'name': "Утверждающий",
            'nameKZ': 'Бекітуші',
            'can_cancel': True
        }, {
            'id': doc_type4_id,
            'name': "Уведомляемый",
            'nameKZ': 'Хабарландырушы',
            'can_cancel': False
        }, {
            'id': doc_type5_id,
            'name': "Инициатор",
            'nameKZ': 'Бастаушы',
            'can_cancel': True
        }]
    )

    jurisdiction_id = get_uuid()
    jurisdiction2_id = get_uuid()
    jurisdiction3_id = get_uuid()
    jurisdiction4_id = get_uuid()
    jurisdiction5_id = get_uuid()
    jurisdiction6_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['jurisdictions'],
        [{
            'id': jurisdiction_id,
            'name': "Вся служба",
            'nameKZ': 'Барлық қызмет'
        }, {
            'id': jurisdiction2_id,
            'name': "Личный Состав",
            'nameKZ': 'Жеке құрамы'
        }, {
            'id': jurisdiction3_id,
            'name': "Боевое Подразделение",
            'nameKZ': 'Жауынгерлік Бөлімшесі'
        }, {
            'id': jurisdiction4_id,
            'name': "Штабное Подразделение",
            'nameKZ': 'Штаб Бөлімшесі'
        }, {
            'id': jurisdiction5_id,
            'name': "Кандидаты",
            'nameKZ': 'Үміткерлер'
        }, {
            'id': jurisdiction6_id,
            'name': "Курьируемые сотрудники",
            'nameKZ': 'Жетекшілік ететін қызметкерлер'
        }]
    )

    staff_function1_id = get_uuid()
    staff_function2_id = get_uuid()
    staff_function3_id = get_uuid()
    staff_function4_id = get_uuid()
    staff_function5_id = get_uuid()
    staff_function6_id = get_uuid()
    staff_function7_id = get_uuid()
    staff_function8_id = get_uuid()
    staff_function9_id = get_uuid()
    staff_function10_id = get_uuid()
    staff_function11_id = get_uuid()
    staff_function12_id = get_uuid()

    # new
    staff_function13_id = get_uuid()
    staff_function14_id = get_uuid()
    staff_function15_id = get_uuid()
    staff_function16_id = get_uuid()
    staff_function17_id = get_uuid()
    staff_function18_id = get_uuid()
    staff_function19_id = get_uuid()
    staff_function20_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['staff_functions'],
        [{
            'id': staff_function1_id,
            'hours_per_week': 3,
            'discriminator': 'document_staff_function',
            'name': 'Инициатор приказа о назначении',
            'nameKZ': 'Тағайындау бұйрығының бастаушысы',
            'jurisdiction_id': jurisdiction_id,
            'priority': 1,
            'role_id': doc_type5_id
        },
            {
                'id': staff_function2_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Эксперт приказа о назначении',
                'nameKZ': 'Тағайындау бұйрығының сарапшысы',
                'jurisdiction_id': jurisdiction_id,
                'priority': 2,
                'role_id': doc_type2_id
        },
            {
                'id': staff_function3_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Утверждающий приказа о назначении',
                'nameKZ': 'Тағайындау бұйрығының бекітушісі',
                'jurisdiction_id': jurisdiction_id,
                'priority': 100,
                'role_id': doc_type3_id
        },
            {
                'id': staff_function4_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Инициатор приказа о присвоения звания',
                'nameKZ': 'Атақ беру бұйрығының бастаушысы',
                'jurisdiction_id': jurisdiction_id,
                'priority': 1,
                'role_id': doc_type5_id
        },
            {
                'id': staff_function5_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Эксперт приказа о присвоения звания',
                'nameKZ': 'Атақ беру бұйрығының сарапшысы',
                'jurisdiction_id': jurisdiction_id,
                'priority': 2,
                'role_id': doc_type2_id
        },
            {
                'id': staff_function6_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Утверждающий приказа о присвоения звания',
                'nameKZ': 'Атақ беру бұйрығының бекітушісі',
                'jurisdiction_id': jurisdiction_id,
                'priority': 100,
                'role_id': doc_type3_id
        },
            {
                'id': staff_function7_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Инициатор приказа о присвоения черного берета',
                'nameKZ': 'Қара берет беру бұйрығының бастаушысы',
                'jurisdiction_id': jurisdiction_id,
                'priority': 1,
                'role_id': doc_type5_id
        },
            {
                'id': staff_function8_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Эксперт приказа о присвоения черного берета',
                'nameKZ': 'Қара берет беру бұйрығының сарапшысы',
                'jurisdiction_id': jurisdiction_id,
                'priority': 2,
                'role_id': doc_type2_id
        },
            {
                'id': staff_function9_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Утверждающий приказа о присвоения черного берета',
                'nameKZ': 'Қара берет беру бұйрығының бекітушісі',
                'jurisdiction_id': jurisdiction_id,
                'priority': 100,
                'role_id': doc_type3_id
        }, {
            'id': staff_function10_id,
            'hours_per_week': 3,
            'discriminator': 'document_staff_function',
            'name': 'Согласующий приказа о присвоения звания',
            'nameKZ': 'Атақ беру бұйрығының келісушісі',
            'jurisdiction_id': jurisdiction_id,
            'priority': 3,
            'role_id': doc_type1_id
        }, {
            'id': staff_function11_id,
            'hours_per_week': 3,
            'discriminator': 'document_staff_function',
            'name': 'Согласующий приказа о присвоения черного берета',
            'nameKZ': 'Қара берет беру бұйрығының келісушісі',
            'jurisdiction_id': jurisdiction_id,
            'priority': 3,
            'role_id': doc_type1_id
        }, {
            'id': staff_function12_id,
            'hours_per_week': 3,
            'discriminator': 'document_staff_function',
            'name': 'Согласующий приказа о назначении',
            'nameKZ': 'Тағайындау бұйрығының келісушісі',
            'jurisdiction_id': jurisdiction_id,
            'priority': 3,
            'role_id': doc_type1_id
        },
            {
                'id': staff_function13_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Инициатор приказа об изменении штатного расписания',
                'nameKZ': 'Штаттық кестені өзгерту туралы бұйрықтың бастамашысы',
                'jurisdiction_id': jurisdiction_id,
                'priority': 1,
                'role_id': doc_type5_id
        },
            {
                'id': staff_function14_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Согласующий приказа об изменении штатного расписания',
                'nameKZ': 'Штаттық кестені өзгерту туралы бұйрықтың келісушісі',
                'jurisdiction_id': jurisdiction_id,
                'priority': 3,
                'role_id': doc_type1_id
        },
            {
                'id': staff_function15_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Эксперт приказа об изменении штатного расписания',
                'nameKZ': 'Штаттық кестені өзгерту туралы бұйрықтың сарапшысы',
                'jurisdiction_id': jurisdiction_id,
                'priority': 2,
                'role_id': doc_type2_id
        },

            {
                'id': staff_function16_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Утверждающий приказа об изменении штатного расписания',
                'nameKZ': 'Штаттық кестені өзгерту туралы бұйрықтың бекітушісі',
                'jurisdiction_id': jurisdiction_id,
                'priority': 100,
                'role_id': doc_type3_id
        },
            {
                'id': staff_function17_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Инициатор приказа об назначении на должность (штатное расписание)',
                'nameKZ': 'Штаттық кестенің (жұмыс кестесінің) мүшесіне тағайындау туралы бұйрықтың бастамашысы',
                'jurisdiction_id': jurisdiction_id,
                'priority': 1,
                'role_id': doc_type5_id
        },
            {
                'id': staff_function18_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Согласующий приказа о назначении на должность (штатное расписание)',
                'nameKZ': 'Штаттық кестенің (жұмыс кестесінің) мүшесіне тағайындау туралы бұйрықтың келісушісі',
                'jurisdiction_id': jurisdiction_id,
                'priority': 3,
                'role_id': doc_type1_id
        },
            {
                'id': staff_function19_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Эксперт приказа о назначении на должность (штатное расписание)',
                'nameKZ': 'Штаттық кестенің (жұмыс кестесінің) мүшесіне тағайындау туралы бұйрықтың сарапшысы',
                'jurisdiction_id': jurisdiction_id,
                'priority': 2,
                'role_id': doc_type2_id
        },

            {
                'id': staff_function20_id,
                'hours_per_week': 3,
                'discriminator': 'document_staff_function',
                'name': 'Утверждающий приказа о назначении на должность (штатное расписание)',
                'nameKZ': 'Штаттық кестенің (жұмыс кестесінің) мүшесіне тағайындау туралы бұйрықтың бекітушісі',
                'jurisdiction_id': jurisdiction_id,
                'priority': 100,
                'role_id': doc_type3_id
        }

        ]
    )

    # Personal tables

    op.bulk_insert(
        Base.metadata.tables['sport_types'],
        [{
            'id': sport_type1_id,
            'name': "Бокс",
            'nameKZ': "Бокс"
        }, {
            'id': sport_type2_id,
            'name': "Карате",
            'nameKZ': "Карате"
        }, {
            'id': sport_type3_id,
            'name': "Джиу-Джитсу",
            'nameKZ': "Джиу-Джитсу"
        }]
    )

    # Educational tables

    op.bulk_insert(
        Base.metadata.tables['academic_degree_degrees'],
        [{
            'id': academic_degree_degree1_id,
            'name': "Доктор Наук (PhD)",
            'nameKZ': 'Ғылым Докторы (PhD)'
        }, {
            'id': academic_degree_degree2_id,
            'name': "Кандидат Доктора Наук",
            'nameKZ': 'Ғылым кандидаты Наук'
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['academic_title_degrees'],
        [{
            'id': academic_title_degree1_id,
            'name': "Профессор",
            'nameKZ': 'Профессор'
        }, {
            'id': academic_title_degree2_id,
            'name': "Доцент",
            'nameKZ': 'Доцент'
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['course_providers'],
        [{
            'id': course_provider1_id,
            'name': "StepUp academy",
            'nameKZ': 'StepUp academy'
        }, {
            'id': course_provider2_id,
            'name': "Udemy.com",
            'nameKZ': 'Udemy.com'
        }, {
            'id': course_provider3_id,
            'name': "Coursera.com",
            'nameKZ': 'Coursera.com'
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['institution_degree_types'],
        [{
            'id': institution_degree_type1_id,
            'name': "Среднее",
            'nameKZ': 'Орта'
        }, {
            'id': institution_degree_type2_id,
            'name': "Бакалавриат",
            'nameKZ': 'Бакалавриат'
        }, {
            'id': institution_degree_type3_id,
            'name': "Магистратура",
            'nameKZ': 'Магистратура'
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['sciences'],
        [{
            'id': science1_id,
            'name': "Психологическая Наука",
            'nameKZ': 'Психологиялық Ғылым',
        }, {
            'id': science2_id,
            'name': "Военная Наука",
            'nameKZ': 'Әскери Ғылым',
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['specialties'],
        [{
            'id': specialty1_id,
            'name': "Нейронные связи",
            'nameKZ': 'Нейрондық байланыстар'
        }, {
            'id': specialty2_id,
            'name': "Квантовая физика",
            'nameKZ': 'Кванттық физика'
        }, {
            'id': specialty3_id,
            'name': "Биохимия",
            'nameKZ': 'Биохимия'
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['languages'],
        [{
            'id': language1_id,
            'name': "Казахский язык",
            'nameKZ': 'Қазақ тілі',
        }, {
            'id': language2_id,
            'name': "Английский язык",
            'nameKZ': 'Ағылшын тілі',
        }, {
            'id': language3_id,
            'name': "Русский язык",
            'nameKZ': 'Орыс тілі',
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['institutions'],
        [{
            'id': institution1_id,
            'name': 'Лицей "Бiлiм-Инновация',
            'nameKZ': 'Бiлiм-Инновация лицей'
        }, {
            'id': institution2_id,
            'name': "Astana IT University",
            'nameKZ': 'Astana IT University'
        }]
    )

    # Additional profile tables

    op.bulk_insert(
        Base.metadata.tables['countries'],
        [{
            'id': country_id,
            'name': "Турция",
            'nameKZ': "Түркия"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['property_types'],
        [{
            'id': property_type1_id,
            'name': "Двухэтажный дом",
            'nameKZ': "Екі қабатты үй"
        }, {
            'id': property_type2_id,
            'name': "1-комнтаная квартира",
            'nameKZ': '1 бөлмелі пәтер'
        }, {
            'id': property_type3_id,
            'name': "2-комнатная квартира",
            'nameKZ': '2 бөлмелі пәтер'
        }]
    )

    group1_id = get_uuid()
    group2_id = get_uuid()
    group3_id = get_uuid()
    group4_id = get_uuid()
    group5_id = get_uuid()
    group6_id = get_uuid()
    group7_id = get_uuid()
    group8_id = get_uuid()
    group9_id = get_uuid()
    group10_id = get_uuid()
    group11_id = get_uuid()
    group12_id = get_uuid()
    group13_id = get_uuid()
    group14_id = get_uuid()
    group15_id = get_uuid()
    group16_id = get_uuid()
    group2_1_id = get_uuid()

    all_service_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['staff_divisions'],
        [{
            'parent_group_id': None,
            'id': all_service_id,
            'name': "СГО РК",
            'nameKZ': 'ҚР МКҚ',
            'staff_division_number': None,
            'type_id': None,
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'is_combat_unit': False,
            'is_visible': True,
        }, {
            'parent_group_id': all_service_id,
            'id': group1_id,
            'staff_division_number': 5,
            'name': "Пятый департамент",
            'nameKZ': "Бесінші департаменті",
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'type_id': staff_division_type_id,
            'is_combat_unit': True,
            'is_visible': True,
        }, {
            'parent_group_id': group1_id,
            'id': group2_id,
            'staff_division_number': 1,
            'name': "1 управление",
            'nameKZ': '1 басқару',
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'type_id': staff_division_type2_id,
            'is_combat_unit': False,
            'is_visible': True,
        }, {
            'parent_group_id': group1_id,
            'id': group3_id,
            'staff_division_number': 2,
            'name': "2 управление",
            'nameKZ': '2 басқару',
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'type_id': staff_division_type2_id,
            'is_combat_unit': True,
            'is_visible': True,
        }, {
            'parent_group_id': group1_id,
            'id': group4_id,
            'staff_division_number': 3,
            'name': "3 управление",
            'nameKZ': '3 басқару',
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'type_id': staff_division_type2_id,
            'is_combat_unit': False,
            'is_visible': True,
        }, {
            'parent_group_id': group1_id,
            'id': group5_id,
            'staff_division_number': 4,
            'name': "4 управление",
            'nameKZ': '4 басқару',
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'type_id': staff_division_type2_id,
            'is_combat_unit': True,
            'is_visible': True,
        }, {
            'parent_group_id': None,
            'id': group6_id,
            'name': "Особая группа",
            'nameKZ': 'Арнайы группа',
            'staff_division_number': None,
            'type_id': None,
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'is_combat_unit': False,
            'is_visible': False,
        }, {
            'parent_group_id': group6_id,
            'id': group7_id,
            'name': "Кандидаты",
            'nameKZ': 'Кандидаттар',
            'staff_division_number': None,
            'type_id': None,
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'is_combat_unit': False,
            'is_visible': False,
        }, {
            'parent_group_id': group6_id,
            'id': group8_id,
            'name': "Умер",
            'nameKZ': 'Өлі',
            'staff_division_number': None,
            'type_id': None,
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'is_combat_unit': False,
            'is_visible': False,
        }, {
            'parent_group_id': group6_id,
            'id': group9_id,
            'name': "В отставке",
            'nameKZ': 'Зейнеткер',
            'staff_division_number': None,
            'type_id': None,
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'is_combat_unit': False,
            'is_visible': False,
        }, {
            'parent_group_id': group6_id,
            'id': group10_id,
            'name': "В запасе",
            'nameKZ': 'Резервте',
            'staff_division_number': None,
            'type_id': None,
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'is_combat_unit': False,
            'is_visible': False,
        }, {
            'parent_group_id': group6_id,
            'id': group11_id,
            'name': "Исключен из списков личного состава",
            'nameKZ': 'Кадрлар тізімінен шығарылған',
            'staff_division_number': None,
            'type_id': None,
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'is_combat_unit': False,
            'is_visible': False,
        }, {
            'parent_group_id': group6_id,
            'id': group12_id,
            'name': "Откомандирован в другой гос. орган",
            'nameKZ': 'Басқа мемлекеттік органға жіберілді',
            'staff_division_number': None,
            'type_id': None,
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'is_combat_unit': False,
            'is_visible': False,
        }, {
            'parent_group_id': group6_id,
            'id': group13_id,
            'name': "Погиб",
            'nameKZ': 'Қайтыс болды',
            'staff_division_number': None,
            'type_id': None,
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'is_combat_unit': False,
            'is_visible': False,
        }, {
            'parent_group_id': all_service_id,
            'id': group14_id,
            'staff_division_number': 7,
            'name': "Седьмой департамент",
            'nameKZ': "Жетінші департаменті",
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'type_id': staff_division_type_id,
            'is_combat_unit': True,
            'is_visible': True,
        }, {
            'parent_group_id': group14_id,
            'id': group15_id,
            'staff_division_number': 3,
            'name': "3 управление",
            'nameKZ': '3 басқару',
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'type_id': staff_division_type2_id,
            'is_combat_unit': False,
            'is_visible': True,
        }, {
            'parent_group_id': group15_id,
            'id': group16_id,
            'staff_division_number': 1,
            'name': "1 отдел",
            'nameKZ': '1 бөлім',
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'type_id': staff_division_type3_id,
            'is_combat_unit': False,
            'is_visible': True,
        },  {
            'parent_group_id': group15_id,
            'id': group2_1_id,
            'staff_division_number': 2,
            'name': "2 отдел",
            'nameKZ': '2 бөлім',
            'description': {
                "name": 'Департамент управления финансами отвечает за управление и ведение учета финансовых операций компании. Он отвечает за сбор, анализ и отчетность о всех финансовых операциях, производимых внутри компании.Задачи департамента финансов включают в себя следующее:' +
                'Составление бюджетов и финансовых планов на текущий и будущий год;' +
                'Обеспечение достаточности финансовых ресурсов для реализации стратегических целей компании;Отслеживание финансовых показателей и оценка финансовой эффективности деятельности компании;' +
                'Разработка и внедрение системы контроля и управления финансовыми рисками;Оценка инвестиционных возможностей и принятие решений о вложении средств компании в различные проекты;' +
                'Составление отчетности о финансовом положении компании и подготовка отчетов для внешних заинтересованных сторон.' +
                '    Департамент финансов должен иметь высокую квалификацию сотрудников, занимающихся финансовыми вопросами, и использовать передовые методы управления и анализа данных. Он должен тесно сотрудничать с другими департаментами компании, чтобы обеспечить наилучшие результаты в рамках общей стратегии компании.',
                "nameKZ": 'Қаржыны басқару департаменті компанияның қаржылық операцияларын басқаруға және есепке алуға жауапты. Ол компания ішінде жасалатын барлық қаржылық операцияларды жинауға, талдауға және есеп беруге жауапты.Қаржы департаментінің міндеттері мыналарды қамтиды:' +
                'Ағымдағы және келер жылға арналған бюджеттер мен қаржылық жоспарларды жасау;' +
                'Компанияның стратегиялық мақсаттарын іске асыру үшін қаржы ресурстарының жеткіліктілігін қамтамасыз ету;қаржылық көрсеткіштерді қадағалау және Компания қызметінің қаржылық тиімділігін бағалау;' +
                'Қаржылық тәуекелдерді бақылау және басқару жүйесін әзірлеу және енгізу; инвестициялық мүмкіндіктерді бағалау және компанияның қаражатын әртүрлі жобаларға салу туралы шешім қабылдау;' +
                'Компанияның қаржылық жағдайы туралы есеп беру және сыртқы мүдделі тараптар үшін есептер дайындау.' +
                'Қаржы департаменті қаржылық мәселелермен айналысатын қызметкерлердің жоғары біліктілігіне ие болуы керек және деректерді басқару мен талдаудың озық әдістерін қолдануы керек. Ол компанияның жалпы Стратегиясында ең жақсы нәтижелерді қамтамасыз ету үшін компанияның басқа департаменттерімен тығыз жұмыс істеуі керек.'
            },
            'type_id': staff_division_type3_id,
            'is_combat_unit': False,
            'is_visible': True,
        }]
    )

    staff_unit1_id = get_uuid()
    staff_unit2_id = get_uuid()
    staff_unit3_id = get_uuid()
    staff_unit4_id = get_uuid()
    staff_unit5_id = get_uuid()
    staff_unit6_id = get_uuid()
    staff_unit7_id = get_uuid()
    staff_unit8_id = get_uuid()
    staff_unit9_id = get_uuid()
    staff_unit10_id = get_uuid()
    staff_unit11_id = get_uuid()
    staff_unit12_id = get_uuid()
    staff_unit13_id = get_uuid()
    staff_unit14_id = get_uuid()
    staff_unit15_id = get_uuid()
    staff_unit16_id = get_uuid()
    staff_unit17_id = get_uuid()
    staff_unit18_id = get_uuid()
    staff_unit19_id = get_uuid()
    staff_unit20_id = get_uuid()
    staff_unit21_id = get_uuid()
    staff_unit22_id = get_uuid()
    staff_unit23_id = get_uuid()
    staff_unit25_id = get_uuid()
    staff_unit26_id = get_uuid()
    staff_unit27_id = get_uuid()
    staff_unit28_id = get_uuid()
    staff_unit29_id = get_uuid()
    staff_unit30_id = get_uuid()
    staff_unit31_id = get_uuid()
    staff_unit32_id = get_uuid()
    staff_unit33_id = get_uuid()
    staff_unit34_id = get_uuid()

    empty_unit_id = get_uuid()

    empty_unit1_id = get_uuid()
    empty_unit2_id = get_uuid()
    empty_unit3_id = get_uuid()
    empty_unit4_id = get_uuid()
    empty_unit5_id = get_uuid()
    empty_unit6_id = get_uuid()
    empty_unit7_id = get_uuid()
    empty_unit8_id = get_uuid()
    empty_unit9_id = get_uuid()
    empty_unit10_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['staff_units'],
        [{
            'id': staff_unit12_id,
            'user_id': None,
            'position_id': position5_id,
            'staff_division_id': group1_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': staff_unit13_id,
            'user_id': None,
            'position_id': position3_id,
            'staff_division_id': group2_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': staff_unit14_id,
            'user_id': None,
            'position_id': position4_id,
            'staff_division_id': group3_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit_id,
            'user_id': None,
            'position_id': position4_id,
            'staff_division_id': group2_1_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit1_id,
            'user_id': None,
            'position_id': position12_id,
            'staff_division_id': group2_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit2_id,
            'user_id': None,
            'position_id': position9_id,
            'staff_division_id': group2_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": [
                                    "Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                    "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit3_id,
            'user_id': None,
            'position_id': position8_id,
            'staff_division_id': group2_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit4_id,
            'user_id': None,
            'position_id': position8_id,
            'staff_division_id': group5_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit5_id,
            'user_id': None,
            'position_id': position8_id,
            'staff_division_id': group5_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit6_id,
            'user_id': None,
            'position_id': position8_id,
            'staff_division_id': group16_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit7_id,
            'user_id': None,
            'position_id': position7_id,
            'staff_division_id': group16_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit8_id,
            'user_id': None,
            'position_id': position6_id,
            'staff_division_id': group16_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit9_id,
            'user_id': None,
            'position_id': position8_id,
            'staff_division_id': group2_1_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }, {
            'id': empty_unit10_id,
            'user_id': None,
            'position_id': position6_id,
            'staff_division_id': group2_1_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        },]
    )

    op.bulk_insert(
        Base.metadata.tables['family_statuses'],
        [{
            'id': family_status_id,
            'name': "Женат / Замужем",
            'nameKZ': 'Үйленген / Тұрмысқа шыққан'
        }, {
            'id': family_status2_id,
            'name': "Не женат / Не замужем",
            'nameKZ': 'Үйленбеген / Тұрмысқа құрмаған'
        }, {
            'id': family_status3_id,
            'name': "Разведен-а",
            'nameKZ': 'Ажырасқан'
        }, {
            'id': family_status4_id,
            'name': "Вдовец / Вдова",
            'nameKZ': 'Жесір / Жесір'
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['family_relations'],
        [{
            'id': family_relation_id,
            'name': 'Отец',
            'nameKZ': 'Әкесі'
        }, {
            'id': family_relation1_id,
            'name': 'Отчим',
            'nameKZ': 'Өгей әкесі'
        }, {
            'id': family_relation2_id,
            'name': 'Мать',
            'nameKZ': 'Анасы'
        }, {
            'id': family_relation3_id,
            'name': 'Мачеха',
            'nameKZ': 'Өгей анасы'
        }, {
            'id': family_relation4_id,
            'name': 'Супруг(-а)',
            'nameKZ': 'Жұбайы'
        }, {
            'id': family_relation5_id,
            'name': 'Отец супруги',
            'nameKZ': 'Жұбайының әкесі'
        }, {
            'id': family_relation6_id,
            'name': 'Мать супруги',
            'nameKZ': 'Жұбайының анасы'
        }, {
            'id': family_relation7_id,
            'name': 'Отчим супруги',
            'nameKZ': 'Жұбайының өгей әкесі'
        }, {
            'id': family_relation8_id,
            'name': 'Мачеха супруги',
            'nameKZ': 'Жұбайының өгей анасы'
        }, {
            'id': family_relation9_id,
            'name': 'Сын',
            'nameKZ': 'Ұлы'
        }, {
            'id': family_relation10_id,
            'name': 'Усыновлен',
            'nameKZ': 'Асырап алған ұлы'
        }, {
            'id': family_relation11_id,
            'name': 'Удочерен',
            'nameKZ': 'Асырап алған қызы'
        }, {
            'id': family_relation12_id,
            'name': 'Брат',
            'nameKZ': 'Інісі'
        }, {
            'id': family_relation13_id,
            'name': 'Сестра',
            'nameKZ': 'Апасы'
        }, {
            'id': family_relation14_id,
            'name': 'Брат супруги',
            'nameKZ': 'Жұбайының інісі'
        }, {
            'id': family_relation15_id,
            'name': 'Сестра супруги',
            'nameKZ': 'Жұбайының апасы'
        }, {
            'id': family_relation16_id,
            'name': 'Внук/Внучка',
            'nameKZ': 'Немересі'
        }, ]
    )

    op.bulk_insert(
        Base.metadata.tables['liberations'],
        [{
            'id': liberation_id,
            'name': 'Физические нагрузки',
            'nameKZ': 'Дене белсенділігі'
        }, {
            'id': liberation2_id,
            'name': 'Дежурство',
            'nameKZ': 'Кезекшілік'
        }]
    )

    user1_id = "704e13e5-2970-4dce-9db3-1dfcdfd25b7d"
    user2_id = "b387564a-a25f-4cdf-8fd0-642a3c221548"
    user3_id = "6175b070-c683-4e7b-b59a-3685a433506d"
    user4_id = "16fbddb8-f09d-4cfe-acc5-5768bcc40397"
    user5_id = "34525614-c698-4e40-a548-62f41aba2557"
    user6_id = "544941b6-463f-4e02-a0dd-b67bc67bb83a"
    user7_id = "5d6f53c2-8f9f-4d0d-9b50-c24aa51f6574"
    user8_id = "dfd0a5ec-a23a-47af-8f1c-fb5e4813f570"
    user9_id = "dc4b2cd6-00ca-439e-bb8b-fba49ac3df3c"
    user10_id = "356f26fa-c181-47ba-972d-ad17d132c0cd"
    user11_id = "c41e20f4-097d-4ab4-b8eb-623068054e06"
    user12_id = "21a07369-1745-405b-9c4e-d17a4e448abf"
    user13_id = "1cd68211-502f-4f91-918d-7da3ce64e112"
    user14_id = "a0b4357a-5422-49d9-b43d-07291a732c44"
    user15_id = "3f7451bb-ff2f-4f81-93c9-fe2c7074ff64"
    user16_id = "40f0040e-5d6d-48d2-9a98-24c06c8dfeae"
    user17_id = "6ebd4b23-ed91-4090-9c74-d9d606ac6d9a"
    user18_id = "9c05476f-b398-44df-ad2f-4c6a55cc1050"
    user19_id = "17b04b7c-f019-40d8-82b3-1035ed0731d1"
    user21_id = "03a99775-01f2-45d9-8caa-e5cd83324dae"
    user22_id = get_uuid()
    user23_id = get_uuid()
    user24_id = get_uuid()
    user25_id = get_uuid()
    user26_id = get_uuid()
    user27_id = get_uuid()
    user28_id = get_uuid()
    user29_id = get_uuid()
    user30_id = get_uuid()

    admin_user_id = "d2f57daa-f8e9-4d66-82d2-b184c3fdf7be"

    create_user(
        user10_id,
        "Сакен",
        "Исабеков",
        'Саинович',
        's_isabekov@sgo.kz',
        all_service_id,
        None,
        "21",
        '10',
        staff_unit10_id,
        rank11_id,
        staff_unit10_id,
        f"{base_s3_url}/static/isabekov.jpg",
        position17_id,
        True,
        "А0201",
        True)
    create_user(
        user1_id,
        "Адилет",
        "Наурызбаев",
        'Саматович',
        'adilet@mail.ru',
        group2_id,
        user10_id,
        "Альфа 1",
        '1',
        staff_unit1_id,
        rank1_id,
        staff_unit1_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position1_id,
        True,
        '1.2.213K',
        True)
    create_user(
        user2_id,
        "Жандос",
        "Доспенбетов",
        'Гаухарбекович',
        'zh_dospenbetov@sgo.kz',
        group3_id,
        user10_id,
        "Альфа 2",
        '2',
        staff_unit2_id,
        rank1_id,
        staff_unit2_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position1_id,
        True,
        '1.2.213K',
        True)
    create_user(
        user3_id,
        "Асет",
        "Султанов",
        'Асланович',
        'aset@mail.ru',
        group2_id,
        user10_id,
        "Альфа 3",
        '3',
        staff_unit3_id,
        rank1_id,
        staff_unit3_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position1_id,
        True,
        '1.2.214K',
        True)
    create_user(
        user4_id,
        "Аскер",
        "Кибатаев",
        'Козыевич',
        'a_kibataev@sgo.kz',
        group14_id,
        user10_id,
        "Алан-40",
        '4',
        staff_unit4_id,
        rank9_id,
        staff_unit4_id,
        f"{base_s3_url}/static/kibataev.png",
        position11_id,
        False,
        "А0913",
        True)
    create_user(
        user5_id,
        "Ануар",
        "Наурызбеков",
        'Дидарович',
        'anuar@mail.ru',
        group2_id,
        user10_id,
        "Альфа 5",
        '5',
        staff_unit5_id,
        rank1_id,
        staff_unit5_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position1_id,
        True,
        "1.2.215K",
        True)
    create_user(
        user6_id,
        "Айтым",
        "Аманкелдіұлы",
        None,
        'a_amankeldiuly@sgo.kz',
        group2_1_id,
        user10_id,
        "Семсер-12",
        '6',
        staff_unit6_id,
        rank8_id,
        staff_unit6_id,
        f"{base_s3_url}/static/amankeldiuly.jpg",
        position8_id,
        False,
        'B0412',
        True)
    create_user(
        user7_id,
        "Ерден",
        "Ескендиров",
        'Алматович',
        'erden@mail.ru',
        group2_1_id,
        user10_id,
        "Альфа 7",
        '7',
        staff_unit7_id,
        rank1_id,
        staff_unit7_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position1_id,
        True,
        '1.2.215K',
        True)
    create_user(
        user8_id,
        "Максим",
        "Козенко",
        'Викторович',
        'm_kozenko@sgo.kz',
        group4_id,
        None,
        "Альфа 8",
        '8',
        staff_unit8_id,
        rank10_id,
        staff_unit8_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position13_id,
        True,
        "1.2.216K",
        True)
    create_user(
        user9_id,
        "Батырбек",
        "Абдышев",
        'Кадырбекович',
        'b_abdyshev@sgo.kz',
        group14_id,
        user10_id,
        "Алан-1",
        '9',
        staff_unit9_id,
        rank10_id,
        staff_unit9_id,
        f"{base_s3_url}/static/abdyshev.jpg",
        position15_id,
        True,
        "А0915",
        True)
    create_user(
        user11_id,
        "Елена",
        "Петрова",
        'Игоревна',
        'elena@mail.ru',
        group3_id,
        None,
        "Альфа 11",
        '11',
        staff_unit15_id,
        rank5_id,
        staff_unit15_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position22_id,
        True,
        "1.2.217K",
        True)
    create_user(
        user12_id,
        "Лилия",
        "Агажаева",
        'Онерхановна',
        'l_agazhaeva@sgo.kz',
        group5_id,
        None,
        "Альфа 12",
        '12',
        staff_unit16_id,
        rank9_id,
        staff_unit16_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position13_id,
        True,
        "1.2.217K",
        True)
    create_user(
        user13_id,
        "Куат",
        "Жанатов",
        'Нурсултанович',
        'kuat@mail.ru',
        group3_id,
        None,
        "Альфа 13",
        '13',
        staff_unit17_id,
        rank5_id,
        staff_unit17_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position24_id,
        True,
        "1.2.217K",
        True)
    create_user(
        user14_id,
        "Даулет",
        "Кайратұлы",
        'Темірбеков',
        'daulet@mail.ru',
        group3_id,
        None,
        "Альфа 14",
        '14',
        staff_unit18_id,
        rank5_id,
        staff_unit18_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position21_id,
        True,
        "1.2.217K",
        True)
    create_user(
        user15_id,
        "Ақжол",
        "Бекмұхаметов",
        'Құдайбергенұлы',
        'akzhol@mail.ru',
        group3_id,
        None,
        "Альфа 15",
        '15',
        staff_unit19_id,
        rank5_id,
        staff_unit19_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position20_id,
        True,
        "1.2.217K",
        True)
    create_user(
        user16_id,
        "Қайрат",
        "Мақсұтұлы",
        'Мұқанов',
        'kairat@mail.ru',
        group3_id,
        None,
        "Альфа 16",
        '16',
        staff_unit20_id,
        rank5_id,
        staff_unit20_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position19_id,
        True,
        "1.2.217K",
        True)
    create_user(
        user17_id,
        "Санжар",
        "Бекжанов",
        'Қуанышбекұлы',
        'sanzhar@mail.ru',
        group3_id,
        None,
        "Альфа 17",
        '17',
        staff_unit21_id,
        rank5_id,
        staff_unit21_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position18_id,
        True,
        "1.2.217K",
        True)
    create_user(
        user18_id,
        "Көктем",
        "Исмаилова",
        None,
        'koktem@mail.ru',
        group3_id,
        None,
        "Альфа 18",
        '18',
        staff_unit22_id,
        rank5_id,
        staff_unit22_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position25_id,
        True,
        "1.2.217K",
        False)
    create_user(
        user19_id,
        "Нейл",
        "Алишев",
        None,
        'alishev@mail.ru',
        group3_id,
        None,
        "Альфа 19",
        '19',
        staff_unit23_id,
        rank5_id,
        staff_unit23_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position25_id,
        True,
        "1.2.217K",
        False)
    create_user(
        user21_id,
        "Батырбек",
        "Бакыткерей",
        None,
        'batyrbek@mail.ru',
        group3_id,
        None,
        "Альфа 21",
        '21',
        staff_unit25_id,
        rank5_id,
        staff_unit25_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position32_id,
        True,
        "1.2.217K",
        False
    )
    create_user(
        admin_user_id,
        "Админ",
        "Админов",
        "Админович",
        'admin@mail.com',
        group3_id,
        None,
        'admin',
        '123456789',
        staff_unit11_id,
        rank3_id,
        staff_unit11_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position4_id,
        False,
        '1.2.100K',
        True)
    create_user(
        user22_id,
        "Касымхан",
        "Тлеуов",
        'Кадырович',
        'kassymkhan@mail.ru',
        group1_id,
        None,
        "Альфа 22",
        '22',
        staff_unit26_id,
        rank13_id,
        staff_unit26_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position12_id,
        True,
        '1.2.27K',
        True)
    create_user(
        user23_id,
        "Бауыржан",
        "Хусаинов",
        'Букенович',
        'b_husainov@sgo.kz',
        group2_id,
        user22_id,
        "Альфа 23",
        '23',
        staff_unit27_id,
        rank10_id,
        staff_unit27_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position13_id,
        True,
        '1.2.216K',
        True)
    create_user(
        user24_id,
        "Дмитрий",
        "Левченко",
        'Валентинович',
        'd_levchenko@sgo.kz',
        group2_1_id,
        user23_id,
        "Альфа 24",
        '24',
        staff_unit28_id,
        rank8_id,
        staff_unit28_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position10_id,
        True,
        '1.2.215K',
        True)
    create_user(
        user25_id,
        "Бейбарыс",
        "Телжанов",
        'Хакимович',
        'beibarys@mail.ru',
        group14_id,
        None,
        "Альфа 25",
        '25',
        staff_unit29_id,
        rank13_id,
        staff_unit29_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position7_id,
        True,
        '1.2.27K',
        True)
    create_user(
        user26_id,
        "Балтабай",
        "Баржаксы",
        'Естиярович',
        'baltabay@mail.ru',
        group15_id,
        user25_id,
        "Альфа 26",
        '26',
        staff_unit30_id,
        rank3_id,
        staff_unit30_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position11_id,
        True,
        '1.2.216K',
        True)
    create_user(
        user27_id,
        "Аскар",
        "Абдурахманов",
        'Куандыкович',
        'askar@mail.ru',
        group16_id,
        user24_id,
        "Альфа 27",
        '27',
        staff_unit31_id,
        rank6_id,
        staff_unit31_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position10_id,
        True,
        '1.2.215K',
        True)
    create_user(
        user28_id,
        "Кайрат",
        "Сарсебаев",
        'Куанышбекович',
        'k_sarsebaev@sgo.kz',
        group15_id,
        user25_id,
        "Альфа 28",
        '28',
        staff_unit32_id,
        rank10_id,
        staff_unit32_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position13_id,
        True,
        '1.2.215K',
        True,
        user26_id)

    create_user(
        user29_id,
        'Ердос',
        'Шалбаев',
        'Елубаевич',
        'e_shalbaev@sgo.kz',
        group1_id,
        None,
        'Семсер-1',
        '29',
        staff_unit34_id,
        rank10_id,
        staff_unit34_id,
        f"{base_s3_url}/static/placeholder.jpg",
        position15_id,
        False,
        'А0415',
        True,
        None
    )

    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit34_id, group1_id))
    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit27_id, group2_id))
    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit28_id, group2_1_id))
    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit2_id, group3_id))
    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit8_id, group4_id))
    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit16_id, group5_id))
    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit10_id, all_service_id))
    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit9_id, group14_id))
    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit32_id, group15_id))
    op.execute("UPDATE staff_divisions SET leader_id = '{}' WHERE id = '{}'".format(
        staff_unit4_id, group16_id))

    op.execute("UPDATE staff_units SET curator_of_id = '{}' WHERE id = '{}'".format(
        group14_id, staff_unit29_id))
    op.execute("UPDATE staff_units SET curator_of_id = '{}' WHERE id = '{}'".format(
        group1_id, staff_unit7_id))

    op.bulk_insert(
        Base.metadata.tables['staff_unit_functions'],
        [{
            'staff_unit_id': staff_unit10_id,
            'staff_function_id': staff_function9_id
        }, {
            'staff_unit_id': staff_unit10_id,
            'staff_function_id': staff_function6_id
        }, {
            'staff_unit_id': staff_unit10_id,
            'staff_function_id': staff_function3_id
        }, {
            'staff_unit_id': staff_unit6_id,
            'staff_function_id': staff_function8_id
        }, {
            'staff_unit_id': staff_unit6_id,
            'staff_function_id': staff_function5_id
        }, {
            'staff_unit_id': staff_unit6_id,
            'staff_function_id': staff_function2_id
        }, {
            'staff_unit_id': staff_unit4_id,
            'staff_function_id': staff_function7_id
        }, {
            'staff_unit_id': staff_unit4_id,
            'staff_function_id': staff_function4_id
        }, {
            'staff_unit_id': staff_unit4_id,
            'staff_function_id': staff_function1_id
        }, {
            'staff_unit_id': staff_unit9_id,
            'staff_function_id': staff_function10_id
        }, {
            'staff_unit_id': staff_unit9_id,
            'staff_function_id': staff_function11_id
        }, {
            'staff_unit_id': staff_unit9_id,
            'staff_function_id': staff_function12_id
        }, {
            'staff_unit_id': staff_unit4_id,
            'staff_function_id': staff_function13_id
        }, {
            'staff_unit_id': staff_unit6_id,
            'staff_function_id': staff_function14_id
        }, {
            'staff_unit_id': staff_unit9_id,
            'staff_function_id': staff_function15_id
        }, {
            'staff_unit_id': staff_unit10_id,
            'staff_function_id': staff_function16_id
        }, {
            'staff_unit_id': staff_unit4_id,
            'staff_function_id': staff_function17_id
        }, {
            'staff_unit_id': staff_unit6_id,
            'staff_function_id': staff_function18_id
        }, {
            'staff_unit_id': staff_unit9_id,
            'staff_function_id': staff_function19_id
        }, {
            'staff_unit_id': staff_unit10_id,
            'staff_function_id': staff_function20_id
        }
        ]
    )

    template4_id = get_uuid()
    template5_id = get_uuid()
    template6_id = get_uuid()
    template7_id = get_uuid()
    template8_id = get_uuid()
    template9_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_document_templates'],
        [{
            'path': '',
            'pathKZ': 'http://193.106.99.68:2287/static/732a700e-d3f5-475c-bfcc-2f5503a101c1.html',
            "description": "",
            'subject_type': 2,
            'properties': {
                'rank': {
                    'alias_nameKZ': 'Лауазым',
                    'data_taken': 'auto',
                    'type': 'write',
                    'field_name': 'rank',
                    'to_tags': {
                        'foundInText': 'Звание',
                        'titleKZ': 'Лауазым',
                        'isHidden': False,
                        'cases': 0
                    }
                },
                'surname': {
                    'alias_nameKZ': 'Тегі',
                    'data_taken': 'auto',
                    'type': 'write',
                    'field_name': 'surname',
                    'to_tags': {
                        'titleKZ': 'Тегі',
                        'isHidden': False
                    }
                },
                'name': {
                    'alias_nameKZ': 'Аты',
                    'data_taken': 'auto',
                    'type': 'write',
                    'field_name': 'name',
                    'to_tags': {
                        'titleKZ': 'Аты',
                        'isHidden': False
                    }
                },
                'father': {
                    'alias_nameKZ': 'Өкесінің аты',
                    'data_taken': 'auto',
                    'type': 'write',
                    'field_name': 'father_name',
                    'to_tags': {
                        'foundInText': 'Отчество субъекта',
                        'titleKZ': 'Өкесінің аты',
                        'isHidden': False,
                        'cases': 0
                    }
                },
                'officer_number': {
                    'alias_nameKZ': 'Офицерлік нөмер',
                    'data_taken': 'auto',
                    'type': 'write',
                    'field_name': 'officer_number',
                    'to_tags': {
                        'titleKZ': 'Офицерлік нөмер',
                        'isHidden': False
                    }
                },
                'new_position': {
                    'to_tags': {
                        'tagname': 'new_position',
                        'isHidden': False,
                        'titleKZ': 'Жаңа позиция',
                        'idToChange': '1687429650307',
                        'id': '1687429650307',
                        'foundInText': '{{new-departament-name-full}} {{new-upravleniye-name-full}} {{new-otdel-name-full}} {{new-gruppa-name-full}} {{new-job-title}} ({{new-category_name}}) ({{new-za-chet-job-title}})',
                        'action_type': ['position_change']
                    },
                    'alias_name': 'Новая должность',
                    'alias_nameKZ': 'Новая должность',
                    'type': 'write',
                    'data_taken': 'dropdown',
                    'field_name': 'staff_unit',
                    'isHidden': False
                },
                'posiiton_name': {
                    'alias_nameKZ': 'Позиция',
                    'data_taken': 'auto',
                    'type': 'write',
                    'field_name': 'position',
                    'to_tags': {
                        'titleKZ': 'Позиция',
                        'isHidden': False
                    }
                },
                'reason': {
                    'to_tags': {
                        'tagname': 'reason',
                        'isHidden': False,
                        'titleKZ': 'Себебі',
                        'idToChange': '1687429650310',
                        'id': '1687429650310',
                        'foundInText': '{{reason-for-percent}}',
                        'action_type': ['position_change']
                    },
                    'alias_name': 'Причина надбавки',
                    'alias_nameKZ': 'Причина надбавки',
                    'type': 'read',
                    'data_taken': 'manual',
                    'data_type': 'string',
                    'isHidden': False
                },
                'percentage': {
                    'to_tags': {
                        'tagname': 'percentage',
                        'isHidden': False,
                        'titleKZ': 'Пайыз',
                        'idToChange': '1687429650311',
                        'id': '1687429650311',
                        'foundInText': False,
                        'action_type': ['position_change']
                    },
                    'alias_name': 'Процент надбавки',
                    'alias_nameKZ': 'Процент надбавки',
                    'type': 'read',
                    'data_taken': 'manual',
                    'data_type': 'number',
                    'isHidden': False
                    }
                },
                'actions': {'args': [
                    {
                        'position_change': {
                            'staff_unit': {
                                'tagname': 'new_position',
                                'alias_name': 'Новая должность',
                                'alias_nameKZ': 'Жаңа қызмет атауы'
                            },
                            'percent': {
                                'tagname': 'percent',
                                'alias_name': 'Процент надбавки',
                                'alias_nameKZ': 'Қосымша пайыз'
                            },
                            'reason': {
                                'tagname': 'reason',
                                'alias_name': 'Причина надбавки',
                                'alias_nameKZ': 'Қосымша пайыздың себебі'
                            }
                        }
                    }
                ]
            },
            'name': 'Приказ о назначении на должность',
            'nameKZ': 'Қызметке тағайындау туралы бұйрық',
            'id': get_uuid(),
            'maintainer_id': staff_unit4_id,
            'is_visible': True
        },{
            'path': '',
            "pathKZ": "http://193.106.99.68:2287/static/498662e9-bc52-40ad-a6ff-2a2649a19bd7.html",
            "description": "",
            'subject_type': 1,
            'properties': {
                        'surname': {
                        'alias_nameKZ': '\u0422\u0435\u0433\u0456',
                        'data_taken': 'auto',
                        'type': 'write',
                        'field_name': 'surname',
                        'to_tags': {
                            'titleKZ': '\u0422\u0435\u0433\u0456',
                            'isHidden': 'false'
                            }
                        },
                        'name': {
                        'alias_nameKZ': '\u0410\u0442\u044b',
                        'data_taken': 'auto',
                        'type': 'write',
                        'field_name': 'name',
                        'to_tags': {
                            'titleKZ': '\u0410\u0442\u044b',
                            'isHidden': False
                            }
                        },
                        'father': {
                            'alias_nameKZ': '\u04d8\u043a\u0435\u0441\u0456\u043d\u0456\u04a3 \u0430\u0442\u044b',
                            'data_taken': 'auto',
                            'type': 'write',
                            'field_name': 'father_name',
                            'to_tags': {
                                'foundInText': '\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0443\u0431\u044a\u0435\u043a\u0442\u0430',

                                'titleKZ': '\u04d8\u043a\u0435\u0441\u0456\u043d\u0456\u04a3 \u0430\u0442\u044b',
                                'isHidden': False,
                                'cases': 0
                            }
                        },
                        'contract': {
                            'to_tags': {
                                'tagname': 'contract',
                                'titleKZ': '\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442',
                                'idToChange': '1687429527959',
                                'id': '1687429527959',
                                'foundInText': '{{contract - term}}',
                                'isHidden': False,
                                'cases': 0,
                                'action_type': '[renew_contract]'
                            },
                            'alias_name': '\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442',
                            'alias_nameKZ': '\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442',
                            'type': 'write',
                            'data_taken': 'dropdown',
                            'field_name': 'contracts',
                            'isHidden': False

                            },
                        'new_rank_name': {
                            'alias_nameKZ': '\u0416\u0430\u04a3\u0430 \u043b\u0430\u0443\u0430\u0437\u044b\u043c',
                            'data_taken': 'dropdown',
                            'type': 'write',
                            'field_name': 'rank',
                            'to_tags': {
                                'titleKZ': '\u0416\u0430\u04a3\u0430 \u043b\u0430\u0443\u0430\u0437\u044b\u043c',
                                'directory': 'rank',
                                'isHidden': 'false'}
                        },
                        'new_position': {
                            'alias_nameKZ': '\u0416\u0430\u04a3\u0430 \u043f\u043e\u0437\u0438\u0446\u0438\u044f',
                            'data_taken': 'dropdown',
                            'type': 'write',
                            'field_name': 'staff_unit',
                            'to_tags': {
                                'titleKZ': '\u0416\u0430\u04a3\u0430 \u043f\u043e\u0437\u0438\u0446\u0438\u044f',
                                'directory': 'staff_unit',
                                'isHidden': 'false'}
                            }
            },
            'actions': {'args': [
                {
                    'renew_contract': {
                        'contract': {
                            'tagname': 'contract_type',
                            'alias_name': '\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442',
                            'alias_nameKZ': '\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442'
                        }
                    }
                }
            ]
            },
            'name': 'Приказ о зачислении на службу сотрудника',
            'nameKZ': 'Қызметкерді қызметке қабылдау бұйрығы',
            'id': get_uuid(),
            'maintainer_id': staff_unit4_id,
            'is_visible': True
        },
        {
            "name": "Запрос на наличие сведений для указанных граждан о причастности к религиозному экстремизму",
            "nameKZ": "Көрсетілген азаматтар үшін діни экстремизмге қатысы бар екендігі туралы мәліметтердің болуына сұрау салу",
            "path": f"{base_s3_url}/static/кандидаты1.html",
            "pathKZ": f"{base_s3_url}/static/кандидаты1.html",
            "subject_type": 1,
            'description': "",
            'maintainer_id': staff_unit4_id,
            'is_visible': False,
            "properties": {
                "recipient.organization_name": {
                    "alias_name": "Наименование ссылаемой организации",
                    "type": "read",
                    "data_taken": "manual"
                },
                "recipient.position": {
                    "alias_name": "Позиция ссылаемого челевека",
                    "type": "read",
                    "data_taken": "manual"
                },
                "recipient.rank": {
                    "alias_name": "Звание ссылаемого челевека",
                    "type": "read",
                    "data_taken": "manual"
                },
                "recipient.name": {
                    "alias_name": "Имя ссылаемого челевека",
                    "type": "read",
                    "data_taken": "manual"
                },
                "recipient.father_name": {
                    "alias_name": "Отчество ссылаемого челевека",
                    "type": "read",
                    "data_taken": "manual"
                },
                "recipient.surname": {
                    "alias_name": "Фамилия ссылаемого челевека",
                    "type": "read",
                    "data_taken": "manual"
                },
                "recipient.city": {
                    "alias_name": "Город ссылаемой организации",
                    "type": "read",
                    "data_taken": "manual"
                },
                "candidate.surname": {
                    "alias_name": "Фамилия кандидата",
                    "type": "read",
                    "data_taken": "auto"
                },
                "candidate.name": {
                    "alias_name": "Имя кандидата",
                    "type": "read",
                    "data_taken": "auto"
                },
                "candidate.father_name": {
                    "alias_name": "Отчество кандидата",
                    "type": "read",
                    "data_taken": "auto"
                },
                "candidate.IIN": {
                    "alias_name": "ИИН кандидата",
                    "type": "read",
                    "data_taken": "auto"
                },
                "candidate.birth_date": {
                    "alias_name": "Дата рождения кандидата",
                    "type": "read",
                    "data_taken": "auto"
                },
                "candidate.birth_place": {
                    "alias_name": "Место рождения кандидата",
                    "type": "read",
                    "data_taken": "auto"
                },
                "candidate.nationality": {
                    "alias_name": "Национальность кандидата",
                    "type": "read",
                    "data_taken": "auto"
                },
                "candidate.residence_address": {
                    "alias_name": "Место жительство кандидата",
                    "type": "read",
                    "data_taken": "auto"
                },
                "check_information": {
                    "alias_name": "Запрошенная информация для проверки",
                    "type": "read",
                    "data_taken": "manual"
                },
                "approving.position": {
                    "alias_name": "Позиция куратора",
                    "type": "read",
                    "data_taken": "auto"
                },
                "approving.rank": {
                    "alias_name": "Звание куратора",
                    "type": "read",
                    "data_taken": "auto"
                },
                "approving.surname": {
                    "alias_name": "Фамилия куратора",
                    "type": "read",
                    "data_taken": "auto"
                },
                "approving.name": {
                    "alias_name": "Имя куратора",
                    "type": "read",
                    "data_taken": "auto"
                },
                "approving.father_name": {
                    "alias_name": "Отчество куратора",
                    "type": "read",
                    "data_taken": "auto"
                },
                "date_of_signature": {
                    "alias_name": "Дата подписания",
                    "type": "read",
                    "data_taken": "auto"
                }
            }, 'actions': {'args': [

            ]},
            'id': template4_id
        },
            {
                "name": "Заключение спец. проверки",
                "nameKZ": "Арнайы қорытынды тексерулер",
                "path": f"{base_s3_url}/static/pre-finalv2.html",
                "pathKZ": f"{base_s3_url}/static/pre-finalv2.html",
                "subject_type": 1,
                'description': "",
                'is_visible': False,
                'maintainer_id': staff_unit4_id,
                "properties": {
                    "curator.rank.name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "curator.first_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "curator.father_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "curator.last_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "year": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "day": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "month": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "candidate.rank.name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "candidate.first_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "candidate.father_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "candidate.last_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "candidate.date_birth": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "candidate.profile.personal_profile.biographic_info.place_birth": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "candidate.profile.personal_profile.biographic_info.nationality": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "candidate.address": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "father.first_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "father.father_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "father.last_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "father.iin": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "father.date_birth": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "father.place_birth": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "father.workplace": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "father.address": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "curator.staff_unit.position.name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "curator.staff_unit.staff_division.name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "mother.first_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "mother.father_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "mother.last_name": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "mother.iin": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "mother.date_birth": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "mother.place_birth": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "mother.workplace": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    },
                    "mother.address": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    }
                }, 'actions': {'args': [

                ]},
                'id': template5_id
        },
            {
                "name": "Заключение на зачисление",
                "nameKZ": "Қабылдау қорытындысы",
                "path": None,
                "pathKZ": f"{base_s3_url}/static/finish_candidate.html",
                "subject_type": 1,
                'maintainer_id': staff_unit4_id,
                'description': "",
                'is_visible': False,
                "properties": {
                    "example": {
                        "alias_name": "Звание куратора",
                        "type": "read",
                        "data_taken": "auto"
                    }
                },
                'actions': {'args': [

                ]},
                'id': template6_id
        }, {
            "name": "Приказ об изменении штатного расписания",
            "nameKZ": "Штат кестесін өзгерту туралы бұйрық",
            "path": None,
            "pathKZ": None,
            "subject_type": None,
            'maintainer_id': None,
            'description': "",
            'is_visible': False,
            "properties": {
                "staff_list": {
                    'alias_name': 'Штатное расписание',
                    'alias_nameKZ': 'Штат кестесі',
                    'type': 'write',
                    'data_taken': "dropdown",
                    'field_name': ""
                }
            },
            'actions': {'args': [
                {
                    'superdoc': {},
                }, {
                    'apply_staff_list': {
                        'staff_list': {
                            'tagname': 'staff_list'
                        }
                    }
                }
            ]},
            'id': template7_id
        }, {
            'name': "Супер документ",
            'nameKZ': "Супер құжат",
            'path': None,
            'pathKZ': None,
            'subject_type': None,
            'maintainer_id': None,
            'description': "",
            'is_visible': False,
            'properties': {},
            'actions': {'args': [
                {
                    'superdoc': {}
                }
            ]},
            'id': template8_id
        }, {
            'name': "Приказ о назначении на должность (штатное расписание)",
            'nameKZ': "Штат кестесіне байланысты есепке алу туралы бұйрық (Штат кестесіне байланысты есепке алу туралы бұйрық)",
            'path': None,
            'pathKZ': None,
            'subject_type': 'EMPLOYEE',
            'maintainer_id': None,
            'description': "",
            'is_visible': False,
            'properties': {
                'staff_unit': {
                    'alias_name': 'Позиция сотрудника',
                    'data_taken': 'dropdown',
                    'type': 'write',
                    'field_name': 'staff_unit'
                }
            },
            'actions': {'args': [

            ]},
            'id': template9_id
        }]
    )

    step4_1 = get_uuid()
    step4_2 = get_uuid()
    step4_3 = get_uuid()
    step4_4 = get_uuid()
    step5_1 = get_uuid()
    step5_2 = get_uuid()
    step5_3 = get_uuid()
    step5_4 = get_uuid()
    step6_1 = get_uuid()
    step6_2 = get_uuid()
    step6_3 = get_uuid()
    step6_4 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_document_steps'],
        [{
            'hr_document_template_id': template7_id,
            'previous_step_id': None,
            'staff_function_id': staff_function13_id,
            'id': step4_1
        }, {
            'hr_document_template_id': template7_id,
            'previous_step_id': step4_1,
            'staff_function_id': staff_function14_id,
            'id': step4_2
        }, {
            'hr_document_template_id': template7_id,
            'previous_step_id': step4_2,
            'staff_function_id': staff_function15_id,
            'id': step4_3
        }, {
            'hr_document_template_id': template7_id,
            'previous_step_id': step4_3,
            'staff_function_id': staff_function16_id,
            'id': step4_4
        }, {
            'hr_document_template_id': template8_id,
            'previous_step_id': None,
            'staff_function_id': staff_function4_id,
            'id': step5_1
        }, {
            'hr_document_template_id': template8_id,
            'previous_step_id': step5_1,
            'staff_function_id': staff_function5_id,
            'id': step5_2
        }, {
            'hr_document_template_id': template8_id,
            'previous_step_id': step5_2,
            'staff_function_id': staff_function10_id,
            'id': step5_3
        }, {
            'hr_document_template_id': template8_id,
            'previous_step_id': step5_2,
            'staff_function_id': staff_function6_id,
            'id': step5_4
        }, {
            'hr_document_template_id': template9_id,
            'previous_step_id': None,
            'staff_function_id': staff_function17_id,
            'id': step6_1
        }, {
            'hr_document_template_id': template9_id,
            'previous_step_id': step6_1,
            'staff_function_id': staff_function18_id,
            'id': step6_2
        }, {
            'hr_document_template_id': template9_id,
            'previous_step_id': step6_2,
            'staff_function_id': staff_function19_id,
            'id': step6_3
        }, {
            'hr_document_template_id': template9_id,
            'previous_step_id': step6_3,
            'staff_function_id': staff_function20_id,
            'id': step6_4
        }]
    )

    candidate_id = get_uuid()
    candidate2_id = get_uuid()
    candidate3_id = get_uuid()
    candidate4_id = get_uuid()
    candidate5_id = get_uuid()
    candidate6_id = get_uuid()
    candidate7_id = get_uuid()
    candidate8_id = get_uuid()
    candidate9_id = get_uuid()
    candidate10_id = get_uuid()
    candidate11_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['candidates'],
        [{
            'id': candidate_id,
            'staff_unit_id': staff_unit1_id,
            'staff_unit_curator_id': staff_unit11_id,
            'status': 'ACTIVE',
            'debarment_reason': None
        }, {
            'id': candidate2_id,
            'staff_unit_id': staff_unit2_id,
            'staff_unit_curator_id': staff_unit11_id,
            'status': 'ACTIVE',
            'debarment_reason': None
        }, {
            'id': candidate3_id,
            'staff_unit_id': staff_unit3_id,
            'staff_unit_curator_id': staff_unit11_id,
            'status': 'ACTIVE',
            'debarment_reason': None
        }, {
            'id': candidate4_id,
            'staff_unit_id': staff_unit5_id,
            'staff_unit_curator_id': staff_unit11_id,
            'status': 'ACTIVE',
            'debarment_reason': None
        }, {
            'id': candidate5_id,
            'staff_unit_id': staff_unit7_id,
            'staff_unit_curator_id': staff_unit11_id,
            'status': 'ACTIVE',
            'debarment_reason': None
        }, {
            'id': candidate6_id,
            'staff_unit_id': staff_unit8_id,
            'staff_unit_curator_id': staff_unit11_id,
            'status': 'ACTIVE',
            'debarment_reason': None
        }, {
            'id': candidate7_id,
            'staff_unit_id': staff_unit9_id,
            'staff_unit_curator_id': staff_unit11_id,
            'status': 'DRAFT',
            'debarment_reason': 'Недостаточный уровень квалификации: кандидат не соответствует необходимым требованиям по опыту и навыкам для данной вакансии'
        }, {
            'id': candidate8_id,
            'staff_unit_id': staff_unit1_id,
            'staff_unit_curator_id': staff_unit10_id,
            'status': 'ACTIVE',
            'debarment_reason': None
        }, {
            'id': candidate9_id,
            'staff_unit_id': staff_unit1_id,
            'staff_unit_curator_id': staff_unit10_id,
            'status': 'ACTIVE',
            'debarment_reason': None
        }, {
            'id': candidate10_id,
            'staff_unit_id': staff_unit1_id,
            'staff_unit_curator_id': staff_unit10_id,
            'status': 'DRAFT',
            'debarment_reason': 'Недостаточное количество опыта: кандидат не имеет достаточного опыта работы в данной области или на аналогичной должности'
        }, {
            'id': candidate11_id,
            'staff_unit_id': staff_unit1_id,
            'staff_unit_curator_id': staff_unit10_id,
            'status': 'DRAFT',
            'debarment_reason': 'Нарушение правил: кандидат нарушил правила собеседования или требования к вакансии.'
        }]
    )

    penalty_type_id = get_uuid()
    penalty_type2_id = get_uuid()
    penalty_type3_id = get_uuid()
    penalty_type4_id = get_uuid()
    penalty_type5_id = get_uuid()
    penalty_type6_id = get_uuid()
    penalty_type7_id = get_uuid()
    penalty_type8_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['penalty_types'],
        [{
            'id': penalty_type_id,
            'name': 'Замечание',
            'nameKZ': 'Ескерту',
        },
            {
                'id': penalty_type2_id,
                'name': 'Выговор',
                'nameKZ': 'Сөгіс'
        },
            {
                'id': penalty_type3_id,
                'name': 'Строгий выговор',
                'nameKZ': 'Қатаң сөгіс'
        },
            {
                'id': penalty_type4_id,
                'name': 'Предупреждение о неполном служебном соответствии',
                'nameKZ': 'Толық қызметтік сәйкестікті қателіктен басқа құлақтандыру'
        },
            {
                'id': penalty_type5_id,
                'name': 'Увольнение со службы по отрицательным мотивам',
                'nameKZ': 'Теріс себептермен қызметтен босату'
        },
            {
                'id': penalty_type6_id,
                'name': 'Снижение воинского звания',
                'nameKZ': 'Әскери атағын төмендету'
        },
            {
                'id': penalty_type7_id,
                'name': 'Неполное служебное соответствие',
                'nameKZ': 'Толық емес қызметтік сәйкестік'

        },
            {
                'id': penalty_type8_id,
                'name': 'Письменное предупреждение',
                'nameKZ': 'Жазбаша ескерту'
        }]
    )

    penalty_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['penalties'],
        [{
            'id': penalty_id,
            'type_id': penalty_type_id,
            'user_id': user1_id,
        }]
    )

    badge_id = get_uuid()
    badge1_1_id = get_uuid()
    badge1_2_id = get_uuid()
    badge1_3_id = get_uuid()

    badge2_1_id = get_uuid()
    badge2_2_id = get_uuid()
    badge2_3_id = get_uuid()

    badge3_1_id = get_uuid()
    badge3_2_id = get_uuid()
    badge3_3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['badges'],
        [{
            'id': badge_id,
            'user_id': user1_id,
            'type_id': badgetype1_id
        }, {
            'id': badge1_1_id,
            'user_id': user1_id,
            'type_id': badgetype3_id
        }, {
            'id': badge1_2_id,
            'user_id': user1_id,
            'type_id': badgetype4_id
        }, {
            'id': badge1_3_id,
            'user_id': user1_id,
            'type_id': badgetype5_id
        }, {
            'id': badge2_1_id,
            'user_id': user2_id,
            'type_id': badgetype4_id
        }, {
            'id': badge2_2_id,
            'user_id': user2_id,
            'type_id': badgetype5_id
        }, {
            'id': badge2_3_id,
            'user_id': user2_id,
            'type_id': badgetype6_id
        }, {
            'id': badge3_1_id,
            'user_id': user3_id,
            'type_id': badgetype3_id
        }, {
            'id': badge3_2_id,
            'user_id': user3_id,
            'type_id': badgetype4_id
        }, {
            'id': badge3_3_id,
            'user_id': user3_id,
            'type_id': badgetype6_id
        }, ]
    )

    type_army_equipment_id = get_uuid()
    type_army_equipment2_id = get_uuid()
    type_army_equipment3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['type_army_equipments'],
        [{
            'id': type_army_equipment_id,
            'name': 'Автомат',
            'nameKZ': 'Автомат',
        },
            {
                'id': type_army_equipment2_id,
                'name': 'РПГ',
                'nameKZ': 'РПГ',
        },
            {
                'id': type_army_equipment3_id,
                'name': 'Артиллерия',
                'nameKZ': 'Артиллерия',
        }
        ])

    type_army_equipment_model_id = get_uuid()
    type_army_equipment_model2_id = get_uuid()
    type_army_equipment_model3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['type_army_equipment_models'],
        [{
            'id': type_army_equipment_model_id,
            'name': 'AK-74',
            'nameKZ': 'AK-74',
            'type_of_army_equipment_id': type_army_equipment_id
        },
            {
                'id': type_army_equipment_model2_id,
                'name': 'Автомат пулемет',
                'nameKZ': "Автомат пулемет",
                'type_of_army_equipment_id': type_army_equipment_id
        },
            {
                'id': type_army_equipment_model3_id,
                'name': 'Автомат пулемет',
                'nameKZ': "Автомат пулемет",
                'type_of_army_equipment_id': type_army_equipment_id
        }]
    )

    type_of_clothing_equipment_id = get_uuid()
    type_of_clothing_equipment2_id = get_uuid()
    type_of_clothing_equipment3_id = get_uuid()
    type_of_clothing_equipment4_id = get_uuid()
    type_of_clothing_equipment5_id = get_uuid()
    type_of_clothing_equipment6_id = get_uuid()
    type_of_clothing_equipment7_id = get_uuid()
    type_of_clothing_equipment8_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['type_clothing_equipments'],
        [{
            'id': type_of_clothing_equipment_id,
            'name': 'Шапка',
            'nameKZ': 'Бас киім'
        },
            {
                'id': type_of_clothing_equipment2_id,
                'name': 'Куртка',
                'nameKZ': 'Пиджак'
        },
            {
                'id': type_of_clothing_equipment3_id,
                'name': 'Футболка',
                'nameKZ': 'Футболка'
        },
            {
                'id': type_of_clothing_equipment4_id,
                'name': 'Кофта',
                'nameKZ': 'Жейде'
        },
            {
                'id': type_of_clothing_equipment5_id,
                'name': 'Штаны',
                'nameKZ': 'Шалбар'
        },
            {
                'id': type_of_clothing_equipment6_id,
                'name': 'Термобелье',
                'nameKZ': 'Термиялық іш киім',
        },
            {
                'id': type_of_clothing_equipment7_id,
                'name': 'Ботинки',
                'nameKZ': 'Етік',
        },
            {
                'id': type_of_clothing_equipment8_id,
                'name': 'Носки',
                'nameKZ': 'Шұлық'
        }])

    type_of_clothing_equipment_model_id = get_uuid()
    type_of_clothing_equipment_model2_id = get_uuid()
    type_of_clothing_equipment_model3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['type_clothing_equipment_models'],
        [{
            'id': type_of_clothing_equipment_model_id,
            'name': 'Военная',
            'nameKZ': 'Әскери',
            'type_of_clothing_equipment_id': type_of_clothing_equipment_id
        },
            {
                'id': type_of_clothing_equipment_model2_id,
                'name': 'Тактическая',
                'nameKZ': 'Тактикалық',
                'type_of_clothing_equipment_id': type_of_clothing_equipment2_id
        },
            {
                'id': type_of_clothing_equipment_model3_id,
                'name': 'Парадная',
                'nameKZ': 'Салтанатты',
                'type_of_clothing_equipment_id': type_of_clothing_equipment3_id
        },
        ])

    clothing_equipment_types_model_id = get_uuid()
    clothing_equipment_types_model2_id = get_uuid()
    clothing_equipment_types_model3_id = get_uuid()
    clothing_equipment_types_model4_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['clothing_equipment_types_models'],
        [{
            'id': clothing_equipment_types_model_id,
            'type_clothing_equipments_id': type_of_clothing_equipment_id,
            'type_clothing_equipment_models_id': type_of_clothing_equipment_model_id
        },
            {
                'id': clothing_equipment_types_model2_id,
                'type_clothing_equipments_id': type_of_clothing_equipment2_id,
                'type_clothing_equipment_models_id': type_of_clothing_equipment_model_id
        },
            {
                'id': clothing_equipment_types_model3_id,
                'type_clothing_equipments_id': type_of_clothing_equipment2_id,
                'type_clothing_equipment_models_id': type_of_clothing_equipment_model2_id
        },
            {
                'id': clothing_equipment_types_model4_id,
                'type_clothing_equipments_id': type_of_clothing_equipment_id,
                'type_clothing_equipment_models_id': type_of_clothing_equipment_model2_id
        },
        ])

    type_other_equipment_id = get_uuid()
    type_other_equipment2_id = get_uuid()
    op.bulk_insert(
        Base.metadata.tables['type_other_equipments'],
        [{
            'id': type_other_equipment_id,
            'name': 'Принтер',
            'nameKZ': 'Принтер'
        },
            {
                'id': type_other_equipment2_id,
                'name': 'Телефон',
                'nameKZ': 'Телефон'
        }]
    )

    type_other_equipment_model_id = get_uuid()
    type_other_equipment_model2_id = get_uuid()
    type_other_equipment_model3_id = get_uuid()
    type_other_equipment_model4_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['type_other_equipment_models'],
        [{
            'id': type_other_equipment_model_id,
            'name': 'HP LaserJet N7100',
            'nameKZ': 'HP LaserJet N7100',
            'type_of_other_equipment_id': type_other_equipment_id
        },
            {
                'id': type_other_equipment_model2_id,
                'name': 'HP LaserJet P1102',
                'nameKZ': 'HP LaserJet P1102',
                'type_of_other_equipment_id': type_other_equipment_id
        },
            {
                'id': type_other_equipment_model3_id,
                'name': 'Mitel 6865',
                'nameKZ': 'Mitel 6865',
                'type_of_other_equipment_id': type_other_equipment2_id
        },
            {
                'id': type_other_equipment_model4_id,
                'name': 'Mitel 5304',
                'nameKZ': 'Mitel 5304',
                'type_of_other_equipment_id': type_other_equipment2_id
        }
        ])

    army_equipment_id = get_uuid()
    clothing_equipment_id = get_uuid()
    clothing_equipment2_id = get_uuid()
    clothing_equipment3_id = get_uuid()
    clothing_equipment4_id = get_uuid()
    other_equipment_id = get_uuid()
    other_equipment2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['equipments'],
        [{
            'id': army_equipment_id,
            'type_of_army_equipment_model_id': type_army_equipment_model_id,
            'count_of_ammo': 100,
            'inventory_number': '123456789',
            'inventory_count': 1,
            'clothing_size': None,
            'user_id': user1_id,
            'type_of_equipment': 'army_equipment',
            'clothing_equipment_types_models_id': None,
            'type_of_other_equipment_model_id': None,
            'document_link': f'{base_s3_url}/static/example.txt',
            'document_number': '123456789',
            'date_from': '2023-04-11T19:43:02.556000',
            'date_to': None,
        },
            {
                'id': clothing_equipment_id,
                'clothing_equipment_types_models_id': clothing_equipment_types_model_id,
                'user_id': user1_id,
                'type_of_equipment': 'clothing_equipment',
                'count_of_ammo': None,
                'inventory_number': '123456789',
                'inventory_count': None,
                'clothing_size': '56',
                'type_of_army_equipment_model_id': None,
                'type_of_other_equipment_model_id': None,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '123456789',
                'date_from': '2023-04-11T19:43:02.556000',
                'date_to': None,
        },
            {
                'id': clothing_equipment2_id,
                'clothing_equipment_types_models_id': clothing_equipment_types_model2_id,
                'user_id': user1_id,
                'type_of_equipment': 'clothing_equipment',
                'count_of_ammo': None,
                'inventory_number': '64718248',
                'inventory_count': None,
                'clothing_size': '56',
                'type_of_army_equipment_model_id': None,
                'type_of_other_equipment_model_id': None,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '123456789',
                'date_from': '2023-04-11T19:43:02.556000',
                'date_to': None,
        },
            {
                'id': clothing_equipment3_id,
                'clothing_equipment_types_models_id': clothing_equipment_types_model3_id,
                'user_id': user1_id,
                'type_of_equipment': 'clothing_equipment',
                'count_of_ammo': None,
                'inventory_number': '159815617',
                'inventory_count': None,
                'clothing_size': '56',
                'type_of_army_equipment_model_id': None,
                'type_of_other_equipment_model_id': None,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '123456789',
                'date_from': '2023-04-11T19:43:02.556000',
                'date_to': None,
        },
            {
                'id': clothing_equipment4_id,
                'clothing_equipment_types_models_id': clothing_equipment_types_model4_id,
                'user_id': user1_id,
                'type_of_equipment': 'clothing_equipment',
                'count_of_ammo': None,
                'inventory_number': '637041620',
                'inventory_count': None,
                'clothing_size': '56',
                'type_of_army_equipment_model_id': None,
                'type_of_other_equipment_model_id': None,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '123456789',
                'date_from': '2023-04-11T19:43:02.556000',
                'date_to': None,
        },
            {
                'id': other_equipment_id,
                'type_of_other_equipment_model_id': type_other_equipment_model_id,
                'user_id': user1_id,
                'type_of_equipment': 'other_equipment',
                'count_of_ammo': None,
                'inventory_number': '987456123',
                'inventory_count': 1,
                'clothing_size': None,
                'type_of_army_equipment_model_id': None,
                'clothing_equipment_types_models_id': None,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '123456789',
                'date_from': '2023-04-11T19:43:02.556000',
                'date_to': None,
        },
            {
                'id': other_equipment2_id,
                'type_of_other_equipment_model_id': type_other_equipment_model3_id,
                'user_id': user1_id,
                'type_of_equipment': 'other_equipment',
                'count_of_ammo': None,
                'inventory_number': '1721581041',
                'inventory_count': 1,
                'clothing_size': None,
                'type_of_army_equipment_model_id': None,
                'clothing_equipment_types_models_id': None,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '123456789',
                'date_from': '2023-04-11T19:43:02.556000',
                'date_to': None,
        }
        ])

    secondment_id = get_uuid()
    secondment2_id = get_uuid()
    secondment3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['secondments'],
        [{
            'id': secondment_id,
            'staff_division_id': group1_id,
            'user_id': user1_id,
            'name': 'Перевод в другую группу',
            'nameKZ': 'Басқа топқа өткізу'
        },
            {
                'id': secondment2_id,
                'staff_division_id': group2_id,
                'user_id': user1_id,
                'name': 'Перевод в другую группу',
                'nameKZ': 'Басқа топқа өткізу'
        },
            {
                'id': secondment3_id,
                'staff_division_id': group3_id,
                'user_id': user1_id,
                'name': 'Перевод в другую группу',
                'nameKZ': 'Басқа топқа өткізу'
        }]
    )

    name_change_id = get_uuid()
    name_change2_id = get_uuid()
    name_change3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['name_changes'],
        [{
            'id': name_change_id,
            'name_before': 'Иван',
            'name_after': 'Петр',
            'name_type': 'name'
        },
            {
                'id': name_change2_id,
                'name_before': 'Петр',
                'name_after': 'Самат',
                'name_type': 'name'
        },
            {
                'id': name_change3_id,
                'name_before': 'Иванов',
                'name_after': 'Петров',
                'name_type': 'surname'
        }]
    )

    attestation_id = get_uuid()
    attestation2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['attestations'],
        [{
            'id': attestation_id,
            'user_id': user1_id,
        }]
    )

    status_type = get_uuid()
    status_type2 = get_uuid()
    status_type3 = get_uuid()
    status_type4 = get_uuid()
    status_type5 = get_uuid()
    status_type6 = get_uuid()
    status_type7 = get_uuid()
    status_type8 = get_uuid()
    status_type9 = get_uuid()
    status_type10 = get_uuid()
    status_type11 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['status_types'],
        [{
            'id': status_type,
            'name': 'На работе',
            'nameKZ': 'Жұмыста'
        },
            {
            'id': status_type2,
            'name': 'В отпуске',
            'nameKZ': 'Демалыста'
        },
            {
            'id': status_type3,
            'name': "Умер",
            'nameKZ': 'Қайтыс болды'
        },
            {
            'id': status_type4,
            'name': "В отставке",
            'nameKZ': 'Қызметін доғарды'
        },
            {
            'id': status_type5,
            'name': "В запасе",
            'nameKZ': 'Резервте'
        },
            {
            'id': status_type6,
            'name': "Исключен из списков личного состава",
            'nameKZ': 'Кадрлар тізімінен шығарылған'
        },
            {
            'id': status_type7,
            'name': "Откомандирован в другой гос. орган",
            'nameKZ': 'Басқа мемлекеттік органға жіберілді'
        },
            {
            'id': status_type8,
            'name': "Погиб",
            'nameKZ': 'Қайтыс болды'
        }, {
            'id': status_type9,
            'name': "В отпуске по беременности и родам",
            'nameKZ': 'Жүктілік және босану демалысында'
        }, {
            'id': status_type10,
            'name': "В отпуске по болезни",
            'nameKZ': 'Аурулардың демалысында'
        }, {
            'id': status_type11,
            'name': "Ежегодный отпуск",
            'nameKZ': 'Жылдық демалыс',
        }]
    )

    coolness_type_id = get_uuid()
    coolness_type2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['coolness_types'],
        [{
            'id': coolness_type_id,
            'name': "Специалист I класса",
            'nameKZ': 'I сыныпты маман',
            'order': 1
        },
            {
            'id': coolness_type2_id,
            'name': 'Специалист 2 класса',
            'nameKZ': '2-сынып маманы',
            'order': 2
        },
        ]
    )

    coolness_id = get_uuid()
    coolness2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['coolnesses'],
        [{
            'id': coolness_id,
            'type_id': coolness_type_id,
            'user_id': user1_id,
        },
            {
                'id': coolness2_id,
                'type_id': coolness_type2_id,
                'user_id': user1_id,
        },
        ]
    )

    contract_type_id = get_uuid()
    contract_type2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['contract_types'],
        [{
            'id': contract_type_id,
            'name': 'Контракт на 2 года',
            'nameKZ': '2 жылға арналған келісімшарт',
            'years': 2,
            'is_finite': True
        }, {
            'id': contract_type2_id,
            'name': 'Контракт на неопределенный срок',
            'nameKZ': 'Белгісіз мерзімге келісімшарт',
            'years': -1,
            'is_finite': False
        }]
    )

    contract_id = get_uuid()
    contract2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['contracts'],
        [{
            'id': contract_id,
            'type_id': contract_type_id,
            'user_id': user1_id,
        },
            {
                'id': contract2_id,
                'type_id': contract_type2_id,
                'user_id': user1_id,
        },
        ]
    )

    history_id = get_uuid()
    history2_id = get_uuid()
    history3_id = get_uuid()
    history6_id = get_uuid()
    history7_id = get_uuid()
    history8_id = get_uuid()
    history10_id = get_uuid()
    history11_id = get_uuid()
    history12_id = get_uuid()
    history13_id = get_uuid()
    history14_id = get_uuid()
    history15_id = get_uuid()
    history16_id = get_uuid()
    history17_id = get_uuid()

    history18_id = get_uuid()
    history19_id = get_uuid()
    history20_id = get_uuid()
    history21_id = get_uuid()
    history22_id = get_uuid()
    history23_id = get_uuid()
    history24_id = get_uuid()
    history25_id = get_uuid()
    history26_id = get_uuid()
    history27_id = get_uuid()

    military_unit_id = get_uuid()
    military_unit2_id = get_uuid()
    military_unit3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['military_units'],
        [{
            'id': military_unit_id,
            'name': 'Военная часть 1',
            'nameKZ': 'Әскери бөлім 1',
        },
            {
                'id': military_unit2_id,
                'name': 'Военная часть 2',
                'nameKZ': 'Әскери бөлім 2',
        },
            {
                'id': military_unit3_id,
                'name': 'Военная часть 3',
                'nameKZ': 'Әскери бөлім 3',
        },
        ]
    )

    oauth_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['user_oaths'],
        [{
            'id': oauth_id,
            'date': datetime.datetime.now(),
            'user_id': user1_id,
            'military_unit_id': military_unit_id,
        }])

    privelege_emergency_service_id = get_uuid()
    privelege_emergency_service2_id = get_uuid()

    from models import FormEnum

    op.bulk_insert(
        Base.metadata.tables['privelege_emergencies'],
        [{
            'id': privelege_emergency_service_id,
            'form': 'form1',
            'date_from': datetime.datetime.now(),
            'date_to': datetime.datetime.now() + datetime.timedelta(days=1),
            'user_id': user1_id,
        }
        ]
    )

    personnel_reserve_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['personnal_reserves'],
        [{
            'id': personnel_reserve_id,
            'reserve': 'enlisted',
            'date_from': datetime.datetime.now() - datetime.timedelta(days=365),
            'date_to': datetime.datetime.now() + datetime.timedelta(days=365),
            'user_id': user1_id,
            'document_link': f'{base_s3_url}/static/example.txt',
            'document_number': '№ 59124',
        },
        ]
    )

    service_id_info_id = get_uuid()
    service_id_info2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['service_ids'],
        [{
            'id': service_id_info_id,
            'number': '№ 59124',
            'date_to': datetime.datetime.now() + datetime.timedelta(days=365),
            'token_status': 'RECEIVED',
            'id_status': 'RECEIVED',
            'user_id': user1_id,
        },
        ])

    op.bulk_insert(
        Base.metadata.tables['histories'],
        [
            {
                'id': history17_id,  # TODO: change the id
                'date_from': datetime.datetime(2012, 3, 1),
                'date_to': datetime.datetime(2014, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': 'badge_history',
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # МЕНЯТЬ НА name_change_id
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # Add the missing parameter here
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'badge_id': badge_id,
                'name_of_organization': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history14_id,
                'date_from': datetime.datetime(2012, 3, 1),
                'date_to': datetime.datetime(2015, 3, 12),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': 'emergency_history',
                'penalty_id': None,
                'name': '18 history',
                'position_id': position4_id,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                # Add the missing parameter here
                'emergency_service_id': privelege_emergency_service_id,
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # МЕНЯТЬ НА name_change_id
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # Add the missing parameter here
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': 1.0,
                'percentage': 50,
                'staff_division_id': group3_id,
                'badge_id': None,
                'name_of_organization': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': rank4_id,
                'contractor_signer_name': "Начальник Службы",
                'contractor_signer_nameKZ': "Қызмет бастығы",
            },
            # {
            #     'id': history14_id,
            #     'date_from': str(datetime.datetime(2019, 2, 1)),
            #     'date_to': str(datetime.datetime(2019, 2, 28)),
            #     'user_id': user1_id,
            #     'document_link': f'{base_s3_url}/static/example.txt',
            #     'document_number': '№ 59124',
            #     'type': type_of_histories[3],
            #     'rank_id': None,  # Add the missing parameter here
            #     'name': '2 history',
            #     'position_id': None,  # Add the missing parameter here
            #     'penalty_id': None,  # Add the missing parameter here
            #     'emergency_service_id': None,  # Add the missing parameter here
            #     'work_experience_id': None,  # Add the missing parameter here
            #     'secondment_id': None,  # Add the missing parameter here
            #     'name_change_id': None,  # Add the missing parameter here
            #     'attestation_id': None,  # Add the missing parameter here
            #     'service_characteristic_id': None,  # Add the missing parameter here
            #     'status_id': None,  # Add the missing parameter here
            #     'coolness_id': None,  # Add the missing parameter here
            #     'contract_id': None,  # Add the missing parameter here
            #     'attestation_status': None,  # МЕНЯТЬ НА attestation_status
            #     'experience_years': None,  # Add the missing parameter here
            #     'characteristic_initiator_id': None,  # Add the missing parameter here
            #     'coefficient' : 1.5,
            #     'percentage' : 10,
            #     'staff_division_id' : group1_id,
            #     'nabadge_id': None,
            #     'id': history2_id,
            #     'date_from': str(datetime.datetime(2019, 2, 1)),
            #     'date_to': str(datetime.datetime(2019, 2, 28)),
            #     'user_id': user1_id,
            #     'document_link': f'{base_s3_url}/static/example.txt',
            #     'document_number': '№ 59124',
            #     'type': type_of_histories[1],
            #     'rank_id': rank1_id,
            #     'rank_assigned_by': "Кусманов А.С.",
            #     'name': '2 history',
            #     'position_id': None,  # Add the missing parameter here
            #     'penalty_id': None,  # Add the missing parameter here
            #     'emergency_service_id': None,  # Add the missing parameter here
            #     'work_experience_id': None,  # Add the missing parameter here
            #     'secondment_id': None,  # Add the missing parameter here
            #     'name_change_id': None,  # Add the missing parameter here
            #     'attestation_id': None,  # Add the missing parameter here
            #     'service_characteristic_id': None,  # Add the missing parameter here
            #     'status_id': None,  # Add the missing parameter here
            #     'coolness_id': None,  # Add the missing parameter here
            #     'contract_id': None,  # Add the missing parameter here
            #     'attestation_status': None,  # МЕНЯТЬ НА attestation_status
            #     'experience_years': None,  # Add the missing parameter here
            #     'characteristic_initiator_id': None,  # Add the missing parameter here
            #     'coefficient' : None,
            #     'percentage' : None,
            #     'staff_division_id' : None,
            #     'name_of_organization': None,
            #     'badge_id' : None,
            #     'is_credited': None,
            #     'document_style': None,
            #     'date_credited': None,
            #     'emergency_rank_id': rank1_id
            # },
            {
                'id': history3_id,
                'date_from': datetime.datetime(2019, 3, 1),
                'date_to': datetime.datetime(2019, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 59124',
                'type': type_of_histories[2],
                'penalty_id': penalty_id,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # Add the missing parameter here
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },

            {
                'id': history6_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': type_of_histories[5],
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': secondment_id,  # МЕНЯТЬ НА secondment_id
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # Add the missing parameter here
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history7_id,
                'date_from': datetime.datetime(2012, 3, 1),
                'date_to': None,
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': type_of_histories[6],
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': name_change_id,  # МЕНЯТЬ НА name_change_id
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # Add the missing parameter here
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history15_id,  # TODO: change the id
                'date_from': datetime.datetime(2012, 3, 1),
                'date_to': datetime.datetime(2014, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': 'work_experience_history',
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # МЕНЯТЬ НА name_change_id
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # Add the missing parameter here
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': 'Cleverest Technologies',
                'badge_id': None,
                'is_credited': True,
                'document_style': 'Первый',
                'date_credited': datetime.datetime(2014, 3, 31),
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history16_id,
                'date_from': datetime.datetime(2015, 5, 5),
                'date_to': None,
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': type_of_histories[6],
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': name_change2_id,  # МЕНЯТЬ НА name_change_id
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # Add the missing parameter here
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history8_id,
                'date_from': datetime.datetime(2012, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': type_of_histories[7],
                # МЕНЯТЬ НА attestation_status
                'attestation_status': 'Занимаемой должности соответсвует',
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': attestation_id,  # МЕНЯТЬ НА attestation_id
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # Add the missing parameter here
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history11_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': type_of_histories[10],
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': coolness_id,  # МЕНЯТЬ НА coolness_id
                'contract_id': None,  # Add the missing parameter here
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history12_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': type_of_histories[11],
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': contract_id,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history13_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': type_of_histories[8],
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                # МЕНЯТЬ НА characteristic_initiator_id
                'characteristic_initiator_id': user2_id,
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history18_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history19_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge1_1_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history20_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge1_2_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history21_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user1_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge1_3_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history22_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user2_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge2_1_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history23_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user2_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge2_2_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            },
            {
                'id': history24_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user2_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge2_3_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            }, {
                'id': history25_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user3_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge3_1_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            }, {
                'id': history26_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user3_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge3_2_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            }, {
                'id': history27_id,
                'date_from': datetime.datetime(2020, 3, 1),
                'date_to': datetime.datetime(2021, 3, 31),
                'user_id': user3_id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 12421',
                'type': "badge_history",
                'penalty_id': None,
                'name': '3 history',
                'position_id': None,  # Add the missing parameter here
                'rank_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # МЕНЯТЬ НА contract_id
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': 5,
                'characteristic_initiator_id': None,  # МЕНЯТЬ НА characteristic_initiator_id
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': badge3_3_id,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None,
                'contractor_signer_name': None,
                'contractor_signer_nameKZ': None,
            }
        ])

    candidate_category1_id = get_uuid()
    candidate_category2_id = get_uuid()
    candidate_category3_id = get_uuid()
    candidate_category4_id = get_uuid()
    candidate_category5_id = get_uuid()
    candidate_category6_id = get_uuid()
    candidate_category7_id = get_uuid()
    candidate_category8_id = get_uuid()
    candidate_category9_id = get_uuid()
    candidate_category10_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['candidate_categories'],
        [{
            'id': candidate_category1_id,
            'name': 'Оперативная служба СГО РК',
            'nameKZ': 'ҚР МКҚ жедел қызметі'
        }, {
            'id': candidate_category2_id,
            'name': 'Оперативная воинская служба СОН СГО РК',
            'nameKZ': 'ҚР МКҚ АМК жедел әскери қызметі'
        }, {
            'id': candidate_category3_id,
            'name': 'Оперативно-постовая служба СГО РК',
            'nameKZ': 'ҚР МКҚ жедел жұмыс жоспары қызметі'
        }, {
            'id': candidate_category4_id,
            'name': 'Оперативно-постовая воинская служба СОН СГО РК',
            'nameKZ': 'ҚР МКҚ АМК жедел жұмыс жоспары әскери қызметі'
        }, {
            'id': candidate_category5_id,
            'name': 'Оперативно-техническая и информационно-аналитическая служба СГО РК ',
            'nameKZ': 'ҚР МКҚ жедел техникалық және ақпараттық қызметі'
        }, {
            'id': candidate_category6_id,
            'name': 'Оперативно-техническая и информационно-аналитическая воинская служба СОН СГО РК',
            'nameKZ': 'ҚР МКҚ АМК жедел техникалық және ақпараттық әскери қызметі'
        }, {
            'id': candidate_category7_id,
            'name': 'Инженерно-техническая, медицинская, административная и хозяйственная служба СГО РК',
            'nameKZ': 'ҚР МКҚ жедел инженерлік-техникалық, өнеркәсіп, әкімшілік және құрылымдық қызметі'
        }, {
            'id': candidate_category8_id,
            'name': 'Инженерно-техническая, медицинская, административная и хозяйственная воинская служба СОН СГО РК',
            'nameKZ': 'ҚР МКҚ АМК жедел инженерлік-техникалық, өнеркәсіп, әкімшілік және құрылымдық әскери қызметі'
        }, {
            'id': candidate_category9_id,
            'name': 'Водители службы СГО РК',
            'nameKZ': 'ҚР МКҚ жедел шоферлері'
        }, {
            'id': candidate_category10_id,
            'name': 'Водители воинской службы СОН СГО РК',
            'nameKZ': 'ҚР МКҚ АМК жедел шоферлері'
        }, ]
    )

    candidate_stage_types1_id = get_uuid()
    candidate_stage_types2_id = get_uuid()
    candidate_stage_types3_id = get_uuid()
    candidate_stage_types4_id = get_uuid()
    candidate_stage_types5_id = get_uuid()
    candidate_stage_types6_id = get_uuid()
    candidate_stage_types7_id = get_uuid()
    candidate_stage_types8_id = get_uuid()
    candidate_stage_types9_id = get_uuid()
    candidate_stage_types10_id = get_uuid()
    candidate_stage_types11_id = get_uuid()
    candidate_stage_types12_id = get_uuid()
    candidate_stage_types13_id = get_uuid()
    candidate_stage_types14_id = get_uuid()
    candidate_stage_types15_id = get_uuid()
    candidate_stage_types16_id = get_uuid()
    candidate_stage_types17_id = get_uuid()
    candidate_stage_types18_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['candidate_stage_types'],
        [{
            'id': candidate_stage_types1_id,
            'name': 'Запросы с внешних источников (др. гос органы)',
            'nameKZ': 'Сыртқы көздерден сұраулар (басқа мемлекеттік органдар)'
        }, {
            'id': candidate_stage_types2_id,
            'name': 'Первичная беседа',
            'nameKZ': 'Бастапқы әңгіме'
        }, {
            'id': candidate_stage_types3_id,
            'name': 'Рецензия на эссе',
            'nameKZ': 'Эссеге шолу',
        }, {
            'id': candidate_stage_types4_id,
            'name': 'Дополнительная беседа',
            'nameKZ': 'Қосымша әңгіме',
        }, {
            'id': candidate_stage_types5_id,
            'name': 'Военно-врачебная комиссия',
            'nameKZ': 'Әскери-дәрігерлік комиссия'
        }, {
            'id': candidate_stage_types6_id,
            'name': 'Беседа с психологом',
            'nameKZ': 'Психологпен әңгіме',
            'is_curator_review_required': True
        }, {
            'id': candidate_stage_types7_id,
            'name': 'Результаты тестирования на знание законодательства РК',
            'nameKZ': 'ҚР заңнамасының тестілеу нәтижелері'
        }, {
            'id': candidate_stage_types8_id,
            'name': 'Беседа о религии',
            'nameKZ': 'Дін туралы әңгіме',
        }, {
            'id': candidate_stage_types9_id,
            'name': 'Беседа с родителями',
            'nameKZ': 'Ата-аналармен әңгіме',
        }, {
            'id': candidate_stage_types10_id,
            'name': 'Справка по результатам оперативного задания (не обязательно)',
            'nameKZ': 'Жедел тапсырманың нәтижелері бойынша анықтама (міндетті емес)',
            'is_curator_review_required': True
        }, {
            'id': candidate_stage_types11_id,
            'name': 'Беседа о проф. пригодности',
            'nameKZ': 'Кәсіби жарамдылық туралы әңгіме',
            'is_curator_review_required': True
        }, {
            'id': candidate_stage_types12_id,
            'name': 'Беседа с представителем УСБ',
            'nameKZ': 'ЖҚБ өкілімен әңгіме',
            'is_curator_review_required': True
        }, {
            'id': candidate_stage_types13_id,
            'name': 'Беседа с руководителем структурного подразделения',
            'nameKZ': 'Структуралық бөлімдің басқарушысымен әңгіме',
            'is_curator_review_required': True
        }, {
            'id': candidate_stage_types14_id,
            'name': 'Беседа с руководством департамента кадров',
            'nameKZ': 'Кадрлар департаментінің басшылығымен әңгімелесу',
            'is_curator_review_required': True
        }, {
            'id': candidate_stage_types15_id,
            'name': 'Результаты полиграфологического исследования',
            'nameKZ': 'Полиграфологиялық зерттеу нәтижелері',
        }, {
            'id': candidate_stage_types16_id,
            'name': 'Результаты физической подготовки',
            'nameKZ': 'Дене шынықтыру нәтижелері',
        }, {
            'id': candidate_stage_types17_id,
            'name': 'Заключение по спец. проверке',
            'nameKZ': 'Арнайы тексеру бойынша қорытынды',
        }, {
            'id': candidate_stage_types18_id,
            'name': 'Заключение о зачислении',
            'nameKZ': 'Қабылдау қорытынды',
            'is_curator_review_required': True
        }]
    )

    candidate_stage_question1_id = get_uuid()  # Первичная беседа
    candidate_stage_question2_id = get_uuid()  # Первичная беседа
    candidate_stage_question3_id = get_uuid()  # Первичная беседа
    candidate_stage_question4_id = get_uuid()  # Первичная беседа
    candidate_stage_question5_id = get_uuid()  # Первичная беседа
    candidate_stage_question6_id = get_uuid()  # Первичная беседа
    candidate_stage_question7_id = get_uuid()  # Первичная беседа
    candidate_stage_question8_id = get_uuid()  # Первичная беседа
    candidate_stage_question9_id = get_uuid()  # Первичная беседа
    candidate_stage_question10_id = get_uuid()  # Первичная беседа
    # Запросы с внешних источников (др. гос органы)
    candidate_stage_question11_id = get_uuid()
    candidate_stage_question12_id = get_uuid()  # Беседа о религии
    candidate_stage_question13_id = get_uuid()  # Беседа с родителями
    # Справка о профессиональной пригодности
    candidate_stage_question14_id = get_uuid()
    # Дополнительная беседа (не обязательно)
    candidate_stage_question15_id = get_uuid()
    candidate_stage_question16_id = get_uuid()  # Беседа с представителем УСБ
    # Беседа с руководством департамента кадров
    candidate_stage_question17_id = get_uuid()
    candidate_stage_question18_id = get_uuid()  # Рецензия на эссе
    candidate_stage_question19_id = get_uuid()  # Заключение по спец. проверке
    candidate_stage_question20_id = get_uuid()  # Заключение о зачислении
    # Результаты тестирования на знание законодательства РК
    candidate_stage_question21_id = get_uuid()
    candidate_stage_question22_id = get_uuid()  # Военно-врачебная комиссия
    candidate_stage_question23_id = get_uuid()
    candidate_stage_question24_id = get_uuid()
    candidate_stage_question25_id = get_uuid()
    candidate_stage_question26_id = get_uuid()
    candidate_stage_question27_id = get_uuid()
    candidate_stage_question28_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['candidate_stage_questions'],
        [{
            'id': candidate_stage_question1_id,
            'question_type': 'Document',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': None,
        }, {
            'id': candidate_stage_question2_id,
            'question_type': 'Dropdown',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Кем подобран и кем рекомендован',
        }, {
            'id': candidate_stage_question28_id,
            'question_type': 'Document',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': None,
        }, {
            'id': candidate_stage_question3_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Краткие сведения из автобиографии',
            'description': '(о рождении, школе, учебе в колледже/ВУЗе, срочной службе, трудовой деятельности)'
        }, {
            'id': candidate_stage_question4_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Как характеризуется с последнего места работы',
            'description': '(сведения из характеристики с места работы)'
        }, {
            'id': candidate_stage_question5_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Доведение требований к службе в СГО РК',
        }, {
            'id': candidate_stage_question6_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Мотив кандидата на службу в СГО РК',
        }, {
            'id': candidate_stage_question7_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Рекомендация кандидату (читать газеты, смотреть мировые новости и тд.)',
        }, {
            'id': candidate_stage_question8_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Сведения о родственниках кандидата',
        }, {
            'id': candidate_stage_question9_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Дополнительные сведения (физическая подготовка)',
        }, {
            'id': candidate_stage_question10_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Подведение итогов беседы',
        }, {
            'id': candidate_stage_question11_id,
            'question_type': 'Dropdown',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': 'Категория кандидата',
        }, {
            'id': candidate_stage_question12_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types3_id,
            'question': None
        }, {
            'id': candidate_stage_question13_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types4_id,
            'question': None
        }, {
            'id': candidate_stage_question14_id,
            'question_type': 'Choice',
            'candidate_stage_type_id': candidate_stage_types5_id,
            'question': None
        }, {
            'id': candidate_stage_question15_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types6_id,
            'question': None
        }, {
            'id': candidate_stage_question16_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types7_id,
            'question': None
        }, {
            'id': candidate_stage_question17_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types8_id,
            'question': None
        }, {
            'id': candidate_stage_question18_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types9_id,
            'question': None
        }, {
            'id': candidate_stage_question19_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types10_id,
            'question': None
        }, {
            'id': candidate_stage_question20_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types11_id,
            'question': None
        }, {
            'id': candidate_stage_question21_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types12_id,
            'question': None
        }, {
            'id': candidate_stage_question22_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types13_id,
            'question': None
        }, {
            'id': candidate_stage_question23_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types14_id,
            'question': None
        }, {
            'id': candidate_stage_question24_id,
            'question_type': 'Choice',
            'candidate_stage_type_id': candidate_stage_types15_id,
            'question': None
        }, {
            'id': candidate_stage_question25_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types16_id,
            'question': None
        }, {
            'id': candidate_stage_question26_id,
            'question_type': 'Document',
            'candidate_stage_type_id': candidate_stage_types17_id,
            'question': None
        }, {
            'id': candidate_stage_question27_id,
            'question_type': 'Document',
            'candidate_stage_type_id': candidate_stage_types18_id,
            'question': None
        }]
    )

    create_candidate_stage_info(candidate_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate_id,
                                candidate_stage_types18_id)

    # candidate2_id
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate2_id,
                                candidate_stage_types18_id)

    # candidate3_id
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate3_id,
                                candidate_stage_types18_id)

    # candidate4_id
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate4_id,
                                candidate_stage_types18_id)

    # candidate5_id
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate5_id,
                                candidate_stage_types18_id)

    # candidate6_id
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate6_id,
                                candidate_stage_types18_id)

    # candidate7_id
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate7_id,
                                candidate_stage_types18_id)

    # candidate8_id
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate8_id,
                                candidate_stage_types18_id)

    # candidate9_id
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate9_id,
                                candidate_stage_types18_id)

    # candidate10_id
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types12_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate10_id,
                                candidate_stage_types18_id)

    # candidate11_id
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types1_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types2_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types3_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types4_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types5_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types6_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types7_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types8_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types9_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types10_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types11_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types13_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types14_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types15_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types16_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types17_id)
    create_candidate_stage_info(candidate11_id,
                                candidate_stage_types18_id)

    candidate_essay_type1_id = get_uuid()
    candidate_essay_type2_id = get_uuid()
    candidate_essay_type3_id = get_uuid()
    candidate_essay_type4_id = get_uuid()
    candidate_essay_type5_id = get_uuid()
    candidate_essay_type6_id = get_uuid()
    candidate_essay_type7_id = get_uuid()
    candidate_essay_type8_id = get_uuid()
    candidate_essay_type9_id = get_uuid()
    candidate_essay_type10_id = get_uuid()
    candidate_essay_type11_id = get_uuid()
    candidate_essay_type12_id = get_uuid()
    candidate_essay_type13_id = get_uuid()
    candidate_essay_type14_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['candidate_essay_types'],
        [{
            'id': candidate_essay_type1_id,
            'name': 'Будущее Казахстана - мое будущее',
            'nameKZ': 'Қазақстанның болашағы-менің болашағым',
        }, {
            'id': candidate_essay_type2_id,
            'name': '«Я патриот! А это значит ...»',
            'nameKZ': 'Мен патриотпын! Бұл дегеніміз ...»'
        }, {
            'id': candidate_essay_type3_id,
            'name': 'Мое образование - мой капитал',
            'nameKZ': 'Менің білімім - менің капиталым'
        }, {
            'id': candidate_essay_type4_id,
            'name': 'Социальные сети: плюсы и минусы',
            'nameKZ': 'Әлеуметтік медиа: оң және теріс жақтары'
        }, {
            'id': candidate_essay_type5_id,
            'name': 'Армия в моей жизни.',
            'nameKZ': 'Менің өмірімдегі Армия.'
        }, {
            'id': candidate_essay_type6_id,
            'name': 'Будущее Казахстана.',
            'nameKZ': 'Қазақстанның болашағы.'
        }, {
            'id': candidate_essay_type7_id,
            'name': 'В чем смысл жизни?',
            'nameKZ': 'Өмірдің мәні неде?'
        }, {
            'id': candidate_essay_type8_id,
            'name': 'Верность долгу, и измена Родине',
            'nameKZ': 'Борышқа адалдық және Отанға опасыздық'
        }, {
            'id': candidate_essay_type9_id,
            'name': 'Где начинается Родина',
            'nameKZ': 'Отан қайдан басталады'
        }, {
            'id': candidate_essay_type10_id,
            'name': 'Как вы понимаете значение слова подвиг',
            'nameKZ': 'Виг сөзінің мағынасын қалай түсінесіз',
        }, {
            'id': candidate_essay_type11_id,
            'name': 'Почему я хочу служить в СГО РК',
            'nameKZ': "Неге мен ҚР МКҚ-да қызмет еткім келеді"
        }, {
            'id': candidate_essay_type12_id,
            'name': 'Кто для меня Президент',
            'nameKZ': 'Мен үшін Президент кім'
        }, {
            'id': candidate_essay_type13_id,
            'name': 'Что я могу сделать для Родины',
            'nameKZ': 'Отан үшін не істей аламын'
        }, {
            'id': candidate_essay_type14_id,
            'name': 'Герои нашего времени',
            'nameKZ': 'Біздің заманымыздың батырлары'
        }]
    )

    # candidate_stage_info_id = get_uuid()

    # op.bulk_insert(
    #     Base.metadata.tables['candidate_stage_infos'],
    #     [{
    #         'id': candidate_stage_info_id,
    #         'staff_unit_coordinate_id': staff_unit1_id,
    #         'candidate_stage_type_id': candidate_stage_types1_id,
    #         'is_waits': True
    #     }]
    # )

    hr_vacancy_id = get_uuid()
    hr_vacancy2_id = get_uuid()
    hr_vacancy3_id = get_uuid()
    hr_vacancy4_id = get_uuid()
    hr_vacancy6_id = get_uuid()
    hr_vacancy7_id = get_uuid()
    hr_vacancy8_id = get_uuid()
    hr_vacancy9_id = get_uuid()
    hr_vacancy10_id = get_uuid()
    hr_vacancy11_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_vacancies'],
        [{
            'id': hr_vacancy_id,
            'staff_unit_id': staff_unit21_id
        }, {
            'id': hr_vacancy2_id,
            'staff_unit_id': staff_unit22_id
        }, {
            'id': hr_vacancy3_id,
            'staff_unit_id': staff_unit1_id
        }, {
            'id': hr_vacancy4_id,
            'staff_unit_id': staff_unit2_id
        }, {
            'id': hr_vacancy6_id,
            'staff_unit_id': staff_unit4_id
        }, {
            'id': hr_vacancy7_id,
            'staff_unit_id': staff_unit5_id
        }, {
            'id': hr_vacancy8_id,
            'staff_unit_id': staff_unit6_id
        }, {
            'id': hr_vacancy9_id,
            'staff_unit_id': staff_unit7_id
        }, {
            'id': hr_vacancy10_id,
            'staff_unit_id': staff_unit29_id
        }, {
            'id': hr_vacancy11_id,
            'staff_unit_id': staff_unit12_id
        }]
    )

    hr_vacancy_requirement_id = get_uuid()
    hr_vacancy_requirement2_id = get_uuid()
    hr_vacancy_requirement3_id = get_uuid()
    hr_vacancy_requirement4_id = get_uuid()
    hr_vacancy_requirement5_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_vacancies_requirements'],
        [{
            'id': hr_vacancy_requirement_id,
            'name': "Пригодность по состоянию здоровья",
            'nameKZ': "Денсаулық жағдайы бойынша жарамдылық"
        }, {
            'id': hr_vacancy_requirement2_id,
            'name': "10 лет стажа работы",
            'nameKZ': "10 жыл жұмыс тәжірибесі"
        }, {
            'id': hr_vacancy_requirement3_id,
            'name': "Высшее образование",
            'nameKZ': "Жоғары білім"
        }, {
            'id': hr_vacancy_requirement4_id,
            'name': "Коммуникационные навыки",
            'nameKZ': "Қарым-қатынас дағдылары"
        }, {
            'id': hr_vacancy_requirement5_id,
            'name': "Знание законодательства и правил",
            'nameKZ': "Заң мен ережелерді білу"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['hr_vacancy_hr_vacancy_requirements'],
        [{
            'hr_vacancy_id': hr_vacancy_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement_id
        }, {
            'hr_vacancy_id': hr_vacancy_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement2_id
        }, {
            'hr_vacancy_id': hr_vacancy_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement3_id
        }, {
            'hr_vacancy_id': hr_vacancy2_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement4_id
        }, {
            'hr_vacancy_id': hr_vacancy2_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement5_id
        }, {
            'hr_vacancy_id': hr_vacancy3_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement_id
        }, {
            'hr_vacancy_id': hr_vacancy3_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement2_id
        }, {
            'hr_vacancy_id': hr_vacancy4_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement3_id
        }, {
            'hr_vacancy_id': hr_vacancy4_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement4_id
        }, {
            'hr_vacancy_id': hr_vacancy6_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement2_id
        }, {
            'hr_vacancy_id': hr_vacancy6_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement3_id
        }, {
            'hr_vacancy_id': hr_vacancy7_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement4_id
        }, {
            'hr_vacancy_id': hr_vacancy7_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement5_id
        }, {
            'hr_vacancy_id': hr_vacancy8_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement_id
        }, {
            'hr_vacancy_id': hr_vacancy8_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement2_id
        }, {
            'hr_vacancy_id': hr_vacancy9_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement3_id
        }, {
            'hr_vacancy_id': hr_vacancy9_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement4_id
        }, {
            'hr_vacancy_id': hr_vacancy10_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement5_id
        }, {
            'hr_vacancy_id': hr_vacancy11_id,
            'hr_vacancy_requirement_id': hr_vacancy_requirement_id
        }]
    )


def create_user(id,
                name,
                surname,
                father_name,
                email,
                group_id,
                supervised_by,
                call_sign,
                number,
                staff_unit_id,
                rank_id,
                actual_staff_unit_id,
                icon,
                position_id,
                is_military,
                cabinet,
                is_active,
                user_replacing_id=None,
                iin: str = "123456789012"):
    op.bulk_insert(
        Base.metadata.tables['staff_units'],
        [{
            'id': staff_unit_id,
            'user_id': id,
            'position_id': position_id,
            'staff_division_id': group_id,
            'user_replacing_id': user_replacing_id,
            'requirements':
                [
                    {
                        "name": "Требования к образованию",
                        "nameKZ": "Білім талаптары",
                        "keys": [
                            {
                                "text": ["Высшее профессиональное"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Жоғары кәсіпкерлік"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования к стажу",
                        "nameKZ": "Тәжірибе талаптары",
                        "keys": [
                            {
                                "text": ["10 лет стажа работы в правоохранительных, специальных государственных органах или на воинской службе",
                                         "4 года стажа работы на руководящих должностях"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Құқық қорғау, арнаулы мемлекеттік органдарда немесе әскери қызметте 10 жыл жұмыс өтілі",
                                         "4 жыл басшы лауазымдардағы жұмыс өтілі"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Практический опыт",
                        "nameKZ": "Практикалық тәжірибе",
                        "keys": [
                            {
                                "text": ["Наличие обязательных знаний, умений и навыков"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Міндетті білімнің, іскерліктің және дағдылардың болуы"],
                                "lang": "kz"
                            }
                        ]
                    },
                    {
                        "name": "Требования по состоянию здоровья",
                        "nameKZ": "Денсаулық талаптары",
                        "keys": [
                            {
                                "text": ["Пригодность по состоянию здоровья"],
                                "lang": "ru"
                            },
                            {
                                "text": ["Денсаулық жағдайы бойынша жарамдылық"],
                                "lang": "kz"
                            }
                        ]
                    }
                ]
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['users'],
        [{
            'id': id,
            'email': email,
            'password': '$2b$12$vhg69KJxWiGgetoLxGRvie3VxElPt45i4ELJiE/V2qOj30X3c3.7m',
            'first_name': name,
            'last_name': surname,
            'father_name': father_name,
            'staff_unit_id': staff_unit_id,
            'date_birth': '1990-01-23',
            'supervised_by': supervised_by,
            'call_sign': call_sign,
            'id_number': number,
            'phone_number': '+7 (777) 123-47-89',
            'rank_id': rank_id,
            'actual_staff_unit_id': actual_staff_unit_id,
            'icon': icon,
            'service_phone_number': "679-258",
            'personal_id': number,
            'is_military': is_military,
            'cabinet': cabinet,
            'address': "г. Астана, ул. Мангилик ел 54, кв. 15",
            'iin': iin,
            'is_active': is_active,
        }]
    )

    rank_history_id = get_uuid()
    op.bulk_insert(
        Base.metadata.tables['histories'],
        [
            {
                'id': rank_history_id,
                'date_from': str(datetime.datetime(2019, 2, 1)),
                'date_to': None,
                'user_id': id,
                'document_link': f'{base_s3_url}/static/example.txt',
                'document_number': '№ 59124',
                'type': type_of_histories[1],
                'rank_id': rank_id,
                'rank_assigned_by': "Кусманов А.С.",
                'position_id': None,  # Add the missing parameter here
                'penalty_id': None,  # Add the missing parameter here
                'emergency_service_id': None,  # Add the missing parameter here
                'work_experience_id': None,  # Add the missing parameter here
                'secondment_id': None,  # Add the missing parameter here
                'name_change_id': None,  # Add the missing parameter here
                'attestation_id': None,  # Add the missing parameter here
                'service_characteristic_id': None,  # Add the missing parameter here
                'status_id': None,  # Add the missing parameter here
                'coolness_id': None,  # Add the missing parameter here
                'contract_id': None,  # Add the missing parameter here
                'attestation_status': None,  # МЕНЯТЬ НА attestation_status
                'experience_years': None,  # Add the missing parameter here
                'characteristic_initiator_id': None,  # Add the missing parameter here
                'coefficient': None,
                'percentage': None,
                'staff_division_id': None,
                'name_of_organization': None,
                'badge_id': None,
                'is_credited': None,
                'document_style': None,
                'date_credited': None,
                'emergency_rank_id': None
            }
        ]
    )

    profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['profiles'],
        [{
            'id': profile_id,
            'user_id': id,
        }]
    )

    personal_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['personal_profiles'],
        [{
            'id': personal_profile_id,
            'profile_id': profile_id,
        }]
    )

    educational_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['educational_profiles'],
        [{
            'id': educational_profile_id,
            'profile_id': profile_id
        }]
    )

    medical_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['medical_profiles'],
        [{
            'id': medical_profile_id,
            'profile_id': profile_id

        }]
    )

    additional_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['additional_profiles'],
        [{
            'id': additional_profile_id,
            'profile_id': profile_id

        }]
    )

    user_vehicles = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['user_vehicles'],
        [{
            'id': user_vehicles,
            'profile_id': additional_profile_id,
            'vin_code': 'JN1WNYD21U0000001',
            'date_from': '2021-02-25',
            'number': '021 AMS 01',
            'document_link': f'{base_s3_url}/static/example.txt',
            'name': 'Toyota Camry ACV50(2020)',
            'nameKZ': 'Toyota Camry ACV50(2020)'
        }]
    )

    family_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['family_profiles'],
        [{
            'id': family_profile_id,
            'profile_id': profile_id

        }]
    )

    academic_degree1_id = get_uuid()
    academic_degree2_id = get_uuid()
    academic_degree3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['academic_degrees'],
        [{
            'id': academic_degree1_id,
            'profile_id': educational_profile_id,
            'degree_id': academic_degree_degree1_id,
            'science_id': science1_id,
            'specialty_id': specialty1_id,
            'document_number': "1231262",
            'document_link': f"{base_s3_url}/static/example.txt",
            'assignment_date': "2022-10-07"
        }, {
            'id': academic_degree2_id,
            'profile_id': educational_profile_id,
            'degree_id': academic_degree_degree2_id,
            'science_id': science2_id,
            'specialty_id': specialty2_id,
            'document_number': 2,
            'document_link': f"{base_s3_url}/static/example.txt",
            'assignment_date': "2022-10-08"
        }]
    )

    language_proficiency1_id = get_uuid()
    language_proficiency2_id = get_uuid()
    language_proficiency3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['language_proficiencies'],
        [{
            'id': language_proficiency1_id,
            'language_id': language1_id,
            "level": 5,
            'profile_id': educational_profile_id
        }, {
            'id': language_proficiency2_id,
            'language_id': language2_id,
            "level": 3,
            'profile_id': educational_profile_id
        }, {
            'id': language_proficiency3_id,
            'language_id': language3_id,
            "level": 4,
            'profile_id': educational_profile_id,
        }]
    )

    academic_title1_id = get_uuid()
    academic_title2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['academic_titles'],
        [{
            'id': academic_title1_id,
            'profile_id': educational_profile_id,
            'degree_id': academic_title_degree1_id,
            'specialty_id': specialty1_id,
            'document_number': '123123',
            'document_link': f"{base_s3_url}/static/example.txt",
            'assignment_date': "2022-12-12"
        }, {
            'id': academic_title2_id,
            'profile_id': educational_profile_id,
            'degree_id': academic_title_degree2_id,
            'specialty_id': specialty2_id,
            'document_number': '123123',
            'document_link': f"{base_s3_url}/static/example.txt",
            'assignment_date': "2022-12-13"
        }]
    )

    course1_id = get_uuid()
    course2_id = get_uuid()
    course3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['courses'],
        [{
            'id': course1_id,
            'name': "Backend курс",
            'nameKZ': 'Backend курс',
            'profile_id': educational_profile_id,
            'course_provider_id': course_provider1_id,
            'specialty_id': specialty1_id,
            'document_number': 1,
            'document_link': f"{base_s3_url}/static/example.txt",
            'assignment_date': "2022-12-12",
            'start_date': '2019-10-12',
            'end_date': '2019-12-10'
        }, {
            'id': course2_id,
            'name': "Курсы по подготовке к стрельбе",
            'nameKZ': 'Атуға дайындық курстары',
            'profile_id': educational_profile_id,
            'course_provider_id': course_provider2_id,
            'specialty_id': specialty2_id,
            'document_number': 2,
            'document_link': f"{base_s3_url}/static/example.txt",
            'assignment_date': "2022-12-13",
            'start_date': '2020-11-25',
            'end_date': '2020-12-15'
        }, {
            'id': course3_id,
            'name': "Front-End курс",
            'nameKZ': 'Front-End курс',
            'profile_id': educational_profile_id,
            'course_provider_id': course_provider3_id,
            'specialty_id': specialty3_id,
            'document_number': 3,
            'document_link': f"{base_s3_url}/static/example.txt",
            'assignment_date': "2022-12-14",
            'start_date': '2021-11-12',
            'end_date': '2022-02-05'
        }]
    )

    education1_id = get_uuid()
    education2_id = get_uuid()
    education3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['educations'],
        [{
            'id': education1_id,
            'profile_id': educational_profile_id,
            'institution_id': institution1_id,
            'degree_id': institution_degree_type1_id,
            'start_date': "2014-09-01",
            'end_date': "2019-06-01",
            'document_link': "document_link1"
        }, {
            'id': education2_id,
            'profile_id': educational_profile_id,
            'institution_id': institution2_id,
            'degree_id': institution_degree_type2_id,
            'start_date': "2019-09-01",
            'end_date': "2022-06-01",
            'document_link': "document_link2"
        }]
    )

    sport_degree1_id = get_uuid()
    sport_degree2_id = get_uuid()
    sport_degree3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['sport_degrees'],
        [{
            'id': sport_degree1_id,
            'profile_id': personal_profile_id,
            'name': "Мастер спорта по боксу",
            'nameKZ': 'Бокстан спорт шебері',
            'assignment_date': '2022-10-09',
            'document_link': f'{base_s3_url}/static/example.txt',
            'sport_type_id': sport_type1_id
        }, {
            'id': sport_degree2_id,
            'profile_id': personal_profile_id,
            'name': "Мастер спорта по карате",
            'nameKZ': 'Каратэден спорт шебері',
            'assignment_date': '2022-10-10',
            'document_link': f'{base_s3_url}/static/example.txt',
            'sport_type_id': sport_type2_id
        }, {
            'id': sport_degree3_id,
            'profile_id': personal_profile_id,
            'name': "Кандидат мастер спорта по джиу-джитсу",
            'nameKZ': 'Джиу-джитсудан спорт шеберілігінен үміткер',
            'assignment_date': '2022-10-11',
            'document_link': f'{base_s3_url}/static/example.txt',
            'sport_type_id': sport_type3_id
        }]
    )

    sport_achievement1_id = get_uuid()
    sport_achievement2_id = get_uuid()
    sport_achievement3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['sport_achievements'],
        [{
            'id': sport_achievement1_id,
            'profile_id': personal_profile_id,
            'name': "III место на Токийском съезде джиу-джитсу",
            'nameKZ': 'Токио джиу-джитсу конгресінде III орын',
            'assignment_date': '2022-10-09',
            'document_link': f'{base_s3_url}/static/example.txt',
            'sport_type_id': sport_type3_id
        }, {
            'id': sport_achievement2_id,
            'profile_id': personal_profile_id,
            'name': "I место в Чемпионате Мира по боксу",
            'nameKZ': 'Бокстан Әлем чемпионатында I орын',
            'assignment_date': '2022-10-10',
            'document_link': f'{base_s3_url}/static/example.txt',
            'sport_type_id': sport_type1_id
        }, {
            'id': sport_achievement3_id,
            'profile_id': personal_profile_id,
            'name': "II место в Чемпионате города Астаны по карате",
            'nameKZ': 'II место в Чемпионате города Астаны по карате',
            'assignment_date': '2022-10-11',
            'document_link': f'{base_s3_url}/static/example.txt',
            'sport_type_id': sport_type2_id
        }]
    )

    """
        Table biographic_infos as BI {
        id uuid 
        place_birth str
        gender bool
        citizenship str
        nationality str
        family_status uuid
        address str
        profile_id uuid
        }
    """

    biographic_info_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['biographic_infos'],
        [{
            'id': biographic_info_id,
            'place_birth': "г. Астана",
            'gender': True,
            'citizenship': "Казахстан",
            'nationality': 'Казах',
            'family_status_id': family_status_id,
            'address': "г. Астана, ул. Мангилик Ел, д. 1, кв. 1",
            'residence_address': 'г. Астана, ул. Мангилик Ел, д. 1, кв. 1',
            'profile_id': personal_profile_id
        }]
    )

    tax_declaration1_id = get_uuid()
    tax_declaration2_id = get_uuid()
    tax_declaration3_id = get_uuid()
    tax_declaration4_id = get_uuid()
    tax_declaration5_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['tax_declarations'],
        [{
            'id': tax_declaration1_id,
            'year': "2019",
            'is_paid': True,
            'profile_id': personal_profile_id
        }, {
            'id': tax_declaration2_id,
            'year': "2020",
            'is_paid': True,
            'profile_id': personal_profile_id
        }, {
            'id': tax_declaration3_id,
            'year': "2021",
            'is_paid': False,
            'profile_id': personal_profile_id
        }, {
            'id': tax_declaration4_id,
            'year': "2022",
            'is_paid': False,
            'profile_id': personal_profile_id
        }, {
            'id': tax_declaration5_id,
            'year': "2023",
            'is_paid': False,
            'profile_id': personal_profile_id
        }]
    )

    user_financial_info_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['user_financial_infos'],
        [{
            'id': user_financial_info_id,
            'iban': "KZ200155980950859874",
            'housing_payments_iban': "KZ200155980950859874",
            'profile_id': personal_profile_id
        }]
    )

    identification_card_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['identification_cards'],
        [{
            'id': identification_card_id,
            'document_number': "04665766",
            'date_of_issue': "2022-09-11",
            'date_to': "2025-09-12",
            'issued_by': "МВД РК",
            'document_link': f"{base_s3_url}/static/example.txt",
            'profile_id': personal_profile_id
        }]
    )

    driving_licence_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['driving_licenses'],
        [{
            'id': driving_licence_id,
            'document_number': "88705845",
            'category': ["A", "B", "C"],
            'date_of_issue': "2022-09-11",
            'date_to': "2022-09-12",
            'document_link': f"{base_s3_url}/static/example.txt",
            'profile_id': personal_profile_id
        }]
    )

    passport_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['passports'],
        [{
            'id': passport_id,
            'document_number': "95909558",
            'date_of_issue': "2022-09-11",
            'date_to': "2022-09-12",
            'document_link': f"{base_s3_url}/static/example.txt",
            'profile_id': personal_profile_id,
            'issued_by': "МВД РК"
        }]
    )

    general_user_information_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['general_user_informations'],
        [{
            'id': general_user_information_id,
            'height': 189,
            'blood_type': "AB (IV) Rh+",
            'age_group': 3,
            'profile_id': medical_profile_id,
            'weight': 82
        }]
    )

    anthropometric_data_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['anthropometric_data'],
        [{
            'id': anthropometric_data_id,
            'head_circumference': 57,
            'shoe_size': 43,
            'neck_circumference': 35,
            'shape_size': 52,
            'bust_size': 56,
            'profile_id': medical_profile_id
        }]
    )

    dispensary_registrations_id = get_uuid()
    dispensary_registrations1_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['dispensary_registrations'],
        [{
            'id': dispensary_registrations_id,
            'name': "Астма",
            'nameKZ': 'Демікпе',
            'initiator': 'Республиканская больница',
            'start_date': "2022-09-12",
            'profile_id': medical_profile_id,
            'document_link': f"{base_s3_url}/static/example.txt"
        }, {
            'id': dispensary_registrations1_id,
            'name': "Сахарный Диабет",
            'nameKZ': "Қант Диабеті",
            'initiator': 'Клиника "Нурсултан"',
            'start_date': "2022-12-15",
            'profile_id': medical_profile_id,
            'document_link': f"{base_s3_url}/static/example.txt"
        }]
    )

    user_liberations_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['user_liberations'],
        [{
            'id': user_liberations_id,
            'reason': "Надрыв спины II стадии",
            'liberation_id': liberation_id,
            'initiator': "Медицинский центр 'Тыныс'",
            'start_date': "2022-09-12",
            'end_date': "2022-10-12",
            'profile_id': medical_profile_id
        }]
    )

    hospital_datas_id = get_uuid()
    hospital_datas1_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hospital_datas'],
        [{
            'id': hospital_datas_id,
            'reason': "Больничный",
            'place': 'ГКП на ПХВ "Городская поликлиника №3"',
            'start_date': "2022-09-12",
            'end_date': "2022-10-12",
            'profile_id': medical_profile_id,
            'document_link': f"{base_s3_url}/static/example.txt",
            'code': 'код-829121'
        }, {
            'id': hospital_datas1_id,
            'reason': "Больничный по причине ОРВИ",
            'place': 'ГКП на ПХВ "Городская поликлиника №3"',
            'start_date': "2022-12-15",
            'end_date': "2022-12-16",
            'profile_id': medical_profile_id,
            'document_link': f"{base_s3_url}/static/example.txt",
            'code': None
        }]
    )

    violations_id = get_uuid()
    violations_id1 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['violations'],
        [{
            'id': violations_id,
            'name': "Мелкое хулиганство",
            'nameKZ': "Кішігірім тәртіп бұзушылық",
            'date': "2022-09-12",
            'issued_by': "Районный суд Сарыаркинского района г.Астана",
            'article_number': "122.12(УК РК)",
            'consequence': "Штраф 40МРП",
            'profile_id': additional_profile_id,
            'document_link': f"{base_s3_url}/static/example.txt"
        }]
    )
    op.bulk_insert(
        Base.metadata.tables['violations'],
        [{
            'id': violations_id1,
            'name': "Большое хулиганство",
            'nameKZ': "Кішігірім тәртіп бұзушылық",
            'date': "2022-10-12",
            'issued_by': "Районный суд Сарыаркинского района г.Астана",
            'article_number': "122.12(УК РК)",
            'consequence': "Штраф 400МРП",
            'profile_id': None,
            'document_link': f"{base_s3_url}/static/example.txt",
        }]
    )

    properties_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['properties'],
        [{
            'id': properties_id,
            'type_id': property_type1_id,
            'purchase_date': "2022-09-12",
            'purchase_type': "В подарок",
            'purchase_typeKZ': "Силыққа",
            'address': "Достык 5",
            'profile_id': additional_profile_id
        }]
    )

    abroad_travels_id = get_uuid()
    abroad_travels_id1 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['abroad_travels'],
        [{
            'id': abroad_travels_id,
            'vehicle_type': "Самолет",
            'destination_country_id': country_id,
            'date_from': "2022-05-10",
            'date_to': "2022-05-11",
            'reason': "Служебная командировка",
            'document_link': f"{base_s3_url}/static/example.txt",
            'profile_id': additional_profile_id

        }]
    )

    op.bulk_insert(
        Base.metadata.tables['abroad_travels'],
        [{
            'id': abroad_travels_id1,
            'vehicle_type': "Вертолет",
            'destination_country_id': country_id,
            'date_from': "2022-05-10",
            'date_to': "2022-05-11",
            'reason': "Праздничная командировка",
            'document_link': f"{base_s3_url}/static/example.txt",
            'profile_id': None

        }]
    )

    op.bulk_insert(
        Base.metadata.tables['service_housings'],
        [{
            'id': get_uuid(),
            'type_id': property_type2_id,
            'address': "ул. Достық 5",
            'issue_date': "2022-09-12",
            'profile_id': additional_profile_id,
            'document_link': f"{base_s3_url}/static/example.txt",
        }]
    )

    special_checks_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['special_checks'],
        [{
            'id': special_checks_id,
            'number': "4584908",
            'issued_by': "Иманов А.Е.",
            'date_of_issue': "2022-01-15",
            'document_link': f"{base_s3_url}/static/example.txt",
            "profile_id": additional_profile_id

        }]
    )

    psychological_checks_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['psychological_checks'],
        [{
            'id': psychological_checks_id,
            'issued_by': "Назаров К.С.",
            'date_of_issue': "2022-03-25",
            'document_link': f"{base_s3_url}/static/example.txt",
            'profile_id': additional_profile_id
        }]
    )

    polygraph_checks_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['polygraph_checks'],
        [{
            'id': polygraph_checks_id,
            'number': "84088880",
            "issued_by": "Жапаров Е.С.",
            "date_of_issue": "2021-02-03",
            "document_link": f"{base_s3_url}/static/example.txt",
            'profile_id': additional_profile_id
        }]
    )

    families_profile_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['families'],
        [{
            'id': families_profile_id,
            'relation_id': family_relation_id,
            'first_name': options.get(email, {'first_name': "Имя"})['first_name'],
            'last_name': 'Темирбеков',
            'father_name': options.get(email, {'father_name': "Отчество"})['father_name'],
            'IIN': "980206556948",
            'birthday': "1998-02-06",
            'birthplace': "г. Астана",
            'address': "г. Астана, ул. Кабанбай батыр, д. 15, кв. 15",
            'workplace': "Astana IT University, профессор",
            'profile_id': family_profile_id
        }, {
            'id': get_uuid(),
            'relation_id': family_relation2_id,
            'first_name': "Айгуль",
            'last_name': "Ахметова",
            'father_name': surname,
            'IIN': "980206556948",
            'birthday': "1998-02-06",
            'birthplace': "г. Астана",
            'address': "г. Астана, ул. Кабанбай батыр, д. 15, кв. 15",
            'workplace': "КазМунайГаз, бухгалтер",
            'profile_id': family_profile_id
        }]
    )
    op.bulk_insert(
        Base.metadata.tables['family_abroad_travels'],
        [{
            'family_id': families_profile_id,
            'abroad_travel_id': abroad_travels_id1,
        }]
    )
    op.bulk_insert(
        Base.metadata.tables['family_violations'],
        [{
            'family_id': families_profile_id,
            'violation_id': violations_id1,
        }]
    )


def downgrade() -> None:
    pass
