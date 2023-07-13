"""bsp mock data

Revision ID: bd90d3894431
Revises: 821642c0ded0
Create Date: 2023-07-13 07:26:35.539976

"""
import uuid
from datetime import datetime

from alembic import op
from sqlalchemy import text

from core import Base




# revision identifiers, used by Alembic.
revision = 'bd90d3894431'
down_revision = '821642c0ded0'
branch_labels = None
depends_on = None

def get_uuid():
    return str(uuid.uuid4())

def upgrade() -> None:
    base_s3_url = 'http://192.168.0.169:8083'

    conn = op.get_bind()

    creator_id = conn.execute(
        text("SELECT id FROM users WHERE first_name = 'Батырбек'")
    ).fetchone()[0]

    activity_id1 = get_uuid()
    activity_id2 = get_uuid()
    activity_id3 = get_uuid()
    activity_id4 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['activities'],
        [{
            "id": activity_id1,
            "name": "Специальная физическая подготовка",
            "nameKZ": "Арнайы дене дайындығы",
            "parent_group_id": None,
            "instructions": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        },
        {
            "id": activity_id2,
            "name": "Рукопашные бои",
            "nameKZ": "Қоян-қолтық ұрыс",
            "parent_group_id": activity_id1,
            "instructions": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        },
        {
            "id": activity_id3,
            "name": "Плавание",
            "nameKZ": "Жүзім",
            "parent_group_id": activity_id1,
            "instructions": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        },
        {
            "id": activity_id4,
            "name": "Бег (100м)",
            "nameKZ": "Жүгіру (100м)",
            "parent_group_id": activity_id1,
            "instructions": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        }
        ]
    )

    plan_id = get_uuid()
    plan_id1 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['bsp_plans'],
        [{
            "year": 2022,
            "creator_id": creator_id,
            "signed_at": datetime.now(),
            "id": plan_id
        }, {
            "year": 2023,
            "creator_id": creator_id,
            "signed_at": None,
            "id": plan_id1
        }]
    )

    schedule_id1 = get_uuid()
    schedule_id2 = get_uuid()
    schedule_id3 = get_uuid()
    schedule_id4 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['schedule_years'],
        [{
            "plan_id": plan_id,
            "activity_id": activity_id1,
            "is_exam_required": True,
            "retry_count": 2,
            "id": schedule_id1
        },
        {
            "plan_id": plan_id,
            "activity_id": activity_id2,
            "is_exam_required": True,
            "retry_count": 1,
            "id": schedule_id2
        },
        {
            "plan_id": plan_id1,
            "activity_id": activity_id3,
            "is_exam_required": True,
            "retry_count": 1,
            "id": schedule_id3
        },
        {
            "plan_id": plan_id1,
            "activity_id": activity_id4,
            "is_exam_required": True,
            "retry_count": 1,
            "id": schedule_id4
        }]
    )

    month_id1 = get_uuid()
    month_id2 = get_uuid()
    month_id3 = get_uuid()
    month_id4 = get_uuid()
    month_id5 = get_uuid()
    month_id6 = get_uuid()
    month_id7 = get_uuid()
    month_id8 = get_uuid()
    month_id9 = get_uuid()
    month_id10 = get_uuid()
    month_id11 = get_uuid()
    month_id12 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['months'],
        [
        {
            "name": "Январь",
            "nameKZ": "Қаңтар",
            "id": month_id1
        },
        {
            "name": "Февраль",
            "nameKZ": "Ақпан",
            "id": month_id2
        },
        {
            "name": "Март",
            "nameKZ": "Наурыз",
            "id": month_id3
        },
        {
            "name": "Апрель",
            "nameKZ": "Сәуiр",
            "id": month_id4
        },
        {
            "name": "Май",
            "nameKZ": "Мамыр",
            "id": month_id5
        },
        {
            "name": "Июнь",
            "nameKZ": "Маусым",
            "id": month_id6
        },
        {
            "name": "Июль",
            "nameKZ": "Шiлде",
            "id": month_id7
        },
        {
            "name": "Август",
            "nameKZ": "Тамыз",
            "id": month_id8
        },
        {
            "name": "Сентябрь",
            "nameKZ": "Қыркүйек",
            "id": month_id9
        },
        {
            "name": "Октябрь",
            "nameKZ": "Қазан",
            "id": month_id10
        },
        {
            "name": "Ноябрь",
            "nameKZ": "Қараша",
            "id": month_id11
        },
        {
            "name": "Декабрь",
            "nameKZ": "Желтоқсан",
            "id": month_id12
        },
        ]
    )


    op.bulk_insert(
        Base.metadata.tables['schedule_year_months'],
        [
        {
            "schedule_year_id": schedule_id1,
            "month_id": month_id4
        },
        {
            "schedule_year_id": schedule_id1,
            "month_id": month_id3
        },
        {
            "schedule_year_id": schedule_id2,
            "month_id": month_id6
        },
        {
            "schedule_year_id": schedule_id3,
            "month_id": month_id7
        },
        {
            "schedule_year_id": schedule_id4,
            "month_id": month_id8
        }
        ]
    )

    op.bulk_insert(
        Base.metadata.tables['schedule_exam_months'],
        [
        {
            "schedule_year_id": schedule_id1,
            "month_id": month_id4
        },
        {
            "schedule_year_id": schedule_id1,
            "month_id": month_id3
        },
        {
            "schedule_year_id": schedule_id2,
            "month_id": month_id6
        },
        {
            "schedule_year_id": schedule_id3,
            "month_id": month_id7
        },
        {
            "schedule_year_id": schedule_id4,
            "month_id": month_id8
        }
        ]
    )

    department_id = conn.execute(
        text("SELECT id FROM staff_divisions "
             "WHERE name = 'Пятый департамент'")
    ).fetchone()[0]

    division_id = conn.execute(
        text(f"SELECT id FROM staff_divisions"
             f" WHERE name = '1 управление' "
             f"and parent_group_id = '{department_id}'")
    ).fetchone()[0]

    op.bulk_insert(
        Base.metadata.tables['schedule_year_staff_divisions'],
        [
        {
            "schedule_year_id": schedule_id1,
            "staff_division_id": department_id
        },
        {
            "schedule_year_id": schedule_id1,
            "staff_division_id": department_id
        },
        {
            "schedule_year_id": schedule_id2,
            "staff_division_id": department_id
        },
        {
            "schedule_year_id": schedule_id3,
            "staff_division_id": department_id
        },
        {
            "schedule_year_id": schedule_id4,
            "staff_division_id": department_id
        }
        ]
    )

    conn.execute(
        text(f"""
            WITH selected_users AS
            (
            SELECT u.id FROM users u
            JOIN staff_units su ON u.staff_unit_id = su.id
            WHERE su.staff_division_id = '{department_id}'
            )
            INSERT INTO schedule_year_users(schedule_year_id, user_id)
            SELECT '{schedule_id1}', user_id from selected_users
            );
            """)
    )

    conn.execute(
        text(f"""
            WITH selected_users AS
            (
            SELECT u.id FROM users u
            JOIN staff_units su ON u.staff_unit_id = su.id
            WHERE su.staff_division_id in (
            SELECT id FROM staff_divisions
            WHERE parent_group_id = {department_id})
            )
            INSERT INTO schedule_year_users(schedule_year_id, user_id)
            SELECT '{schedule_id1}', user_id from selected_users
            );
            """)
    )



def downgrade() -> None:
    pass
