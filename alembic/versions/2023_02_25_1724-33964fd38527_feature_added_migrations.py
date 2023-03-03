"""feature: added migrations

Revision ID: 33964fd38527
Revises: f2bfe17f02b7
Create Date: 2023-02-25 17:24:21.028216

"""
import uuid

import sqlalchemy as sa

from alembic import op
from core import Base

# revision identifiers, used by Alembic.
revision = '33964fd38527'
down_revision = 'f2bfe17f02b7'
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
        Base.metadata.tables['staff_units'],
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
                position1_id,
                rank1_id,
                position1_id,
                "http://192.168.0.199:8083/static/Erzhan.png"),
            create_user(
                user2_id,
                "Ахат",
                "Наурызбаев",
                'Саматович',
                'ahat@mail.ru',
                group3_id,
                "Альфа 2",
                '2',
                position1_id,
                rank1_id,
                position1_id,
                "http://192.168.0.199:8083/static/Erzhan.png"),
            create_user(
                user3_id,
                "Асет",
                "Наурызбаев",
                'Асланович',
                'aset@mail.ru',
                group3_id,
                "Альфа 3",
                '3',
                position1_id,
                rank1_id,
                position1_id,
                "http://192.168.0.199:8083/static/Almaz.png"),
            create_user(
                user4_id,
                "Жасулан",
                "Наурызбеков",
                'Дидарович',
                'zhasulan@mail.ru',
                group3_id,
                "Альфа 4",
                '4',
                position2_id,
                rank2_id,
                position2_id,
                "http://192.168.0.199:8083/static/Adil.png"),
            create_user(
                user5_id,
                "Ануар",
                "Наурызбеков",
                'Дидарович',
                'anuar@mail.ru',
                group2_id,
                "Альфа 5",
                '5',
                position1_id,
                rank1_id,
                position1_id,
                "http://192.168.0.199:8083/static/Almaz.png"),
            create_user(
                user6_id,
                "Бексундет",
                "Наурызбеков",
                'Дидарович',
                'beksundet@mail.ru',
                group2_id,
                "Альфа 6",
                '6',
                position3_id,
                rank2_id,
                position3_id,
                "http://192.168.0.199:8083/static/Ernazar.png"),
            create_user(
                user7_id,
                "Ерден",
                "Наурызбеков",
                'Алматович',
                'erden@mail.ru',
                group2_id,
                "Альфа 7",
                '7',
                position1_id,
                rank1_id,
                position1_id,
                "http://192.168.0.199:8083/static/Nurlan.png"),
            create_user(
                user8_id,
                "Еркин",
                "Наурызбеков",
                'Дидарович',
                'erkin@mail.ru',
                group3_id,
                "Альфа 8",
                '8',
                position1_id,
                rank1_id,
                position1_id,
                "http://192.168.0.199:8083/static/Erdaulet.png"),
            create_user(
                user9_id,
                "Арман",
                "Наурызбеков",
                'Алматович',
                'arman@mail.ru',
                group3_id,
                "Альфа 9",
                '9',
                position1_id,
                rank1_id,
                position1_id,
                "http://192.168.0.199:8083/static/Erdaulet.png"),
            create_user(
                user10_id,
                "Бауыржан",
                "Наурызбеков",
                'Алматович',
                'bauyrzhan@mail.ru',
                group3_id,
                "Альфа 10",
                '10',
                position4_id,
                rank3_id,
                position4_id,
                "http://192.168.0.199:8083/static/Dima.png"),
            create_user(
                str(uuid.uuid4()),
                "Админ",
                "Админов",
                "Админович",
                'admin@mail.com',
                group3_id,
                'admin',
                '123456789',
                position4_id,
                rank3_id,
                position4_id,
                "http://192.168.0.199:8083/static/Erdaulet.png")
        ]
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

    role_id = get_uuid()
    role2_id = get_uuid()
    role3_id = get_uuid()
    role4_id = get_uuid()
    role5_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['staff_functions'],
        [{
            'id': role_id,
            'name': "Согласующий",
            'discriminator': "document_staff_function",
            'hours_per_week': "2",
            'priority': "3",
            'role_id': doc_type1_id
        }, {
            'id': role2_id,
            'name': "Эксперт",
            'discriminator': "document_staff_function",
            'hours_per_week': "5",
            'priority': "2",
            'role_id': doc_type2_id
    }, {
            'id': role3_id,
            'name': "Утверждающий",
            'discriminator': "document_staff_function",
            'hours_per_week': "2",
            'priority': "100",
            'role_id': doc_type3_id,
        }, {
            'id': role4_id,
            'name': "Уведомляемый",
            'discriminator': "document_staff_function",
            'hours_per_week': "0",
            'priority': "-1",
            'role_id': doc_type4_id
        }, {
            'id': role5_id,
            'name': "Инициатор",
            'discriminator': "document_staff_function",
            'hours_per_week': "3",
            'priority': "1",
            'role_id': doc_type5_id
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
            'staff_unit_id': position2_id,
            'staff_function_id': role5_id,
            'id': step1_1
        }, {
            'hr_document_template_id': template1_id,
            'previous_step_id': step1_1,
            'staff_unit_id': position3_id,
            'staff_function_id': role2_id,
            'id': step1_2
        }, {
            'hr_document_template_id': template1_id,
            'previous_step_id': step1_2,
            'staff_unit_id': position4_id,
            'staff_function_id': role3_id,
            'id': step1_3
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': None,
            'staff_unit_id': position2_id,
            'staff_function_id': role5_id,
            'id': step2_1
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': step2_1,
            'staff_unit_id': position3_id,
            'staff_function_id': role2_id,
            'id': step2_2
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': step2_2,
            'staff_unit_id': position4_id,
            'staff_function_id': role3_id,
            'id': step2_3
        }, {
            'hr_document_template_id': template3_id,
            'previous_step_id': None,
            'staff_unit_id': position2_id,
            'staff_function_id': role5_id,
            'id': step3_1
        }, {
            'hr_document_template_id': template3_id,
            'previous_step_id': step3_1,
            'staff_unit_id': position3_id,
            'staff_function_id': role2_id,
            'id': step3_2
        }, {
            'hr_document_template_id': template3_id,
            'previous_step_id': step3_2,
            'staff_unit_id': position4_id,
            'staff_function_id': role3_id,
            'id': step3_3
        }]
    )


def get_uuid():
    return str(uuid.uuid4())


def create_user(id, name, surname, father_name, email, group_id, call_sign, number,  position_id, rank_id, actual_position_id, icon):
    return {
        'id': id,
        'email': email,
        'password': '$2b$12$vhg69KJxWiGgetoLxGRvie3VxElPt45i4ELJiE/V2qOj30X3c3.7m',
        'first_name': name,
        'last_name': surname,
        'father_name': father_name,
        'staff_division_id': group_id,
        'staff_unit_id': position_id,
        'call_sign': call_sign,
        'id_number': number,
        'phone_number': '+77771234789',
        'address': 'Мангилик Ел, 1',
        'rank_id': rank_id,
        'actual_staff_unit_id': actual_position_id,
        'status': "На работе",
        'icon': icon
    }


def downgrade() -> None:
    pass
