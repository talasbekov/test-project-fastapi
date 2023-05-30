from alembic import op
import sqlalchemy as sa

revision = 'archive_privelege_emergencies'
down_revision = 'b6c2329ba373'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('archive_privelege_emergencies',
        sa.Column('form', sa.Enum('form1', 'form2', 'form3', name='archiveformenum'), nullable=True),
        sa.Column('date_from', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('date_to', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('origin_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['origin_id'], ['privelege_emergencies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )