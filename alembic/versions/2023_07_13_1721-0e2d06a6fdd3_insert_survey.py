"""insert survey

Revision ID: 0e2d06a6fdd3
Revises: bbbd58ffa3ee
Create Date: 2023-07-13 17:21:18.444976

"""
import uuid, datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

from core import Base


# revision identifiers, used by Alembic.
revision = '0e2d06a6fdd3'
down_revision = 'bbbd58ffa3ee'
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


    survey2_id = get_uuid()
    survey3_id = get_uuid()
    survey4_id = get_uuid()
    survey5_id = get_uuid()
    survey6_id = get_uuid()
    survey7_id = get_uuid()
    survey8_id = get_uuid()
    survey9_id = get_uuid()
    survey10_id = get_uuid()
    end_date = datetime.datetime.now() + datetime.timedelta(days=30)

    op.bulk_insert(
        Base.metadata.tables['surveys'],
        [{
            'id': survey2_id,
            'description': 'Приветствуем вас в опросе "SmartLife" - платформе, которая поможет нам понять ваши предпочтения и мнения относительно технологий будущего. Мы стремимся создать лучшую жизнь для всех, основанную на инновациях и современных решениях.',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': 'Технологии будущего: Ваше мнение и предпочтения',
            'nameKZ': None,
            'staff_position': 'Все'
        }, {
            'id': survey3_id,
            'description': 'Мы исследуем ваше отношение к криптовалютам и их роль в будущем финансовой системы. Поделитесь своими знаниями, опытом и мнением о возможностях и рисках, связанных с цифровыми валютами.',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': True,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': 'Криптовалюты и будущее финансов',
            'nameKZ': None,
            'staff_position': 'Все'
        }, {
            'id': survey4_id,
            'description': 'Оцените ваше взаимодействие с мобильными приложениями и их влияние на вашу повседневную жизнь. Помогите нам понять, какие функции и удобства наиболее важны для вас, чтобы улучшить пользовательский опыт.',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': True,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': 'Мобильные приложения и ваше повседневное существование',
            'nameKZ': None,
            'staff_position': 'Все'
        }, {
            'id': survey5_id,
            'description': 'Оцените ваше отношение к роботам и автоматизации на рабочем месте. Помогите нам понять, как вы смотрите на перспективы использования роботов и какие вопросы волнуют вас в связи с этой технологией.',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': '"Роботы и автоматизация в рабочей среде"',
            'nameKZ': None,
            'staff_position': 'Все'
        }, {
            'id': survey6_id,
            'description': 'Мы интересуемся вашим мнением о роли экологических технологий в борьбе за сохранение нашей планеты. Поделитесь своими предпочтениями и вкладом в области устойчивого развития и экологической ответственности.',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': '"Экологические технологии и сохранение планеты"',
            'nameKZ': None,
            'staff_position': 'Все'
        }, {
            'id': survey7_id,
            'description': 'Оцените ваше представление об использовании искусственного интеллекта в образовательной сфере. Поделитесь своим мнением о потенциале ИИ для улучшения образования и вызывающих вопросов аспектах этой технологии.',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Активный',
            'name': 'Искусственный интеллект и будущее образования"',
            'nameKZ': None,
            'staff_position': 'Все'
        }, {
            'id': survey8_id,
            'description': 'Мы исследуем ваше отношение к технологиям виртуальной и дополненной реальности. Поделитесь своими знаниями, опытом и мнением о возможностях и рисках, связанных с этими технологиями.',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Архивный',
            'name': 'Виртуальная и дополненная реальность',
            'nameKZ': None,
            'staff_position': 'Все'
        }, {
            'id': survey9_id,
            'description': 'Оцените ваше взаимодействие с мобильными приложениями и их влияние на вашу повседневную жизнь. Помогите нам понять, какие функции и удобства наиболее важны для вас, чтобы улучшить пользовательский опыт.',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Архивный',
            'name': 'Мобильные приложения и ваше повседневное существование',
            'nameKZ': None,
            'staff_position': 'Все'
        }, {
            'id': survey10_id,
            'description': 'Оцените ваше отношение к роботам и автоматизации на рабочем месте. Помогите нам понять, как вы смотрите на перспективы использования роботов и какие вопросы волнуют вас в связи с этой технологией.',
            'start_date': datetime.datetime.now(),
            'end_date': end_date,
            'is_anonymous': False,
            'jurisdiction_type': 'Определенный участник',
            'certain_member_id': batyrbek_user_id,
            'staff_division_id': None,
            'status': 'Архивный',
            'name': '"Роботы и автоматизация в рабочей среде"',
            'nameKZ': None,
            'staff_position': 'Все'
        }]
    )


def downgrade() -> None:
    pass
