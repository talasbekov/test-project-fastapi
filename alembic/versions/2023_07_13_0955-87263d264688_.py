"""empty message

Revision ID: 87263d264688
Revises: 984201b8ecf3
Create Date: 2023-07-13 09:55:44.407434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87263d264688'
down_revision = '821642c0ded0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE hr_document_templates
        SET actions = '{"args": [
                {
                    "position_change": {
                        "staff_unit": {
                            "tagname": "staff_unit",
                            "alias_name": "\u041D\u043E\u0432\u0430\u044F\u0020\u0434\u043E\u043B\u0436\u043D\u043E\u0441\u0442\u044C",
                            "alias_nameKZ": "\u0416\u0430\u04A3\u0430\u0020\u049B\u044B\u0437\u043C\u0435\u0442\u0020\u0430\u0442\u0430\u0443\u044B"
                        }
                    },
                    "renew_contract": {
                        "contract": {
                            "tagname": "contract",
                            "alias_name": "\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442",
                            "alias_nameKZ": "\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442"
                        }
                    }
                }
            ]}'
        WHERE name = 'Приказ о зачислении на службу сотрудника'
        """
    )


def downgrade() -> None:
    pass
