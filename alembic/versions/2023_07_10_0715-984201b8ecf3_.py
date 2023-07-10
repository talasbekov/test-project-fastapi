"""empty message

Revision ID: 984201b8ecf3
Revises: 5895ed1b9641
Create Date: 2023-07-10 07:15:41.392298

"""
import uuid, datetime

from alembic import op
import sqlalchemy as sa

from core import Base


# revision identifiers, used by Alembic.
revision = '984201b8ecf3'
down_revision = '5895ed1b9641'
branch_labels = None
depends_on = None


def get_uuid():
    return str(uuid.uuid4())

def upgrade() -> None:
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
            'jurisdiction_type': 'Штатное подразделение',
            'certain_member_id': None,
            'staff_division_id': None,
            'status': 'Активный',
            'name': 'Опрос "Оценка пользовательского опыта: ваше впечатление о веб-сайте Cleverest Technologies',
            'nameKZ': None
        }]
    )
    
    question1_1_id = get_uuid()
    question1_2_id = get_uuid()
    question1_3_id = get_uuid()
    question1_4_id = get_uuid()
    question1_5_id = get_uuid()
    
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
        },
        {
            'id': question1_4_id,
            'text': 'Насколько удовлетворены вы общей производительностью веб-сайта',
            'is_required': True,
            'survey_id': survey1_id,
            'question_type': 'SCALE',
            'discriminator': 'question_survey'
        },
        {
            'id': question1_5_id,
            'text': 'Пожалуйста, оцените следующие аспекты веб-сайта Cleverest Technologies от 1 до 5, где 1 - очень низкое качество и 5 - очень высокое качество:',
            'is_required': True,
            'survey_id': survey1_id,
            'question_type': 'GRID',
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
    
    option1_4_1_id = get_uuid()
    
    option1_5_1_id = get_uuid()
    option1_5_2_id = get_uuid()
    option1_5_3_id = get_uuid()
    option1_5_4_id = get_uuid()
    option1_5_5_id = get_uuid()
    option1_5_6_id = get_uuid()
    option1_5_7_id = get_uuid()
    option1_5_8_id = get_uuid()
    option1_5_9_id = get_uuid()
    option1_5_10_id = get_uuid()
    
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
        }, {
            'id': option1_4_1_id,
            'question_id': question1_4_id,
            'discriminator': 'option_scale',
            'min_value': 1,
            'max_value': 5,
            'text': None,
            'row_position': None,
            'column_position': None
        }, {
            'id': option1_5_1_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid',
            'text': 'Дизайн интерфейса',
            'row_position': 1,
            'column_position': 1,
            'min_value': None,
            'max_value': None
        },
        {
            'id': option1_5_2_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid',
            'text': 'Скорость загрузки страниц',
            'row_position': 2,
            'column_position': 1,
            'min_value': None,
            'max_value': None
        },
        {
            'id': option1_5_3_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid',
            'text': 'Навигация по сайту',
            'row_position': 3,
            'column_position': 1,
            'min_value': None,
            'max_value': None
        },
        {
            'id': option1_5_4_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid',
            'text': 'Качество предоставляемой информации',
            'row_position': 4,
            'column_position': 1,
            'min_value': None,
            'max_value': None
        },
        {
            'id': option1_5_5_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid','text': 'Удобство использования функциональности',
            'row_position': 5,
            'column_position': 1,
            'min_value': None,
            'max_value': None
        },
        {
            'id': option1_5_6_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid',
            'text': '1',
            'row_position': 1,
            'column_position': 1,
            'min_value': None,
            'max_value': None
        },
        {
            'id': option1_5_7_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid',
            'text': '2',
            'row_position': 1,
            'column_position': 2,
            'min_value': None,
            'max_value': None
        },
        {
            'id': option1_5_8_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid',
            'text': '3',
            'row_position': 1,
            'column_position': 3,
            'min_value': None,
            'max_value': None
        },
        {
            'id': option1_5_9_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid',
            'text': '4',
            'row_position': 1,
            'column_position': 4,
            'min_value': None,
            'max_value': None
        },
        {
            'id': option1_5_10_id,
            'question_id': question1_5_id,
            'discriminator': 'option_grid',
            'text': '5',
            'row_position': 1,
            'column_position': 5,
            'min_value': None,
            'max_value': None,
        }]
    )


def downgrade() -> None:
    pass
