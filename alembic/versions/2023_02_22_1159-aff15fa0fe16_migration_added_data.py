"""migration: added data

Revision ID: aff15fa0fe16
Revises: f58b3d8b6a62
Create Date: 2023-02-22 11:59:27.005940

"""
import uuid

import sqlalchemy as sa

from alembic import op
from core import Base

# revision identifiers, used by Alembic.
revision = 'aff15fa0fe16'
down_revision = 'f58b3d8b6a62'
branch_labels = None
depends_on = None


def upgrade() -> None:

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
                "Наурыбаев",
                'adilet@mail.ru',
                group2_id,
                "Альфа 1",
                '1',
                position1_id,
                rank1_id,
                position1_id),
            create_user(
                user2_id,
                "Ахат",
                "Наурыбаев",
                'ahat@mail.ru',
                group3_id,
                "Альфа 2",
                '2',
                position1_id,
                rank1_id,
                position1_id),
            create_user(
                user3_id,
                "Асет",
                "Наурыбаев",
                'aset@mail.ru',
                group3_id,
                "Альфа 3",
                '3',
                position1_id,
                rank1_id,
                position1_id),
            create_user(
                user4_id,
                "Жасулан",
                "Наурыбеков",
                'zhasulan@mail.ru',
                group3_id,
                "Альфа 4",
                '4',
                position2_id,
                rank2_id,
                position2_id),
            create_user(
                user5_id,
                "Ануар",
                "Наурыбеков",
                'anuar@mail.ru',
                group2_id,
                "Альфа 5",
                '5',
                position1_id,
                rank1_id,
                position1_id),
            create_user(
                user6_id,
                "Бексундет",
                "Наурыбеков",
                'beksundet@mail.ru',
                group2_id,
                "Альфа 6",
                '6',
                position3_id,
                rank2_id,
                position3_id),
            create_user(
                user7_id,
                "Ерден",
                "Наурыбеков",
                'erden@mail.ru',
                group2_id,
                "Альфа 7",
                '7',
                position1_id,
                rank1_id,
                position1_id),
            create_user(
                user8_id,
                "Еркин",
                "Наурыбеков",
                'erkin@mail.ru',
                group3_id,
                "Альфа 8",
                '8',
                position1_id,
                rank1_id,
                position1_id),
            create_user(
                user9_id,
                "Арман",
                "Наурыбеков",
                'arman@mail.ru',
                group3_id,
                "Альфа 9",
                '9',
                position1_id,
                rank1_id,
                position1_id),
            create_user(
                user10_id,
                "Бауыржан",
                "Наурыбеков",
                'bauyrzhan@mail.ru',
                group3_id,
                "Альфа 10",
                '10',
                position4_id,
                rank3_id,
                position4_id),
            create_user(
                str(uuid.uuid4()),
                "Admin",
                "Adminov",
                'admin@mail.com',
                group3_id,
                'admin',
                '123456789',
                position4_id,
                rank3_id,
                position4_id)
        ]
    )

    template1_id = get_uuid()
    template2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_document_templates'],
        [{
            'name': 'Приказ о зачислении на службу',
            'path': 'static/templates/Приказ о зачислении на службу (1).docx',
            'subject_type': 1,
            'properties': {
                "signed_at": {
                    "alias_name": "Время Регистрации",
                    "type": "read",
                    "data_taken": "auto"
                },
                "reg_number": {
                    "alias_name": "Регистрационный номер",
                    "type": "read",
                    "data_taken": "auto"
                },
                "rank": {
                    "alias_name": "Звание",
                    "type": "read",
                    "data_taken": "auto"
                },
                "first_name": {
                    "alias_name": "Имя",
                    "type": "read",
                    "data_taken": "auto"
                },
                "last_name": {
                    "alias_name": "Фамилия",
                    "type": "read",
                    "data_taken": "auto"
                },
                "father_name": {
                    "alias_name": "Имя",
                    "type": "read",
                    "data_taken": "auto"
                },
                "id_number": {
                    "alias_name": "ID",
                    "type": "read",
                    "data_taken": "auto"
                },
                "period": {
                    "alias_name": "Период",
                    "type": "read", # пока нет логики на время
                    "data_taken": "manual"
                },
                "new_rank": {
                    "alias_name": "Новое звание",
                    "type": "write",
                    "field_name": "rank",
                    "data_taken": "manual"
                },
                "department_name": {
                    "alias_name": "Департамент",
                    "type": "write",
                    "field_name": "group",
                    "data_taken": "dropdown"
                },
                "position": {
                    "alias_name": "Позиция",
                    "type": "write",
                    "field_name": "position",
                    "data_taken": "dropdown"
                },
                "position_id": {
                    "alias_name": "ID позиции",
                    "type": "read",
                    "data_taken":"auto"
                }
            },
            'id': template1_id
        }, {
            'name': 'Приказ о выходе в отпуск (рук.состав)',
            'path': 'static/templates/Приказ_о_выходе_в_отпуск_рук_состав.docx',
            'subject_type': 1,
            'properties': {
                "signed_at": {
                    "alias_name": "Время Регистрации",
                    "type": "read",
                    "data_taken": "auto"
                },
                "reg_number": {
                    "alias_name": "Регистрационный номер",
                    "type": "read",
                    "data_taken": "auto"
                },
                "rank": {
                    "alias_name": "Звание",
                    "type": "read",
                    "data_taken": "auto"
                },
                "first_name": {
                    "alias_name": "Имя",
                    "type": "read",
                    "data_taken": "auto"
                },
                "last_name": {
                    "alias_name": "Фамилия",
                    "type": "read",
                    "data_taken": "auto"
                },
                "father_name": {
                    "alias_name": "Имя",
                    "type": "read",
                    "data_taken": "auto"
                },
                "id_number": {
                    "alias_name": "ID",
                    "type": "read",
                    "data_taken": "auto"
                },
                "department_name": {
                    "alias_name": "Департамент",
                    "type": "read",
                    "data_taken": "auto"
                },
                "start_date": {
                    "alias_name": "Начало",
                    "type": "read",
                    "data_taken": "date_picker",
                },
                "end_date": {
                    "alias_name": "Конец",
                    "type": "write",
                    "data_taken": "date_picker",
                    "field_name": "status_till"  # Нет логики на создание event-а
                },
                "responsible_subject_rank": {
                    "alias_name": "Ранк заменяющего",
                    "type": "read",
                    "data_taken": "dropdown",
                },
                "responsible_subject_last_name": {
                    "alias_name": "Фамилия заменяющего",
                    "type": "read",
                    "data_taken": "dropdown",
                },
                "responsible_subject_first_name": {
                    "alias_name": "Имя заменяющего",
                    "type": "read",
                    "data_taken": "dropdown",
                },
                "responsible_subject_father_name":  {
                    "alias_name": "Отчество заменяющего",
                    "type": "read",
                    "data_taken": "dropdown",
                }
            },
            'id': template2_id
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
            'can_cancel': True
        }, {
            'id': role2_id,
            'name': "Эксперт",
            'can_cancel': False
        }, {
            'id': role3_id,
            'name': "Утверждающий",
            'can_cancel': True
        }, {
            'id': role4_id,
            'name': "Уведомляемый",
            'can_cancel': False
        }, {
            'id': role5_id,
            'name': "Инициатор",
            'can_cancel': True
        }]
    )

    step1_1 = get_uuid()
    step1_2 = get_uuid()
    step1_3 = get_uuid()
    step2_1 = get_uuid()
    step2_2 = get_uuid()
    step2_3 = get_uuid()

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
        }]
    )


def get_uuid():
    return str(uuid.uuid4())


def create_user(id, name, surname, email, group_id, call_sign, number,  position_id, rank_id, actual_position_id):
    return {
        'id': id,
        'email': email,
        'password': '$2b$12$vhg69KJxWiGgetoLxGRvie3VxElPt45i4ELJiE/V2qOj30X3c3.7m',
        'first_name': name,
        'last_name': surname,
        'father_name': 'Отчество',
        'staff_division_id': group_id,
        'staff_unit_id': position_id,
        'call_sign': call_sign,
        'id_number': number,
        'phone_number': '+77771234789',
        'address': 'Mangilik Yel, 1',
        'rank_id': rank_id,
        'actual_staff_unit_id': actual_position_id,
        'status': "На работе"
    }


def downgrade() -> None:
    pass
