"""empty message
Revision ID: 87263d264688
Revises: 984201b8ecf3
Create Date: 2023-07-13 09:55:44.407434
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87263d264688'
down_revision = '0e2d06a6fdd3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE hr_document_templates
        SET actions = ' {
                            "args":[
                                {
                                    "apply_candidate":{
                                        "staff_unit":{
                                        "tagname":"new_position",
                                        "alias_name":"Новая должность",
                                        "alias_nameKZ":"Жаңа қызмет атауы"
                                        },
                                        "contract":{
                                        "tagname":"contract",
                                        "alias_name":"Контракт",
                                        "alias_nameKZ":"Контракт"
                                        }
                                    }
                                }
                            ]
                        }'
        WHERE name = 'Приказ о зачислении на службу сотрудника'
        """
    )

    op.execute(
        """
        UPDATE hr_document_templates
        SET properties = '{
                            "surname":{
                                "alias_nameKZ":"\u0422\u0435\u0433\u0456",
                                "data_taken":"auto",
                                "type":"write",
                                "field_name":"surname",
                                "to_tags":{
                                    "titleKZ":"\u0422\u0435\u0433\u0456",
                                    "isHidden":"false"
                                }
                            },
                            "name":{
                                "alias_nameKZ":"\u0410\u0442\u044b",
                                "data_taken":"auto",
                                "type":"write",
                                "field_name":"name",
                                "to_tags":{
                                    "titleKZ":"\u0410\u0442\u044b",
                                    "isHidden":false
                                }
                            },
                            "father":{
                                "alias_nameKZ":"\u04d8\u043a\u0435\u0441\u0456\u043d\u0456\u04a3 \u0430\u0442\u044b",
                                "data_taken":"auto",
                                "type":"write",
                                "field_name":"father_name",
                                "to_tags":{
                                    "foundInText":"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0443\u0431\u044a\u0435\u043a\u0442\u0430",
                                    "titleKZ":"\u04d8\u043a\u0435\u0441\u0456\u043d\u0456\u04a3 \u0430\u0442\u044b",
                                    "isHidden":false,
                                    "cases":0
                                }
                            },
                            "contract":{
                                "to_tags":{
                                    "tagname":"contract",
                                    "titleKZ":"\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442",
                                    "idToChange":"1687429527959",
                                    "id":"1687429527959",
                                    "foundInText":"{{contract - term}}",
                                    "isHidden":false,
                                    "cases":0,
                                    "action_type":"[renew_contract]"
                                },
                                "alias_name":"\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442",
                                "alias_nameKZ":"\u041a\u043e\u043d\u0442\u0440\u0430\u043a\u0442",
                                "type":"write",
                                "data_taken":"dropdown",
                                "field_name":"contracts",
                                "isHidden":false
                            },
                            "new_position":{
                                "alias_nameKZ":"\u0416\u0430\u04a3\u0430 \u043f\u043e\u0437\u0438\u0446\u0438\u044f",
                                "data_taken":"dropdown",
                                "type":"write",
                                "field_name":"staff_unit",
                                "to_tags":{
                                    "titleKZ":"\u0416\u0430\u04a3\u0430 \u043f\u043e\u0437\u0438\u0446\u0438\u044f",
                                    "directory":"staff_unit",
                                    "isHidden":"false"
                                }
                            }
                        }'
        WHERE name = 'Приказ о зачислении на службу сотрудника'
        """
    )



def downgrade() -> None:
    pass
