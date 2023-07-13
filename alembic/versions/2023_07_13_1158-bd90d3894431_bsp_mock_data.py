"""bsp mock data

Revision ID: bd90d3894431
Revises: 821642c0ded0
Create Date: 2023-07-13 07:26:35.539976

"""
import uuid
from datetime import datetime, date, time
from models import PlanStatus

from alembic import op
from sqlalchemy import text

from core import Base




# revision identifiers, used by Alembic.
revision = 'bd90d3894431'
down_revision = '87263d264688'
branch_labels = None
depends_on = None

def get_uuid():
    return str(uuid.uuid4())

def upgrade() -> None:
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
            "instructions": "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        },
        {
            "id": activity_id2,
            "name": "Рукопашные бои",
            "nameKZ": "Қоян-қолтық ұрыс",
            "parent_group_id": activity_id1,
            "instructions": "standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        },
        {
            "id": activity_id3,
            "name": "Плавание",
            "nameKZ": "Жүзім",
            "parent_group_id": activity_id1,
            "instructions": "and typesetting industry.has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        },
        {
            "id": activity_id4,
            "name": "Бег (100м)",
            "nameKZ": "Жүгіру (100м)",
            "parent_group_id": activity_id1,
            "instructions": "has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
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
            "status": PlanStatus.ACTIVE,
            "id": plan_id
        }, {
            "year": 2023,
            "creator_id": creator_id,
            "signed_at": None,
            "status": PlanStatus.DRAFT,
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
            SELECT '{schedule_id1}', id from selected_users
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
            WHERE parent_group_id = '{department_id}')
            )
            INSERT INTO schedule_year_users(schedule_year_id, user_id)
            SELECT '{schedule_id1}', id from selected_users
            """)
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
            SELECT '{schedule_id2}', id from selected_users
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
            WHERE parent_group_id = '{department_id}')
            )
            INSERT INTO schedule_year_users(schedule_year_id, user_id)
            SELECT '{schedule_id2}', id from selected_users
            """)
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
            SELECT '{schedule_id3}', id from selected_users
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
            WHERE parent_group_id = '{department_id}')
            )
            INSERT INTO schedule_year_users(schedule_year_id, user_id)
            SELECT '{schedule_id3}', id from selected_users
            """)
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
            SELECT '{schedule_id4}', id from selected_users
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
            WHERE parent_group_id = '{department_id}')
            )
            INSERT INTO schedule_year_users(schedule_year_id, user_id)
            SELECT '{schedule_id4}', id from selected_users
            """)
    )



    day_id1 = get_uuid()
    day_id2 = get_uuid()
    day_id3 = get_uuid()
    day_id4 = get_uuid()
    day_id5 = get_uuid()
    day_id6 = get_uuid()
    day_id7 = get_uuid()


    op.bulk_insert(
        Base.metadata.tables['days'],
        [
        {
            "name": "Понедельник",
            "nameKZ": "Дүйсенбі",
            "id": day_id1
        },
        {
            "name": "Вторник",
            "nameKZ": "Сейсенбі",
            "id": day_id2
        },
        {
            "name": "Среда",
            "nameKZ": "Сәрсенбі",
            "id": day_id3
        },
        {
            "name": "Четверг",
            "nameKZ": "Бейсенбі",
            "id": day_id4
        },
        {
            "name": "Пятница",
            "nameKZ": "Жұма",
            "id": day_id5
        },
        {
            "name": "Суббота",
            "nameKZ": "Сенбі",
            "id": day_id6
        },
        {
            "name": "Воскресенье",
            "nameKZ": "Жексенбі",
            "id": day_id7
        },
        ]
    )


    place_id1 = get_uuid()
    place_id2 = get_uuid()
    place_id3 = get_uuid()
    place_id4 = get_uuid()


    op.bulk_insert(
        Base.metadata.tables['places'],
        [
        {
            "name": "Большой спортзал",
            "nameKZ": "Үлкен спортзал",
            "id": place_id1
        },
        {
            "name": "Малый спортзал",
            "nameKZ": "Кіші спортзал",
            "id":  place_id2
        },
        {
            "name": "Стрельбище",
            "nameKZ": "Ату алаңы",
            "id": place_id3
        },
        {
            "name": "Бассейн",
            "nameKZ": "Бассейн",
            "id": place_id4
        },
        ]
    )


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

    schedule_month_id1 = get_uuid()
    schedule_month_id2 = get_uuid()
    schedule_month_id3 = get_uuid()
    schedule_month_id4 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['schedule_months'],
        [{
            "start_date": date(2023, 3, 1),
            "end_date": date(2023, 3, 30),
            "place_id": place_id1,
            "schedule_id": schedule_id1,
            "id": schedule_month_id1
        },
        {
            "start_date": date(2023, 4, 1),
            "end_date": date(2023, 4, 30),
            "place_id": place_id2,
            "schedule_id": schedule_id2,
            "id": schedule_month_id2
        },
        {
            "start_date": date(2023, 5, 1),
            "end_date": date(2023, 5, 30),
            "place_id": place_id3,
            "schedule_id": schedule_id3,
            "id": schedule_month_id3
        },
        {
            "start_date": date(2023, 6, 1),
            "end_date": date(2023, 6, 30),
            "place_id": place_id4,
            "schedule_id": schedule_id4,
            "id": schedule_month_id4
        }]
    )

    instructor_id1 = conn.execute(
        text("SELECT id FROM users WHERE first_name = 'Адилет'")
    ).fetchone()[0]

    instructor_id2 = conn.execute(
        text("SELECT id FROM users WHERE first_name = 'Елена'")
    ).fetchone()[0]

    instructor_id3 = conn.execute(
        text("SELECT id FROM users WHERE first_name = 'Бауыржан'")
    ).fetchone()[0]

    instructor_id4 = conn.execute(
        text("SELECT id FROM users WHERE first_name = 'Асет'")
    ).fetchone()[0]

    op.bulk_insert(
        Base.metadata.tables['schedule_month_instructors'],
        [
        {
            "schedule_month_id": schedule_month_id1,
            "user_id": instructor_id1
        },
        {
            "schedule_month_id": schedule_month_id2,
            "user_id": instructor_id2
        },
        {
            "schedule_month_id": schedule_month_id3,
            "user_id": instructor_id3
        },
        {
            "schedule_month_id": schedule_month_id4,
            "user_id": instructor_id4
        }
        ]
    )

    exam_schedule_id1 = get_uuid()
    exam_schedule_id2 = get_uuid()
    exam_schedule_id3 = get_uuid()
    exam_schedule_id4 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['exam_schedules'],
        [{
            "start_date": date(2023, 4, 1),
            "end_date": date(2023, 4, 3),
            "start_time": time(8, 0, 0),
            "end_time": time(10, 0, 0),
            "place_id": place_id1,
            "schedule_id": schedule_id1,
            "id": exam_schedule_id1
        },
        {
            "start_date": date(2023, 5, 1),
            "end_date": date(2023, 5, 3),
            "start_time": time(8, 0, 0),
            "end_time": time(10, 0, 0),
            "place_id": place_id2,
            "schedule_id": schedule_id2,
            "id": exam_schedule_id2
        },
        {
            "start_date": date(2023, 6, 1),
            "end_date": date(2023, 6, 3),
            "start_time": time(8, 0, 0),
            "end_time": time(10, 0, 0),
            "place_id": place_id3,
            "schedule_id": schedule_id3,
            "id": exam_schedule_id3
        },
        {
            "start_date": date(2023, 7, 1),
            "end_date": date(2023, 7, 3),
            "start_time": time(8, 0, 0),
            "end_time": time(10, 0, 0),
            "place_id": place_id4,
            "schedule_id": schedule_id4,
            "id": exam_schedule_id4
        }]
    )

    op.bulk_insert(
        Base.metadata.tables['exam_schedule_instructors'],
        [
        {
            "exam_schedule_id": exam_schedule_id1,
            "user_id": instructor_id1
        },
        {
            "exam_schedule_id": exam_schedule_id2,
            "user_id": instructor_id2
        },
        {
            "exam_schedule_id": exam_schedule_id3,
            "user_id": instructor_id3
        },
        {
            "exam_schedule_id": exam_schedule_id4,
            "user_id": instructor_id4
        }
        ]
    )

    schedule_day_id1 = get_uuid()
    schedule_day_id2 = get_uuid()
    schedule_day_id3 = get_uuid()
    schedule_day_id4 = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['schedule_days'],
        [{
            "day_id": day_id1,
            "month_id": schedule_month_id1,
            "start_time": time(8, 0, 0),
            "end_time": time(10, 0, 0),
            "id": schedule_day_id1
        },
        {
            "day_id": day_id2,
            "month_id": schedule_month_id2,
            "start_time": time(8, 0, 0),
            "end_time": time(10, 0, 0),
            "id": schedule_day_id2
        },
        {
            "day_id": day_id3,
            "month_id": schedule_month_id3,
            "start_time": time(8, 0, 0),
            "end_time": time(10, 0, 0),
            "id": schedule_day_id3
        },
        {
            "day_id": day_id4,
            "month_id": schedule_month_id4,
            "start_time": time(8, 0, 0),
            "end_time": time(10, 0, 0),
            "id": schedule_day_id4
        }
        ]
    )




def downgrade() -> None:
    pass
