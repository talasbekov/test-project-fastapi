"""migration

Revision ID: 9fae9da641dd
Revises: f04c5daf7685
Create Date: 2023-03-02 11:47:59.787804

"""
import uuid

from alembic import op
from core import Base

# revision identifiers, used by Alembic.
revision = '9fae9da641dd'
down_revision = '33853d366eba'
branch_labels = None
depends_on = None


def get_uuid():
    return str(uuid.uuid4())

# Personal
sport_type1_id = get_uuid()
sport_type2_id = get_uuid()
sport_type3_id = get_uuid()

family_status_id = get_uuid()
family_status2_id = get_uuid()
family_status3_id = get_uuid()
family_status4_id = get_uuid()

family_relation_id = get_uuid()
family_relation2_id = get_uuid()

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
    'zhasulan@mail.ru': {
        'first_name': 'Дидар',
        'father_name': 'Даниярович'
    },
    'anuar@mail.ru': {
        'first_name': 'Дидар',
        'father_name': 'Наурызбевович'
    },
    'beksundet@mail.ru': {
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
    'arman@mail.ru': {
        'first_name': 'Улан',
        'father_name': 'Бауыржанович'
    },
    'bauyrzhan@mail.ru': {
        'first_name': 'Алдияр',
        'father_name': 'Маратович'
    },
    'admin@mail.com': {
        'first_name': 'Админ',
        'father_name': 'Админович'
    }
}


