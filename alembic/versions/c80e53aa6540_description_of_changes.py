"""Description of changes

Revision ID: c80e53aa6540
Revises: 49c58ae0724b
Create Date: 2023-05-12 08:37:37.626910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c80e53aa6540'
down_revision = '49c58ae0724b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'nakladnas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('number', sa.String(13)),
        sa.Column('address_1', sa.Integer, sa.ForeignKey('units.id')),
        sa.Column('address_2', sa.Integer, sa.ForeignKey('units.id')),
        sa.Column('id_perelik', sa.Integer, sa.ForeignKey('pereliks.id')),
        sa.Column('kilkist', sa.String(13)),
        sa.Column('id_odvumir', sa.Integer, sa.ForeignKey('odvumirs.id')),
        sa.Column('notes', sa.String(13)),
        sa.Column('date_created', sa.DateTime(), default=sa.text('current_timestamp')),
        sa.Column('date_updated', sa.DateTime(), default=sa.text('current_timestamp')),
    )

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    None