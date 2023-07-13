"""empty message

Revision ID: 59ab1232c593
Revises: 984201b8ecf3
Create Date: 2023-07-13 09:37:22.009022

"""
import uuid, datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

from core import Base


# revision identifiers, used by Alembic.
revision = '984201b8ecf3'
down_revision = 'bd90d3894431'
branch_labels = None
depends_on = None


def get_uuid():
    return str(uuid.uuid4())

def upgrade() -> None:

    conn = op.get_bind()
    # get user_id of batyrbek
    batyrbek_user_id = conn.execute(
        text(
            "SELECT id FROM users WHERE email = 'batyrbek@mail.ru'")
    ).fetchone()[0]


    survey1_id = get_uuid()
    end_date = datetime.datetime.now() + datetime.timedelta(days=30)

    op.bulk_insert(
        Base.metadata.tables['surveys'],
        [{
            'id': survey1_id,
            'description': 'Уважаемые сотрудники! Мы хотели бы получить вашу оценку нашего веб-сайта от Cleverest Technologies. Пожалуйста, поделитесь своим мнением о дизайне, удобстве использования, функциональности и общем опыте работы с нашим сайтом. Ваша обратная связь поможет нам улучшить нашу онлайн-платформу для вашего удобства и удовлетворения. Спасибо за участие!',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': 'Опрос "Оценка пользовательского опыта: ваше впечатление о веб-сайте Cleverest Technologies',
            'nameKZ': None,
            'staff_position': 'Все'
        }]
    )

    question1_1_id = get_uuid()
    question1_2_id = get_uuid()
    question1_3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['questions'],
        [{
            'id': question1_1_id,
            'text': 'Какими словами вы бы описали свой общий опыт использования веб-сайта от Cleverest Technologies?',
            'is_required': False,
            'survey_id': survey1_id,
            'question_type': 'TEXT',
            'discriminator': 'question_survey'
        },
        {
            'id': question1_2_id,
            'text': 'Какую из следующих функций веб-сайта вы считаете наиболее полезной?',
            'is_required': True,
            'survey_id': survey1_id,
            'question_type': 'SINGLE_SELECTION',
            'discriminator': 'question_survey'
        },
        {
            'id': question1_3_id,
            'text': 'Какие из следующих факторов, на ваш взгляд, определяют удобство использования веб-сайта Cleverest Technologies? (Выберите все подходящие варианты)',
            'is_required': True,
            'survey_id': survey1_id,
            'question_type': 'MULTIPLE_SELECTION',
            'discriminator': 'question_survey'
        }]
    )

    option1_2_1_id = get_uuid()
    option1_2_2_id = get_uuid()
    option1_2_3_id = get_uuid()
    option1_2_4_id = get_uuid()

    option1_3_1_id = get_uuid()
    option1_3_2_id = get_uuid()
    option1_3_3_id = get_uuid()
    option1_3_4_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['options'],
        [{
            'id': option1_2_1_id,
            'question_id': question1_2_id,
            'discriminator': 'option_text',
            'text': 'Личный дело сотрудника',
            'min_value': None,
            'max_value': None,
            'row_position': None,
            'column_position': None
        }, {
            'id': option1_2_2_id,
            'question_id': question1_2_id,
            'discriminator': 'option_text',
            'text': 'Автоматизации документооборота',
            'min_value': None,
            'max_value': None,
            'row_position': None,
            'column_position': None
        }, {
            'id': option1_2_3_id,
            'question_id': question1_2_id,
            'discriminator': 'option_text',
            'text': 'Штатное расписание',
            'min_value': None,
            'max_value': None,
            'row_position': None,
            'column_position': None
        }, {
            'id': option1_2_4_id,
            'question_id': question1_2_id,
            'discriminator': 'option_text',
            'text': 'Опросы и тесты',
            'min_value': None,
            'max_value': None,
            'row_position': None,
            'column_position': None
        }, {
            'id': option1_3_1_id,
            'question_id': question1_3_id,
            'discriminator': 'option_text',
            'text': 'Интуитивный интерфейс',
            'min_value': None,
            'max_value': None,
            'row_position': None,
            'column_position': None
        }, {
            'id': option1_3_2_id,
            'question_id': question1_3_id,
            'discriminator': 'option_text',
            'text': 'Быстрая загрузка страниц',
            'min_value': None,
            'max_value': None,
            'row_position': None,
            'column_position': None
        }, {
            'id': option1_3_3_id,
            'question_id': question1_3_id,
            'discriminator': 'option_text',
            'text': 'Четкая навигация',
            'min_value': None,
            'max_value': None,
            'row_position': None,
            'column_position': None
        }, {
            'id': option1_3_4_id,
            'question_id': question1_3_id,
            'discriminator': 'option_text',
            'text': 'Автоматизация рутинных задач',
            'min_value': None,
            'max_value': None,
            'row_position': None,
            'column_position': None
        }]
    )


def downgrade() -> None:
    pass
