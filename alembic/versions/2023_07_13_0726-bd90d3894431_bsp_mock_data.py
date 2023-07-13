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
    plan_id = get_uuid()
    plan_id1 = get_uuid()
    conn = op.get_bind()

    creator_id = conn.execute(
        text("SELECT id FROM users WHERE first_name = 'Батырбек'")
    ).fetchone()[0]

    op.bulk_insert(
        Base.metadata.tables['bsp_plans'],
        [{
            "year": 2023,
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

    # op.bulk_insert(
    #     Base.metadata.tables['schedule_years'],
    #     [{
    #         "year": 2023,
    #         "creator_id": creator_id,
    #         "signed_at": datetime.now(),
    #         "id": plan_id
    #     }, {
    #         "year": 2023,
    #         "creator_id": creator_id,
    #         "signed_at": None,
    #         "id": plan_id
    #     }]
    # )



def downgrade() -> None:
    pass
