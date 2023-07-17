"""empty message

Revision ID: cf2565196316
Revises: 984201b8ecf3
Create Date: 2023-07-17 09:56:31.071405

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

from core import Base


# revision identifiers, used by Alembic.
revision = 'cf2565196316'
down_revision = '59ab1232c593'
branch_labels = None
depends_on = None

def get_uuid():
    return str(uuid.uuid4())

def upgrade() -> None:
    conn = op.get_bind()
    fifth_department_id = str(conn.execute(
        text("SELECT id FROM staff_divisions WHERE name = 'Пятый департамент'")
    ).fetchone()[0])

    head_of_department_position_id = str(conn.execute(
        text("SELECT id from positions where name ='Начальник департамента'")
    ).fetchone()[0])

    conn.execute(
        sa.text("UPDATE staff_units "
                "SET curator_of_id ='" + fifth_department_id + "'" +
                "WHERE position_id ='" + head_of_department_position_id + "'" +
                "AND staff_division_id ='" + fifth_department_id + "'"
        )
    )

    korkem_user_id = str(conn.execute(
        text("SELECT id FROM users WHERE email = 'koktem@mail.ru'")
    ).fetchone()[0])

    elena_user_id = str(conn.execute(
        text("SELECT id FROM users WHERE email = 'elena@mail.ru'")
    ).fetchone()[0])

    kuat_user_id = str(conn.execute(
        text("SELECT id FROM users WHERE email = 'kuat@mail.ru'")
    ).fetchone()[0])

    admin_user_id = str(conn.execute(
        text("SELECT id FROM users WHERE email = 'admin@mail.com'")
    ).fetchone()[0])

    status_type_id = get_uuid()
    status_type2_id = get_uuid()
    status_type3_id = get_uuid()
    status_type4_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['status_types'],
        [
            {
                'id': status_type_id,
                'name': 'В отпуске',
                'nameKZ': 'В отпуске'
            }, {
                'id': status_type2_id,
                'name': 'В отпуске по болезни',
                'nameKZ': 'В отпуске по болезни'
            }, {
                'id': status_type3_id,
                'name': 'В командировке',
                'nameKZ': 'В командировке'
            }, {
                'id': status_type4_id,
                'name': 'Ежегодный отпуск',
                'nameKZ': 'Ежегодный отпуск'
            }
        ])

    status_id = get_uuid()
    status2_id = get_uuid()
    status3_id = get_uuid()
    status4_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['statuses'],
        [
            {
                'id': status_id,
                'type_id': status_type_id,
                'user_id': korkem_user_id
            }, {
                'id': status2_id,
                'type_id': status_type2_id,
                'user_id': elena_user_id
            }, {
                'id': status3_id,
                'type_id': status_type3_id,
                'user_id': kuat_user_id
            }, {
                'id': status4_id,
                'type_id': status_type4_id,
                'user_id': admin_user_id
            }
        ])



def downgrade() -> None:
    pass
