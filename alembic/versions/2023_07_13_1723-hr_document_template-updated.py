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
                                "alias_nameKZ":"Тегі",
                                "data_taken":"auto",
                                "type":"write",
                                "field_name":"surname",
                                "to_tags":{
                                    "titleKZ":"Тегі",
                                    "isHidden":"false"
                                }
                            },
                            "name":{
                                "alias_nameKZ":"Аты",
                                "data_taken":"auto",
                                "type":"write",
                                "field_name":"name",
                                "to_tags":{
                                    "titleKZ":"Аты",
                                    "isHidden":"false"
                                }
                            },
                            "father":{
                                "alias_nameKZ":"Әкесінің аты",
                                "data_taken":"auto",
                                "type":"write",
                                "field_name":"father_name",
                                "to_tags":{
                                    "foundInText":"Отчество субъекта",
                                    "titleKZ":"Әкесінің аты",
                                    "isHidden":"false",
                                    "cases":"0"
                                }
                            },
                            "contract":{
                                "to_tags":{
                                    "tagname":"contract",
                                    "titleKZ":"Контракт",
                                    "idToChange":"1687429527959",
                                    "id":"1687429527959",
                                    "foundInText":"{{contract - term}}",
                                    "isHidden":"false",
                                    "cases":"0",
                                    "action_type":"[renew_contract]"
                                },
                                "alias_name":"Контракт",
                                "alias_nameKZ":"Контракт",
                                "type":"write",
                                "data_taken":"dropdown",
                                "field_name":"contracts",
                                "isHidden":"false"
                            },
                            "new_position":{
                                "alias_nameKZ":"Жаңа позиция",
                                "data_taken":"dropdown",
                                "type":"write",
                                "field_name":"staff_unit",
                                "to_tags":{
                                    "titleKZ":"Жаңа позиция",
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
