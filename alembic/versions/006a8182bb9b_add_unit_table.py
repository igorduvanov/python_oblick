"""Add unit table

Revision ID: 006a8182bb9b
Revises: 7a62a9d8171e
Create Date: 2023-05-11 09:07:45.910826

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006a8182bb9b'
down_revision = '7a62a9d8171e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'units',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('notes', sa.String),
        sa.Column('date_created', sa.DateTime, default=datetime.utcnow),
        sa.Column('date_updated', sa.DateTime, default=datetime.utcnow),
    )

def downgrade():
    op.drop_table('units')