def upgrade() -> None:

    badge1_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['badges'],
        [{
            "id": badge1_id,
            "name": "Черный Берет",
            "url": "http://192.168.0.169:8083/static/black_beret.jpg"
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
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A0%D1%8F%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': None
        }, {
            'id': rank2_id,
            'name': 'Младший сержант',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9C%D0%BB%D0%B0%D0%B4%D1%88%D0%B8%D0%B9%20%D1%81%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9C%D0%BB%D0%B0%D0%B4%D1%88%D0%B8%D0%B9%20%D1%81%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank3_id,
            'name': 'Сержант',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank14_id,
            'name': 'Сержант 1-го класса',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82%201-%D0%B3%D0%BE%20%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B0_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': None
        }, {
            'id': rank15_id,
            'name': 'Сержант 2-го класса',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82%202-%D0%B3%D0%BE%20%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B0_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': None
        }, {
            'id': rank16_id,
            'name': 'Сержант 3-го класса',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82%203-%D0%B3%D0%BE%20%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B0_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': None
        }, {
            'id': rank4_id,
            'name': 'Старший сержант',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D1%82%D0%B0%D1%80%D1%88%D0%B8%D0%B9%20%D1%81%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D1%82%D0%B0%D1%80%D1%88%D0%B8%D0%B9%20%D1%81%D0%B5%D1%80%D0%B6%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank5_id,
            'name': 'Лейтенант',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9B%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9B%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank6_id,
            'name': 'Старший лейтенант',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D1%82%D0%B0%D1%80%D1%88%D0%B8%D0%B9%20%D0%BB%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%A1%D1%82%D0%B0%D1%80%D1%88%D0%B8%D0%B9%20%D0%BB%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank7_id,
            'name': 'Капитан',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9A%D0%B0%D0%BF%D0%B8%D1%82%D0%B0%D0%BD_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9A%D0%B0%D0%BF%D0%B8%D1%82%D0%B0%D0%BD.png"
        }, {
            'id': rank8_id,
            'name': 'Майор',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9C%D0%B0%D0%B9%D0%BE%D1%80_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9C%D0%B0%D0%B9%D0%BE%D1%80.png"
        }, {
            'id': rank9_id,
            'name': 'Подполковник',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9F%D0%BE%D0%B4%D0%BF%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9F%D0%BE%D0%B4%D0%BF%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA.png"
        }, {
            'id': rank10_id,
            'name': 'Полковник',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9F%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA_%D0%B2%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%9F%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA.png"
        }, {
            'id': rank11_id,
            'name': 'Генерал-майор',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BC%D0%B0%D0%B9%D0%BE%D1%80.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BC%D0%B0%D0%B9%D0%BE%D1%80.png"
        }, {
            'id': rank12_id,
            'name': 'Генерал-лейтенант',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BB%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BB%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82.png"
        }, {
            'id': rank13_id,
            'name': 'Генерал-полковник',
            'military_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BF%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA.png",
            'employee_url': "http://192.168.0.169:8083/static/%D0%97%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%3D%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BF%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA.png"
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

    op.bulk_insert(
        Base.metadata.tables['positions'],
        [{
            'id': position1_id,
            'name': 'Военно-служащий срочной службы',
            'max_rank_id': rank1_id
        }, {
            'id': position2_id,
            'name': 'Сотрудник охраны 3-категории',
            'max_rank_id': rank2_id
        }, {
            'id': position3_id,
            'name': 'Сотрудник охраны 2-категории',
            'max_rank_id': rank3_id
        }, {
            'id': position4_id,
            'name': 'Сотрудник охраны 1-категории',
            'max_rank_id': rank4_id
        }, {
            'id': position5_id,
            'name': 'Офицер охраны',
            'max_rank_id': rank7_id
        }, {
            'id': position6_id,
            'name': 'Старший офицер охраны',
            'max_rank_id': rank8_id
        }, {
            'id': position7_id,
            'name': 'Старший офицер',
            'max_rank_id': rank8_id
        }, {
            'id': position8_id,
            'name': 'Инспектор',
            'max_rank_id': rank9_id
        }, {
            'id': position9_id,
            'name': 'Старший инспектор',
            'max_rank_id': rank9_id
        }, {
            'id': position10_id,
            'name': 'Начальник отдела',
            'max_rank_id': rank9_id
        }, {
            'id': position11_id,
            'name': 'Заместитель начальника управление - Начальник отдела',
            'max_rank_id': rank9_id
        }, {
            'id': position12_id,
            'name': 'Главный инспектор',
            'max_rank_id': rank10_id
        }, {
            'id': position13_id,
            'name': 'Начальник управления',
            'max_rank_id': rank10_id
        }, {
            'id': position14_id,
            'name': 'Заместитель начальника департамента',
            'max_rank_id': rank10_id
        }, {
            'id': position15_id,
            'name': 'Начальник департамента',
            'max_rank_id': rank10_id
        }, {
            'id': position16_id,
            'name': 'Заместитель начальника Службы',
            'max_rank_id': rank12_id
        }, {
            'id': position17_id,
            'name': 'Начальник Службы',
            'max_rank_id': rank13_id
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
        }, {
            'id': hr_document_status2_id,
            'name': "В процессе",
        }, {
            'id': hr_document_status3_id,
            'name': "Завершен",
        }, {
            'id': hr_document_status4_id,
            'name': "Отменен",
        }, {
            'id': hr_document_status5_id,
            'name': "На доработке",
        }, {
            'id': hr_document_status6_id,
            'name': "Черновик",
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
            'can_cancel': True
        }, {
            'id': doc_type2_id,
            'name': "Эксперт",
            'can_cancel': False
        }, {
            'id': doc_type3_id,
            'name': "Утверждающий",
            'can_cancel': True
        }, {
            'id': doc_type4_id,
            'name': "Уведомляемый",
            'can_cancel': False
        }, {
            'id': doc_type5_id,
            'name': "Инициатор",
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
            'name': "Вся служба"
        }, {
            'id': jurisdiction2_id,
            'name': "Личный Состав"
        }, {
            'id': jurisdiction3_id,
            'name': "Боевое Подразделение"
        }, {
            'id': jurisdiction4_id,
            'name': "Штабное Подразделение"
        }, {
            'id': jurisdiction5_id,
            'name': "Кандидаты"
        }, {
            'id': jurisdiction6_id,
            'name': "Курьируемые сотрудники"
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

    op.bulk_insert(
        Base.metadata.tables['staff_functions'],
        [{
            'id': staff_function1_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Инициатор приказа о назначении',
            'jurisdiction_id': jurisdiction_id,
            'priority': 1,
            'role_id': doc_type5_id
        },
        {
            'id': staff_function2_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Эксперт приказа о назначении',
            'jurisdiction_id': jurisdiction_id,
            'priority': 2,
            'role_id': doc_type2_id
        },
        {
            'id': staff_function3_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Утверждающий приказа о назначении',
            'jurisdiction_id': jurisdiction_id,
            'priority': 100,
            'role_id': doc_type3_id
        },
        {
            'id': staff_function4_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Инициатор приказа о присвоения звания',
            'jurisdiction_id': jurisdiction_id,
            'priority': 1,
            'role_id': doc_type5_id
        },
        {
            'id': staff_function5_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Эксперт приказа о присвоения звания',
            'jurisdiction_id': jurisdiction_id,
            'priority': 2,
            'role_id': doc_type2_id
        },
        {
            'id': staff_function6_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Утверждающий приказа о присвоения звания',
            'jurisdiction_id': jurisdiction_id,
            'priority': 100,
            'role_id': doc_type3_id
        },
        {
            'id': staff_function7_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Инициатор приказа о присвоения черного берета',
            'jurisdiction_id': jurisdiction_id,
            'priority': 1,
            'role_id': doc_type5_id
        },
        {
            'id': staff_function8_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Эксперт приказа о присвоения черного берета',
            'jurisdiction_id': jurisdiction_id,
            'priority': 2,
            'role_id': doc_type2_id
        },
        {
            'id': staff_function9_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Утверждающий приказа о присвоения черного берета',
            'jurisdiction_id': jurisdiction_id,
            'priority': 100,
            'role_id': doc_type3_id
        }, {
            'id': staff_function10_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Согласующий приказа о присвоения звания',
            'jurisdiction_id': jurisdiction_id,
            'priority': 3,
            'role_id': doc_type1_id
        }, {
            'id': staff_function11_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Согласующий приказа о присвоения черного берета',
            'jurisdiction_id': jurisdiction_id,
            'priority': 3,
            'role_id': doc_type1_id
        }, {
            'id': staff_function12_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Согласующий приказа о назначении',
            'jurisdiction_id': jurisdiction_id,
            'priority': 3,
            'role_id': doc_type1_id
        }]
    )

    # Personal tables

    op.bulk_insert(
        Base.metadata.tables['sport_types'],
        [{
            'id': sport_type1_id,
            'name': "Бокс"
        }, {
            'id': sport_type2_id,
            'name': "Карате"
        }, {
            'id': sport_type3_id,
            'name': "Джиу-Джитсу"
        }]
    )

    # Educational tables

    op.bulk_insert(
        Base.metadata.tables['academic_degree_degrees'],
        [{
            'id': academic_degree_degree1_id,
            'name': "Доктор Наук (PhD)"
        }, {
            'id': academic_degree_degree2_id,
            'name': "Кандидат Доктора Наук"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['academic_title_degrees'],
        [{
            'id': academic_title_degree1_id,
            'name': "Профессор"
        }, {
            'id': academic_title_degree2_id,
            'name': "Доцент"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['course_providers'],
        [{
            'id': course_provider1_id,
            'name': "StepUp academy"
        }, {
            'id': course_provider2_id,
            'name': "Udemy.com"
        }, {
            'id': course_provider3_id,
            'name': "Coursera.com"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['institution_degree_types'],
        [{
            'id': institution_degree_type1_id,
            'name': "Среднее"
        }, {
            'id': institution_degree_type2_id,
            'name': "Бакалавриат"
        }, {
            'id': institution_degree_type3_id,
            'name': "Магистратура"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['sciences'],
        [{
            'id': science1_id,
            'name': "Психологическая Наука"
        }, {
            'id': science2_id,
            'name': "Военная Наука"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['specialties'],
        [{
            'id': specialty1_id,
            'name': "Нейронные связи"
        }, {
            'id': specialty2_id,
            'name': "Квантовая физика"
        }, {
            'id': specialty3_id,
            'name': "Биохимия"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['languages'],
        [{
            'id': language1_id,
            'name': "Казахский язык"
        }, {
            'id': language2_id,
            'name': "Английский язык"
        }, {
            'id': language3_id,
            'name': "Русский язык"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['institutions'],
        [{
            'id': institution1_id,
            'name': 'Лицей "Бiлiм-Инновация"'
        }, {
            'id': institution2_id,
            'name': "Astana IT University"
        }]
    )

# Additional profile tables

    op.bulk_insert(
        Base.metadata.tables['countries'],
        [{
            'id': country_id,
            'name': "Турция"
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['property_types'],
        [{
            'id': property_type1_id,
            'name': "Двухэтажный дом"
        }, {
            'id': property_type2_id,
            'name': "1-комнтаная квартира"
        }, {
            'id': property_type3_id,
            'name': "2-комнатная квартира"
        }]
    )
    
    group1_id = get_uuid()
    group2_id = get_uuid()
    group3_id = get_uuid()
    group4_id = get_uuid()
    group5_id = get_uuid()
    group6_id = get_uuid()
    group7_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['staff_divisions'],
        [{
            'parent_group_id': None,
            'id': group1_id,
            'name': "Департамент 1",
            'is_combat_unit': True
        }, {
            'parent_group_id': group1_id,
            'id': group2_id,
            'name': "Управление 1",
            'is_combat_unit': False
        }, {
            'parent_group_id': group1_id,
            'id': group3_id,
            'name': "Управление 2",
            'is_combat_unit': True
        }, {
            'parent_group_id': group1_id,
            'id': group4_id,
            'name': "Управление 3",
            'is_combat_unit': False
        }, {
            'parent_group_id': group1_id,
            'id': group5_id,
            'name': "Управление 4",
            'is_combat_unit': True
        }, {
            'parent_group_id': None,
            'id': group6_id,
            'name': "Особая группа",
            'is_combat_unit': False
        }, {
            'parent_group_id': group6_id,
            'id': group7_id,
            'name': "Кандидаты",
            'is_combat_unit': False
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

    op.bulk_insert(
        Base.metadata.tables['staff_units'],
        [{
            'id': staff_unit12_id,
            'user_id': None,
            'position_id': position5_id,
            'staff_division_id': group1_id
        }, {
            'id': staff_unit13_id,
            'user_id': None,
            'position_id': position3_id,
            'staff_division_id': group2_id
        }, {
            'id': staff_unit14_id,
            'user_id': None,
            'position_id': position4_id,
            'staff_division_id': group3_id
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['family_statuses'],
        [{
            'id': family_status_id,
            'name': "Женат / Замужем",
        }, {
            'id': family_status2_id,
            'name': "Не женат / Не замужем",
        }, {
            'id': family_status3_id,
            'name': "Разведен-а",
        }, {
            'id': family_status4_id,
            'name': "Вдовец / Вдова",
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['family_relations'],
        [{
            'id': family_relation_id,
            'name': 'Отец'
        }, {
            'id': family_relation2_id,
            'name': 'Мать'
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['liberations'],
        [{
            'id': liberation_id,
            'name': 'Физические нагрузки'
        }, {
            'id': liberation2_id,
            'name': 'Дежурство'
        }]
    )

    user1_id = get_uuid()
    user2_id = get_uuid()
    user3_id = get_uuid()
    user4_id = get_uuid()
    user5_id = get_uuid()
    user6_id = get_uuid()
    user7_id = get_uuid()
    user8_id = get_uuid()
    user9_id = get_uuid()
    user10_id = get_uuid()
    user11_id = get_uuid()

    create_user(
        user10_id,
        "Бауыржан",
        "Маратов",
        'Алдиярович',
        'bauyrzhan@mail.ru',
        group1_id,
        None,
        "Альфа 10",
        '10',
        staff_unit10_id,
        rank3_id,
        staff_unit10_id,
        "http://192.168.0.169:8083/static/Dima.png",
        position4_id,
        True,
        "1.2.218K")
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
        "http://192.168.0.169:8083/static/Erzhan.png",
        position1_id,
        True,
        '1.2.213K')
    create_user(
        user2_id,
        "Ахат",
        "Ганыбаев",
        'Бауыржанович',
        'ahat@mail.ru',
        group3_id,
        user10_id,
        "Альфа 2",
        '2',
        staff_unit2_id,
        rank1_id,
        staff_unit2_id,
        "http://192.168.0.169:8083/static/Erzhan.png",
        position1_id,
        False,
        '1.2.213K')
    create_user(
        user3_id,
        "Асет",
        "Султанов",
        'Асланович',
        'aset@mail.ru',
        group3_id,
        user10_id,
        "Альфа 3",
        '3',
        staff_unit3_id,
        rank1_id,
        staff_unit3_id,
        "http://192.168.0.169:8083/static/Almaz.png",
        position1_id,
        True,
        '1.2.214K')
    create_user(
        user4_id,
        "Жасулан",
        "Данияров",
        'Дидарович',
        'zhasulan@mail.ru',
        group3_id,
        user10_id,
        "Альфа 4",
        '4',
        staff_unit4_id,
        rank2_id,
        staff_unit4_id,
        "http://192.168.0.169:8083/static/Adil.png",
        position2_id,
        False,
        "1.2.214K")
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
        "http://192.168.0.169:8083/static/Almaz.png",
        position1_id,
        True,
        "1.2.215K")
    create_user(
        user6_id,
        "Бексундет",
        "Бахтияров",
        'Ганиулы',
        'beksundet@mail.ru',
        group2_id,
        user10_id,
        "Альфа 6",
        '6',
        staff_unit6_id,
        rank3_id,
        staff_unit6_id,
        "http://192.168.0.169:8083/static/Ernazar.png",
        position2_id,
        False,
        '1.2.215K')
    create_user(
        user7_id,
        "Ерден",
        "Ескендиров",
        'Алматович',
        'erden@mail.ru',
        group2_id,
        user10_id,
        "Альфа 7",
        '7',
        staff_unit7_id,
        rank1_id,
        staff_unit7_id,
        "http://192.168.0.169:8083/static/Nurlan.png",
        position1_id,
        True,
        '1.2.215K')
    create_user(
        user8_id,
        "Еркин",
        "Рахатов",
        'Серикович',
        'erkin@mail.ru',
        group3_id,
        None,
        "Альфа 8",
        '8',
        staff_unit8_id,
        rank1_id,
        staff_unit8_id,
        "http://192.168.0.169:8083/static/Erdaulet.png",
        position1_id,
        False,
        "1.2.216K")
    create_user(
        user9_id,
        "Арман",
        "Бауыржанов",
        'Уланович',
        'arman@mail.ru',
        group3_id,
        user10_id,
        "Альфа 9",
        '9',
        staff_unit9_id,
        rank1_id,
        staff_unit9_id,
        "http://192.168.0.169:8083/static/Erdaulet.png",
        position3_id,
        True,
        "1.2.217K")
    create_user(
        str(uuid.uuid4()),
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
        "http://192.168.0.169:8083/static/Erdaulet.png",
        position4_id,
        False,
        '1.2.100K')


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
        }]
    )

    template1_id = get_uuid()
    template2_id = get_uuid()
    template3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_document_templates'],
        [{
            'name': 'Приказ о назначении',
            'path': 'http://192.168.0.169:8083/static/%D0%9F%D1%80%D0%B8%D0%BA%D0%B0%D0%B7%20%D0%BE%20%D0%BD%D0%B0%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B8.docx',
            'subject_type': 1,
            'properties': {
                "signed_at": {
                    "alias_name": "Дата подписания",
                    "type": "read",
                    "data_taken": "auto"
                },
                "reg_number": {
                    "alias_name": "Регистрационный номер",
                    "type": "read",
                    "data_taken": "auto"
                },
                "rank": {
                    "alias_name": "Звание субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "last_name": {
                    "alias_name": "Фамилия субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "first_name": {
                    "alias_name": "Имя субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "father_name": {
                    "alias_name": "Отчество субъекта",
                    "type": "read",
                    "data_taken": "auto"
                }, 
                "id_number": {
                    "alias_name": "Идентификационный номер субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "new_position": {
                    "alias_name": "Новая позиция субъекта",
                    "type": "write",
                    "data_taken": "dropdown",
                    "field_name": "staff_unit"
                },
                "department_name": {
                    "alias_name": "Департамент субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "reason": {
                    "alias_name": "Причина",
                    "type": "read",
                    "data_taken": "manual"
                },
                "number": {
                    "alias_name": "Процент",
                    "type": "read",
                    "data_taken": "manual"
                }
            },
            'id': template1_id
        }, {
            'name': 'Приказ о присвоения звания',
            'path': 'http://192.168.0.169:8083/static/%D0%9F%D1%80%D0%B8%D0%BA%D0%B0%D0%B7_%D0%BE_%D0%BF%D1%80%D0%B8%D1%81%D0%B2%D0%BE%D0%B5%D0%BD%D0%B8%D0%B8_%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_%D0%BF%D0%BE%D0%B2%D1%8B%D1%88%D0%B5%D0%BD%D0%B8%D0%B5.docx',
            'subject_type': 1,
            'properties': {
                "signed_at": {
                    "alias_name": "Дата подписания",
                    "type": "read",
                    "data_taken": "auto"
                },
                "reg_number": {
                    "alias_name": "Регистрационный номер",
                    "type": "read",
                    "data_taken": "auto"
                },
                "last_name": {
                    "alias_name": "Фамилия субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "first_name": {
                    "alias_name": "Имя субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "father_name": {
                    "alias_name": "Отчество субъекта",
                    "type": "read",
                    "data_taken": "auto"
                }, 
                "id_number": {
                    "alias_name": "Идентификационный номер субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "new_position": {
                    "alias_name": "Новая позиция субъекта",
                    "type": "write",
                    "data_taken": "dropdown",
                    "field_name": "rank"
                }
            },
            'id': template2_id
        }, {
            'name': 'Приказ о присвоения черного берета',
            'path': 'http://192.168.0.169:8083/static/%D0%9F%D1%80%D0%B8%D0%BA%D0%B0%D0%B7_%D0%BE_%D0%BF%D1%80%D0%B8%D1%81%D0%B2%D0%BE%D0%B5%D0%BD%D0%B8%D0%B8_%D0%A7%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE_%D0%B1%D0%B5%D1%80%D0%B5%D1%82%D0%B0.docx',
            'subject_type': 1,  
            'properties': {
                "signed_at": {
                    "alias_name": "Дата подписания",
                    "type": "read",
                    "data_taken": "auto"
                },
                "reg_number": {
                    "alias_name": "Регистрационный номер",
                    "type": "read",
                    "data_taken": "auto"
                },
                "last_name": {
                    "alias_name": "Фамилия субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "first_name": {
                    "alias_name": "Имя субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "father_name": {
                    "alias_name": "Отчество субъекта",
                    "type": "read",
                    "data_taken": "auto"
                }, 
                "id_number": {
                    "alias_name": "Идентификационный номер субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "position": {
                    "alias_name": "Позиция субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "department_name": {
                    "alias_name": "Департамент субъекта",
                    "type": "read",
                    "data_taken": "auto"
                },
                "badge": {
                    "alias_name": "Черный берет",
                    "type": "write",
                    "data_taken": "auto",
                    "field_name": "badges",
                    "value": badge1_id
                }
            },
            'id': template3_id
        }]
    )

    step1_1 = get_uuid()
    step1_2 = get_uuid()
    step1_3 = get_uuid()
    step1_4 = get_uuid()
    step2_1 = get_uuid()
    step2_2 = get_uuid()
    step2_3 = get_uuid()
    step2_4 = get_uuid()
    step3_1 = get_uuid()
    step3_2 = get_uuid()
    step3_3 = get_uuid()
    step3_4 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_document_steps'],
        [{
            'hr_document_template_id': template1_id,
            'previous_step_id': None,
            'staff_function_id': staff_function1_id,
            'id': step1_1
        }, {
            'hr_document_template_id': template1_id,
            'previous_step_id': step1_1,
            'staff_function_id': staff_function2_id,
            'id': step1_2
        }, {
            'hr_document_template_id': template1_id,
            'previous_step_id': step1_2,
            'staff_function_id': staff_function12_id,
            'id': step1_3
        }, {
            'hr_document_template_id': template1_id,
            'previous_step_id': step1_2,
            'staff_function_id': staff_function3_id,
            'id': step1_4
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': None,
            'staff_function_id': staff_function4_id,
            'id': step2_1
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': step2_1,
            'staff_function_id': staff_function5_id,
            'id': step2_2
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': step2_2,
            'staff_function_id': staff_function10_id,
            'id': step2_3
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': step2_2,
            'staff_function_id': staff_function6_id,
            'id': step2_4
        }, {
            'hr_document_template_id': template3_id,
            'previous_step_id': None,
            'staff_function_id': staff_function7_id,
            'id': step3_1
        }, {
            'hr_document_template_id': template3_id,
            'previous_step_id': step3_1,
            'staff_function_id': staff_function8_id,
            'id': step3_2
        }, {
            'hr_document_template_id': template3_id,
            'previous_step_id': step3_2,
            'staff_function_id': staff_function11_id,
            'id': step3_3
        }, {
            'hr_document_template_id': template3_id,
            'previous_step_id': step3_2,
            'staff_function_id': staff_function9_id,
            'id': step3_4
        }]
    )

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
            'name': 'Оперативная служба СГО РК'
        }, {
            'id': candidate_category2_id,
            'name': 'Оперативная воинская служба СОО СГО РК'
        }, {
            'id': candidate_category3_id,
            'name': 'Оперативно-постовая служба СГО РК'
        }, {
            'id': candidate_category4_id,
            'name': 'Оперативно-постовая воинская служба СОО СГО РК'
        }, {
            'id': candidate_category5_id,
            'name': 'Оперативно-техническая и информационно-аналитическая служба СГО РК '
        }, {
            'id': candidate_category6_id,
            'name': 'Оперативно-техническая и информационно-аналитическая воинская служба СОО СГО РК'
        }, {
            'id': candidate_category7_id,
            'name': 'Инжерено-техническая, медицинская, административная и хозяйственная служба СГО РК'
        }, {
            'id': candidate_category8_id,
            'name': 'Инжерено-техническая, медицинская, административная и хозяйственная воинская служба СОО СГО РК'
        }, {
            'id': candidate_category9_id,
            'name': 'Водители службы СГО РК'
        }, {
            'id': candidate_category10_id,
            'name': 'Водители воинской службы СОО СГО РК'
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

    op.bulk_insert(
        Base.metadata.tables['candidate_stage_types'],
        [{
            'id': candidate_stage_types1_id,
            'name': 'Первичная беседа'
        }, {
            'id': candidate_stage_types2_id,
            'name': 'Дополнительная беседа по необходимости'
        }, {
            'id': candidate_stage_types3_id,
            'name': 'Запросы с внешних источников (др. гос органы)'
        }, {
            'id': candidate_stage_types4_id,
            'name': 'Беседа о религии'
        }, {
            'id': candidate_stage_types5_id,
            'name': 'Беседа с родителями'
        }, {
            'id': candidate_stage_types6_id,
            'name': 'Беседа о проф. пригодности'
        }, {
            'id': candidate_stage_types7_id,
            'name': 'Справка по результатам оперативного задания'
        }, {
            'id': candidate_stage_types8_id,
            'name': 'Беседа с психологом'
        }, {
            'id': candidate_stage_types9_id,
            'name': 'Беседа с УСБ'
        }, {
            'id': candidate_stage_types10_id,
            'name': 'Беседа с руководителем структурного подразделения'
        }, {
            'id': candidate_stage_types11_id,
            'name': 'Беседа с руководителем руководством департамента кадров'
        }, {
            'id': candidate_stage_types12_id,
            'name': 'Рецензия на эссе'
        }, {
            'id': candidate_stage_types13_id,
            'name': 'Военной врачебная комиссия '
        }, {
            'id': candidate_stage_types14_id,
            'name': 'Результаты физической подготовки'
        }, {
            'id': candidate_stage_types15_id,
            'name': 'Результаты полиграфического исследования'
        }, {
            'id': candidate_stage_types16_id,
            'name': 'Заключение по спец. проверке'
        }, {
            'id': candidate_stage_types17_id,
            'name': 'Заключение о зачислении '
        }]
    )

    candidate_stage_question1_id = get_uuid()
    candidate_stage_question2_id = get_uuid()
    candidate_stage_question3_id = get_uuid()
    candidate_stage_question4_id = get_uuid()
    candidate_stage_question5_id = get_uuid()
    candidate_stage_question6_id = get_uuid()
    candidate_stage_question7_id = get_uuid()
    candidate_stage_question8_id = get_uuid()
    candidate_stage_question9_id = get_uuid()
    candidate_stage_question10_id = get_uuid()
    candidate_stage_question11_id = get_uuid()
    candidate_stage_question12_id = get_uuid()
    candidate_stage_question13_id = get_uuid()
    candidate_stage_question14_id = get_uuid()
    candidate_stage_question15_id = get_uuid()
    candidate_stage_question16_id = get_uuid()
    candidate_stage_question17_id = get_uuid()
    candidate_stage_question18_id = get_uuid()
    candidate_stage_question19_id = get_uuid()
    candidate_stage_question20_id = get_uuid()
    candidate_stage_question21_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['candidate_stage_questions'],
        [{
            'id': candidate_stage_question1_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Кем подобран и кем рекомендован',
        }, {
            'id': candidate_stage_question2_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Краткие сведения из автобиографии',
            'description': '(о рождении, школе, учебе в колледже/ВУЗе, срочной службе, трудовой деятельности)'
        }, {
            'id': candidate_stage_question3_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Как характеризуется с последнего места работы',
            'description': '(сведения из характеристики с места работы)'
        }, {
            'id': candidate_stage_question4_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Доведение требований к службе в СГО РК',
        }, {
            'id': candidate_stage_question5_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Мотив кандидата на службу в СГО РК',
        }, {
            'id': candidate_stage_question6_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Рекомендация кандидату (читать газеты, смотреть мировые новости и тд.)',
        }, {
            'id': candidate_stage_question7_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Сведения о родственниках кандидата',
        }, {
            'id': candidate_stage_question8_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Дополнительные сведения (физическая подготовка)',
        }, {
            'id': candidate_stage_question9_id,
            'question_type': 'String',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Подведение итогов беседы',
        }, {
            'id': candidate_stage_question10_id,
            'question_type': 'Dropdown',
            'candidate_stage_type_id': candidate_stage_types1_id,
            'question': 'Категория кандидата',
        }, {
            'id': candidate_stage_question11_id,
            'question_type': 'Document',
            'candidate_stage_type_id': candidate_stage_types3_id,
            'question': None
        }, {
            'id': candidate_stage_question12_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types4_id,
            'question': None
        }, {
            'id': candidate_stage_question13_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types5_id,
            'question': None
        }, {
            'id': candidate_stage_question14_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types2_id,
            'question': None
        }, {
            'id': candidate_stage_question15_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types9_id,
            'question': None
        }, {
            'id': candidate_stage_question16_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types11_id,
            'question': None
        }, {
            'id': candidate_stage_question17_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types12_id,
            'question': None
        }, {
            'id': candidate_stage_question18_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types16_id,
            'question': None
        }, {
            'id': candidate_stage_question19_id,
            'question_type': 'Text',
            'candidate_stage_type_id': candidate_stage_types17_id,
            'question': None
        }, {
            'id': candidate_stage_question20_id,
            'question_type': 'Choice',
            'candidate_stage_type_id': candidate_stage_types13_id,
            'question': None
        }, {
            'id': candidate_stage_question21_id,
            'question_type': 'Choice',
            'candidate_stage_type_id': candidate_stage_types15_id,
            'question': None
        }]
    )

    candidate_stage_info_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['candidate_stage_infos'],
        [{
            'id': candidate_stage_info_id,
            'staff_unit_coordinate_id': staff_unit1_id,
            'candidate_stage_type_id': candidate_stage_types1_id,
            'is_waits': True
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
                cabinet):
    op.bulk_insert(
        Base.metadata.tables['staff_units'],
        [{
            'id': staff_unit_id,
            'user_id': id,
            'position_id': position_id,
            'staff_division_id': group_id
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
            'supervised_by': supervised_by,
            'call_sign': call_sign,
            'id_number': number,
            'phone_number': '+7 (777) 123-47-89',
            'rank_id': rank_id,
            'actual_staff_unit_id': actual_staff_unit_id,
            'status': "На работе",
            'icon': icon,
            'service_phone_number': "679-258",
            'personal_id': number,
            'is_military': is_military,
            'cabinet': cabinet
        }]
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
            'document_link': "document_link",
            'assignment_date': "2022-10-07"
        }, {
            'id': academic_degree2_id,
            'profile_id': educational_profile_id,
            'degree_id': academic_degree_degree2_id,
            'science_id': science2_id,
            'specialty_id': specialty2_id,
            'document_number': 2,
            'document_link': "document_link",
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
            'document_link': "document_link",
            'assignment_date': "2022-12-12"
        }, {
            'id': academic_title2_id,
            'profile_id': educational_profile_id,
            'degree_id': academic_title_degree2_id,
            'specialty_id': specialty2_id,
            'document_number': '123123',
            'document_link': "document_link",
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
            'profile_id': educational_profile_id,
            'course_provider_id': course_provider1_id,
            'specialty_id': specialty1_id,
            'document_number': 1,
            'document_link': "document_link",
            'assignment_date': "2022-12-12",
            'start_date': '2019-10-12',
            'end_date': '2019-12-10'
        }, {
            'id': course2_id,
            'name': "Курсы по подготовке к стрельбе",
            'profile_id': educational_profile_id,
            'course_provider_id': course_provider2_id,
            'specialty_id': specialty2_id,
            'document_number': 2,
            'document_link': "document_link",
            'assignment_date': "2022-12-13",
            'start_date': '2020-11-25',
            'end_date': '2020-12-15'
        }, {
            'id': course3_id,
            'name': "Front-End курс",
            'profile_id': educational_profile_id,
            'course_provider_id': course_provider3_id,
            'specialty_id': specialty3_id,
            'document_number': 3,
            'document_link': "document_link",
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
            'assignment_date': '2022-10-09',
            'document_link': 'document_link1',
            'sport_type_id': sport_type1_id
        }, {
            'id': sport_degree2_id,
            'profile_id': personal_profile_id,
            'name': "Мастер спорта по карате",
            'assignment_date': '2022-10-10',
            'document_link': 'document_link2',
            'sport_type_id': sport_type2_id
        }, {
            'id': sport_degree3_id,
            'profile_id': personal_profile_id,
            'name': "Кандидат мастер спорта по джиу-джитсу",
            'assignment_date': '2022-10-11',
            'document_link': 'document_link3',
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
            'assignment_date': '2022-10-09',
            'document_link': 'document_link1',
            'sport_type_id': sport_type3_id
        }, {
            'id': sport_achievement2_id,
            'profile_id': personal_profile_id,
            'name': "I место в Чемпионате Мира по боксу",
            'assignment_date': '2022-10-10',
            'document_link': 'document_link2',
            'sport_type_id': sport_type1_id
        }, {
            'id': sport_achievement3_id,
            'profile_id': personal_profile_id,
            'name': "II место в Чемпионате города Астаны по карате",
            'assignment_date': '2022-10-11',
            'document_link': 'document_link3',
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
            'date_birth': '1990-01-23',
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
            'document_link': "document_link",
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
            'document_link': "document_link",
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
            'document_link': "document_link",
            'profile_id': personal_profile_id
        }]
    )

    general_user_information_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['general_user_informations'],
        [{
            'id':general_user_information_id,
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
            'initiator': 'Республиканская больница',
            'start_date': "2022-09-12",
            'profile_id': medical_profile_id,
            'document_link': "document_link"
        }, {
            'id': dispensary_registrations1_id,
            'name': "Сахарный Диабет",
            'initiator': 'Клиника "Нурсултан"',
            'start_date': "2022-12-15",
            'profile_id': medical_profile_id,
            'document_link': "document_link"
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
            'reason': "Больничный (код-829121)",
            'place': 'ГКП на ПХВ "Городская поликлиника №3"',
            'start_date': "2022-09-12",
            'end_date': "2022-10-12",
            'profile_id': medical_profile_id,
            'document_link': "document_link"
        }, {
            'id': hospital_datas1_id,
            'reason': "Больничный по причине ОРВИ",
            'place': 'ГКП на ПХВ "Городская поликлиника №3"',
            'start_date': "2022-12-15",
            'end_date': "2022-12-16",
            'profile_id': medical_profile_id,
            'document_link': "document_link"
        }]
    )

    violations_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['violations'],
        [{
            'id': violations_id,
            'name': "Мелкое хулиганство",
            'date': "2022-09-12",
            'issued_by': "Районный суд Сарыаркинского района г.Астана",
            'article_number': "122.12(УК РК)",
            'consequence': "Штраф 40МРП",
            'profile_id': additional_profile_id
        }]
    )

    properties_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['properties'],
        [{
            'id': properties_id,
            'type_id': property_type1_id,
            'purchase_date': "2022-09-12",
            'address': "Достык 5",
            'profile_id': additional_profile_id
        }]
    )

    abroad_travels_id = get_uuid()

    op.bulk_insert(      
        Base.metadata.tables['abroad_travels'],
        [{
            'id': abroad_travels_id,
            'vehicle_type': "Самолет",
            'destination_country_id': country_id,
            'date_from': "2022-05-10",
            'date_to': "2022-05-11",
            'reason': "Служебная командировка",
            'document_link':"document_link",
            'profile_id': additional_profile_id

        }]
    )

    op.bulk_insert(
        Base.metadata.tables['service_housings'],
        [{
            'id': get_uuid(),
            'type_id': property_type2_id,
            'address': "Dostyk 5",
            'issue_date': "2022-09-12",
            'profile_id': additional_profile_id
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
                'document_link': "document_link",
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
            'document_link': "document_link",
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
            "document_link": "document_link",
            'profile_id': additional_profile_id
        }]
    )

    families_profile_id = get_uuid()


    op.bulk_insert(
        Base.metadata.tables['families'],
        [{
            'id': families_profile_id,
            'relation_id': family_relation_id,
            'first_name': options[email]['first_name'],
            'last_name': 'Темирбеков',
            'father_name': options[email]['father_name'],
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



def downgrade() -> None:
    pass
