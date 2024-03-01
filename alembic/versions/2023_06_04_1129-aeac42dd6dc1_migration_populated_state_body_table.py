"""migration/populated_state_body_table

Revision ID: aeac42dd6dc1
Revises: 376eb853da7a
Create Date: 2023-06-04 11:29:13.316546

"""
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from core import Base
from models import *


def get_uuid():
    return str(uuid4())

# revision identifiers, used by Alembic.
revision = 'aeac42dd6dc1'
down_revision = '376eb853da7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        Base.metadata.tables['state_bodies'],
        [
            {
                'id': get_uuid(),
                'name': 'Государственный орган',
                'nameKZ': 'Мемлекеттік орган',
            }, {
                'id': get_uuid(),
                'name': 'Запас',
                'nameKZ': 'Запас',
            }, {
                'id': get_uuid(),
                'name': 'Учебное заведение',
                'nameKZ': 'Оқу орны',
            }, {
                'id': get_uuid(),
                'name': 'Министерство по чрезвычайным ситуациям',
                'nameKZ': 'Ауыл шаруашылық ситуациялар министрлігі',
            }, {
                'id': get_uuid(),
                'name': 'Министерство внутренних дел РК',
                'nameKZ': 'Ішкі істер министрлігі',
            }, {
                'id': get_uuid(),
                'name': 'КНБ РК',
                'nameKZ': 'ҚР ҰҚК',
            }, {
                'id': get_uuid(),
                'name': 'Министерство обороны РК',
                'nameKZ': 'Қорғаныс министрлігі',
            }, {
                'id': get_uuid(),
                'name': 'Вооруженные силы РК',
                'nameKZ': 'ҚР Қарулы күштері',
            }, {
                'id': get_uuid(),
                'name': 'Республиканская гвардия',
                'nameKZ': 'Республикалық ұлан',
            }, {
                'id': get_uuid(),
                'name': "Служба охраны президента РК",
                'nameKZ': "ҚР Президентінің күзет қызметі",
            }, {
                'id': get_uuid(),
                'name': 'Пограничная служба КНБ РК',
                'nameKZ': 'ҚР ҰҚК Шекара қызметі',
            }, {
                'id': get_uuid(),
                'name': "Служба внешней разведки РК",
                'nameKZ': "ҚР Сыртқы барлау қызметі",
            }, {
                'id': get_uuid(),
                'name': 'СОО СГО РК',
                'nameKZ': 'ҚР МКҚ ОҚҚ',
            }, {
                'id': get_uuid(),
                'name': "Гражданская организация",
                'nameKZ': "Азаматтық ұйым",
            }, {
                'id': get_uuid(),
                'name': 'Национальная гвардия РК',
                'nameKZ': 'ҚР Ұлттық ұлан',
            }
        ]
    )


def downgrade() -> None:
    pass
