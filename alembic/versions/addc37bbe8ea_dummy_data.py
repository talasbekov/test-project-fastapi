"""dummy data

Revision ID: addc37bbe8ea
Revises: 512b89e2ce36
Create Date: 2023-02-09 14:03:10.828717

"""
import uuid

from alembic import op
import sqlalchemy as sa

from core import configs, Base


# revision identifiers, used by Alembic.
revision = 'addc37bbe8ea'
down_revision = '512b89e2ce36'
branch_labels = None
depends_on = None


def upgrade() -> None:

    rank1_id = get_uuid()
    rank2_id = get_uuid()
    rank3_id = get_uuid()
    
    op.bulk_insert(
        Base.metadata.tables['ranks'],
        [{
            'id': rank1_id,
            'name': 'Майор'
        }, {
            'id': rank2_id,
            'name': 'Подполковник'
        }, {
            'id': rank3_id,
            'name': 'Полковник'
        }]
    )

    position1_id = get_uuid()
    position2_id = get_uuid()
    position3_id = get_uuid()
    position4_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['positions'],
        [{
            'id': position1_id,
            'name': 'Солдат',
            'max_rank_id': rank1_id
        },{
            'id': position2_id,
            'name': 'Начальник Отдела',
            'max_rank_id': rank1_id
        }, {
            'id': position3_id,
            'name': 'Начальник Управления',
            'max_rank_id': rank2_id
        }, {
            'id': position4_id,
            'name': 'Начальник Департамента',
            'max_rank_id': rank3_id
        }]
    )



    group1_id = get_uuid()
    group2_id = get_uuid()
    group3_id = get_uuid()


    op.bulk_insert(
        Base.metadata.tables['groups'],
        [{
            'parent_group_id': None,
            'id': group1_id,
            'name': "Департамент 1"
        }, {
            'parent_group_id': group1_id,
            'id': group2_id,
            'name': "Управление 1"
        }, {
            'parent_group_id': group2_id,
            'id': group3_id,
            'name': "Группа 1"
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
                "Адлет",
                "Наурыбаев", 
                'adilet@mail.ru', 
                group3_id, 
                "Альфа 1", 
                '1', 
                position1_id),
            create_user(
                user2_id,
                "Ахат",
                "Наурыбаев", 
                'ahat@mail.ru', 
                group3_id, 
                "Альфа 2", 
                '2',
                position1_id),
            create_user(
                user3_id,
                "Асет",
                "Наурыбаев", 
                'aset@mail.ru', 
                group3_id, 
                "Альфа 3", 
                '3', 
                position1_id),
            create_user(
                user4_id,
                "Жасулан",
                "Наурыбеков", 
                'zhasulan@mail.ru', 
                group3_id, 
                "Альфа 4", 
                '4', 
                position2_id),
            create_user(
                user5_id,
                "Ануар",
                "Наурыбеков", 
                'anuar@mail.ru', 
                group2_id, 
                "Альфа 5", 
                '5', 
                position1_id),
            create_user(
                user6_id,
                "Бексундет",
                "Наурыбеков", 
                'beksundet@mail.ru', 
                group2_id, 
                "Альфа 6", 
                '6', 
                position3_id),
            create_user(
                user7_id,
                "Ерден",
                "Наурыбеков", 
                'erden@mail.ru', 
                group2_id, 
                "Альфа 7", 
                '7', 
                position1_id),
            create_user(
                user8_id,
                "Еркин",
                "Наурыбеков", 
                'erkin@mail.ru', 
                group3_id, 
                "Альфа 8", 
                '8', 
                position1_id),
            create_user(
                user9_id,
                "Арман",
                "Наурыбеков", 
                'arman@mail.ru', 
                group3_id, 
                "Альфа 9", 
                '9', 
                position1_id),
            create_user(
                user10_id,
                "Бауыржан",
                "Наурыбеков", 
                'bauyrzhan@mail.ru', 
                group3_id, 
                "Альфа 10", 
                '10', 
                position4_id)
        ]
    )

    template1_id = get_uuid()
    template2_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['hr_document_templates'],
        [{
            'name': 'Приказ о назначении на должность',
            'path': '../static/templates/приказ_о_назначении на должность.docx',
            'subject_type': 1,
            'properties': {},
            'id': template1_id
        },{
            'name': 'Приказ на отпуск',
            'path': '../static/templates/приказ_на_отпуск.docx',
            'subject_type': 1,
            'properties': {},
            'id': template2_id
        }]
    )

    role_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['roles'],
        [{
            'id': role_id,
            'name': "Согласующий"
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
            'position_id': position2_id,
            'role_id': role_id,
            'id': step1_1
        }, {
            'hr_document_template_id': template1_id,
            'previous_step_id': step1_1,
            'position_id': position3_id,
            'role_id': role_id,
            'id': step1_2
        }, {
            'hr_document_template_id': template1_id,
            'previous_step_id': step1_2,
            'position_id': position4_id,
            'role_id': role_id,
            'id': step1_3
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': None,
            'position_id': position2_id,
            'role_id': role_id,
            'id': step2_1
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': step2_1,
            'position_id': position3_id,
            'role_id': role_id,
            'id': step2_2
        }, {
            'hr_document_template_id': template2_id,
            'previous_step_id': step2_2,
            'position_id': position4_id,
            'role_id': role_id,
            'id': step2_3
        }]
    )



def get_uuid():
    return str(uuid.uuid4())

def create_user(id, name, surname, email, group_id, call_sign, number,  position_id):
    return {
        'id': id,
        'email': email,
        'password': '$2b$12$vhg69KJxWiGgetoLxGRvie3VxElPt45i4ELJiE/V2qOj30X3c3.7m',
        'first_name': name,
        'last_name': surname,
        'father_name': 'Отчество',
        'group_id': group_id,
        'position_id': position_id,
        'call_sign': call_sign,
        'id_number': number,
        'phone_number': '+77771234789',
        'address': 'Mangilik Yel, 1'
    }



def downgrade() -> None:
    pass
