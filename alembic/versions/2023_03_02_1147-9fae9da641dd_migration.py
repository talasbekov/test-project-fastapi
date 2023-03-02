"""migration

Revision ID: 9fae9da641dd
Revises: f04c5daf7685
Create Date: 2023-03-02 11:47:59.787804

"""
import uuid

import sqlalchemy as sa

from alembic import op
from core import Base

# revision identifiers, used by Alembic.
revision = '9fae9da641dd'
down_revision = 'f04c5daf7685'
branch_labels = None
depends_on = None


def upgrade() -> None:

    badge1_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['badges'],
        [{
            "id": badge1_id,
            "name": "Черный Берет",
            "url": "http://192.168.0.199:8083/static/black_beret.jpg"
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

    op.bulk_insert(
        Base.metadata.tables['ranks'],
        [{
            'id': rank1_id,
            'name': 'Рядовой'
        }, {
            'id': rank2_id,
            'name': 'Младший сержант'
        }, {
            'id': rank3_id,
            'name': 'Сержант'
        }, {
            'id': rank4_id,
            'name': 'Старший сержант'
        }, {
            'id': rank5_id,
            'name': 'Лейтенант'
        }, {
            'id': rank6_id,
            'name': 'Старший лейтенант'
        }, {
            'id': rank7_id,
            'name': 'Капитан'
        }, {
            'id': rank8_id,
            'name': 'Майор'
        }, {
            'id': rank9_id,
            'name': 'Подполковник'
        }, {
            'id': rank10_id,
            'name': 'Полковник'
        }, {
            'id': rank11_id,
            'name': 'Генерал-майор'
        }, {
            'id': rank12_id,
            'name': 'Генерал-лейтенант'
        }, {
            'id': rank13_id,
            'name': 'Генерал-полковник'
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


    jurisdiction1_id = get_uuid()
    jurisdiction2_id = get_uuid()
    jurisdiction3_id = get_uuid()
    jurisdiction4_id = get_uuid()
    jurisdiction5_id = get_uuid()
    jurisdiction6_id = get_uuid()
    
    op.bulk_insert(
        Base.metadata.tables['jurisdictions'],
        [{
            'id': jurisdiction1_id,
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

    op.bulk_insert(
        Base.metadata.tables['staff_functions'],
        [{
            'id': staff_function1_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Инициатор приказа о назначении',
            'jurisdiction_id': jurisdiction1_id,
            'priority': 1
        },
        {
            'id': staff_function2_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Эксперт приказа о назначении',
            'jurisdiction_id': jurisdiction1_id,
            'priority': 2
        },
        {
            'id': staff_function3_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Утверждающий приказа о назначении',
            'jurisdiction_id': jurisdiction1_id,
            'priority': 100
        },
        {
            'id': staff_function4_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Инициатор приказа о присвоения звания',
            'jurisdiction_id': jurisdiction1_id,
            'priority': 1
        },
        {
            'id': staff_function5_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Эксперт приказа о присвоения звания',
            'jurisdiction_id': jurisdiction1_id,
            'priority': 2
        },
        {
            'id': staff_function6_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Утверждающий приказа о присвоения звания',
            'jurisdiction_id': jurisdiction1_id,
            'priority': 100
        },
        {
            'id': staff_function7_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Инициатор приказа о присвоения черного берета',
            'jurisdiction_id': jurisdiction1_id,
            'priority': 1
        },
        {
            'id': staff_function8_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Эксперт приказа о присвоения черного берета',
            'jurisdiction_id': jurisdiction1_id,
            'priority': 2
        },
        {
            'id': staff_function9_id,
            'hours_per_week' : 3,
            'discriminator': 'document_staff_function',
            'name' : 'Утверждающий приказа о присвоения черного берета',
            'jurisdiction_id': jurisdiction1_id,
            'priority': 100
        }]
    )


    group1_id = get_uuid()
    group2_id = get_uuid()
    group3_id = get_uuid()
    group4_id = get_uuid()
    group5_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['staff_divisions'],
        [{
            'parent_group_id': None,
            'id': group1_id,
            'name': "Департамент 1"
        }, {
            'parent_group_id': group1_id,
            'id': group2_id,
            'name': "Управление 1"
        }, {
            'parent_group_id': group1_id,
            'id': group3_id,
            'name': "Управление 2"
        }, {
            'parent_group_id': group1_id,
            'id': group4_id,
            'name': "Управление 3"
        }, {
            'parent_group_id': group1_id,
            'id': group5_id,
            'name': "Управление 4"
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

    op.bulk_insert(
        Base.metadata.tables['users'],
        [
            create_user(
                user1_id,
                "Адилет",
                "Наурызбаев",
                'Саматович',
                'adilet@mail.ru',
                group2_id,
                "Альфа 1",
                '1',
                staff_unit1_id,
                rank1_id,
                staff_unit1_id,
                "http://192.168.0.199:8083/static/Erzhan.png",
                position1_id),
            create_user(
                user2_id,
                "Ахат",
                "Наурызбаев",
                'Саматович',
                'ahat@mail.ru',
                group3_id,
                "Альфа 2",
                '2',
                staff_unit2_id,
                rank1_id,
                staff_unit2_id,
                "http://192.168.0.199:8083/static/Erzhan.png",
                position1_id),
            create_user(
                user3_id,
                "Асет",
                "Наурызбаев",
                'Асланович',
                'aset@mail.ru',
                group3_id,
                "Альфа 3",
                '3',
                staff_unit3_id,
                rank1_id,
                staff_unit3_id,
                "http://192.168.0.199:8083/static/Almaz.png",
                position1_id),
            create_user(
                user4_id,
                "Жасулан",
                "Наурызбеков",
                'Дидарович',
                'zhasulan@mail.ru',
                group3_id,
                "Альфа 4",
                '4',
                staff_unit4_id,
                rank2_id,
                staff_unit4_id,
                "http://192.168.0.199:8083/static/Adil.png",
                position2_id),
            create_user(
                user5_id,
                "Ануар",
                "Наурызбеков",
                'Дидарович',
                'anuar@mail.ru',
                group2_id,
                "Альфа 5",
                '5',
                staff_unit5_id,
                rank1_id,
                staff_unit5_id,
                "http://192.168.0.199:8083/static/Almaz.png",
                position1_id),
            create_user(
                user6_id,
                "Бексундет",
                "Наурызбеков",
                'Дидарович',
                'beksundet@mail.ru',
                group2_id,
                "Альфа 6",
                '6',
                staff_unit6_id,
                rank3_id,
                staff_unit6_id,
                "http://192.168.0.199:8083/static/Ernazar.png",
                position2_id),
            create_user(
                user7_id,
                "Ерден",
                "Наурызбеков",
                'Алматович',
                'erden@mail.ru',
                group2_id,
                "Альфа 7",
                '7',
                staff_unit7_id,
                rank1_id,
                staff_unit7_id,
                "http://192.168.0.199:8083/static/Nurlan.png",
                position1_id),
            create_user(
                user8_id,
                "Еркин",
                "Наурызбеков",
                'Дидарович',
                'erkin@mail.ru',
                group3_id,
                "Альфа 8",
                '8',
                staff_unit8_id,
                rank1_id,
                staff_unit8_id,
                "http://192.168.0.199:8083/static/Erdaulet.png",
                position1_id),
            create_user(
                user9_id,
                "Арман",
                "Наурызбеков",
                'Алматович',
                'arman@mail.ru',
                group3_id,
                "Альфа 9",
                '9',
                staff_unit9_id,
                rank1_id,
                staff_unit9_id,
                "http://192.168.0.199:8083/static/Erdaulet.png",
                position3_id),
            create_user(
                user10_id,
                "Бауыржан",
                "Наурызбеков",
                'Алматович',
                'bauyrzhan@mail.ru',
                group3_id,
                "Альфа 10",
                '10',
                staff_unit10_id,
                rank3_id,
                staff_unit10_id,
                "http://192.168.0.199:8083/static/Dima.png",
                position4_id),
            create_user(
                str(uuid.uuid4()),
                "Админ",
                "Админов",
                "Админович",
                'admin@mail.com',
                group3_id,
                'admin',
                '123456789',
                staff_unit11_id,
                rank3_id,
                staff_unit11_id,
                "http://192.168.0.199:8083/static/Erdaulet.png",
                position4_id)
        ]
    )

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
        }]
    )

    template1_id = get_uuid()
    template2_id = get_uuid()
    template3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_document_templates'],
        [{
            'name': 'Приказ о назначении',
            'path': 'http://192.168.0.199:8083/static/%D0%9F%D1%80%D0%B8%D0%BA%D0%B0%D0%B7%20%D0%BE%20%D0%BD%D0%B0%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B8.docx',
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
                "new_department_name": {
                    "alias_name": "Новый департамент субъекта",
                    "type": "write",
                    "data_taken": "matreshka",
                    "field_name":"staff_division"
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
            'path': 'http://192.168.0.199:8083/static/%D0%9F%D1%80%D0%B8%D0%BA%D0%B0%D0%B7_%D0%BE_%D0%BF%D1%80%D0%B8%D1%81%D0%B2%D0%BE%D0%B5%D0%BD%D0%B8%D0%B8_%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_%D0%BF%D0%BE%D0%B2%D1%8B%D1%88%D0%B5%D0%BD%D0%B8%D0%B5.docx',
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
                    "field_name": "staff_unit"
                }
            },
            'id': template2_id
        }, {
            'name': 'Приказ о присвоения черного берета',
            'path': 'http://192.168.0.199:8083/static/%D0%9F%D1%80%D0%B8%D0%BA%D0%B0%D0%B7_%D0%BE_%D0%BF%D1%80%D0%B8%D1%81%D0%B2%D0%BE%D0%B5%D0%BD%D0%B8%D0%B8_%D0%A7%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE_%D0%B1%D0%B5%D1%80%D0%B5%D1%82%D0%B0.docx',
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
    step2_1 = get_uuid()
    step2_2 = get_uuid()
    step2_3 = get_uuid()
    step3_1 = get_uuid()
    step3_2 = get_uuid()
    step3_3 = get_uuid()

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
            'staff_function_id': staff_function5_id,
            'id': step1_3
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': None,
            'staff_function_id': staff_function6_id,
            'id': step2_1
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': step2_1,
            'staff_function_id': staff_function5_id,
            'id': step2_2
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': step2_2,
            'staff_function_id': staff_function6_id,
            'id': step2_3
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
            'staff_function_id': staff_function9_id,
            'id': step3_3
        }]
    )


def get_uuid():
    return str(uuid.uuid4())


def create_user(id, name, surname, father_name, email, group_id, call_sign, number,  staff_unit_id, rank_id, actual_staff_unit_id, icon, position_id):
    op.bulk_insert(
        Base.metadata.tables['staff_units'],
        [{
            'id': staff_unit_id,
            'user_id': id,
            'position_id': position_id,
            'staff_division_id': group_id
        }]
    )

    return {
        'id': id,
        'email': email,
        'password': '$2b$12$vhg69KJxWiGgetoLxGRvie3VxElPt45i4ELJiE/V2qOj30X3c3.7m',
        'first_name': name,
        'last_name': surname,
        'father_name': father_name,
        'staff_unit_id': staff_unit_id,
        'call_sign': call_sign,
        'id_number': number,
        'phone_number': '+77771234789',
        'address': 'Мангилик Ел, 1',
        'rank_id': rank_id,
        'actual_staff_unit_id': actual_staff_unit_id,
        'status': "На работе",
        'icon': icon
    }


def downgrade() -> None:
    pass
