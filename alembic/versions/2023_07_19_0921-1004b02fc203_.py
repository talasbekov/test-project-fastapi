"""empty message

Revision ID: 1004b02fc203
Revises: 09b20dbda183
Create Date: 2023-07-19 09:21:03.074656

"""
import uuid
import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from core import Base


# revision identifiers, used by Alembic.
revision = '1004b02fc203'
down_revision = '09b20dbda183'
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

    quiz1_id = get_uuid()
    quiz2_id = get_uuid()
    quiz3_id = get_uuid()
    end_date = datetime.datetime.now() + datetime.timedelta(days=30)
    
    op.bulk_insert(
        Base.metadata.tables['surveys'],
        [{
            'id': quiz1_id,
            'description': 'Испытайте свои знания и стратегическое мышление в этом увлекательном квизе, где вам предстоит сражаться с вопросами разной сложности. Битва умов начинается!',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': 'Умные сражения',
            'nameKZ': None,
            'staff_position': 'Все',
            'type': 'QUIZ',
            'is_kz_translate_required': False
        }, {
            'id': quiz2_id,
            'description': 'Погрузитесь в мир знаний и соревнуйтесь с другими игроками в этом захватывающем квизе. Ответьте на вопросы различных тем и покажите, что вы настоящий чемпион знаний!',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': 'Знаниевая арен',
            'nameKZ': None,
            'staff_position': 'Все',
            'type': 'QUIZ',
            'is_kz_translate_required': False
        }, {
            'id': quiz3_id,
            'description': 'Пройдите наш увлекательный квиз и откройте для себя мир игровых возможностей. Ответьте на вопросы о вашем опыте и предпочтениях, чтобы найти самую интересную функцию и понять, что делает игры по-настоящему захватывающими!',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': 'Игровая Мастерская',
            'nameKZ': None,
            'staff_position': 'Все',
            'type': 'QUIZ',
            'is_kz_translate_required': False
        }]
    )
    
    question1_1_id = get_uuid()
    question1_2_id = get_uuid()
    question1_3_id = get_uuid()

    op.bulk_insert(
        Base.metadata.tables['questions'],
        [
            {
                'id': question1_1_id,
                'text': 'Какими словами вы бы описали свой общий опыт использования платформы "Умные сражения"?',
                'is_required': False,
                'survey_id': quiz1_id,
                'question_type': 'TEXT',
                'score': 1
            },
            {
                'id': question1_2_id,
                'text': 'Какой из следующих функций платформы "Умные сражения" вы считаете наиболее полезной?',
                'is_required': True,
                'survey_id': quiz1_id,
                'question_type': 'SINGLE_SELECTION',
                'score': 1
            },
            {
                'id': question1_3_id,
                'text': 'Какие из следующих факторов, на ваш взгляд, определяют удобство использования платформы "Умные сражения"? (Выберите все подходящие варианты)',
                'is_required': True,
                'survey_id': quiz1_id,
                'question_type': 'MULTIPLE_SELECTION',
                'score': 1
            }
        ]
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
        [
            {
                'id': option1_2_1_id,
                'question_id': question1_2_id,
                'text': 'Автоматический расчет результатов',
                'score': 0
            },
            {
                'id': option1_2_2_id,
                'question_id': question1_2_id,
                'score': 1,
                'text': 'Интерактивные игровые элементы'
            },
            {
                'id': option1_2_3_id,
                'question_id': question1_2_id,
                'score': 0,
                'text': 'Система достижений и наград'
            },
            {
                'id': option1_2_4_id,
                'question_id': question1_2_id,
                'score': 0,
                'text': 'Множество уровней сложности'
            },
            {
                'id': option1_3_1_id,
                'question_id': question1_3_id,
                'score': 0,
                'text': 'Простой и интуитивный интерфейс'
            },
            {
                'id': option1_3_2_id,
                'question_id': question1_3_id,
                'score': 0,
                'text': 'Быстрая загрузка игровых сцен'
            },
            {
                'id': option1_3_3_id,
                'score': 0,
                'question_id': question1_3_id,
                'text': 'Гибкая система настроек игры'
            },
            {
                'id': option1_3_4_id,
                'score': 1,
                'question_id': question1_3_id,
                'text': 'Возможность соревноваться с другими игроками'
            }
        ]
    )


def downgrade() -> None:
    pass
