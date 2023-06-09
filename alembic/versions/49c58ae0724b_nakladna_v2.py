"""nakladna v2

Revision ID: 49c58ae0724b
Revises: 9944df5675a1
Create Date: 2023-05-11 16:37:11.788939

"""
from alembic import op
from sqlalchemy import Column, Integer, ForeignKey, String
import sqlalchemy as sa
from alembic.operations import Operations, MigrateOperation



# revision identifiers, used by Alembic.
revision = '49c58ae0724b'
down_revision = '9944df5675a1'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("materials") as batch_op:
        batch_op.create_foreign_key('fk_materials_odvumirs', 'odvumirs', ['id_odvumir'], ['id'])
        batch_op.create_foreign_key('fk_materials_pereliks', 'pereliks', ['id_perelik'], ['id'])

    with op.batch_alter_table("nakladnas") as batch_op:
        batch_op.add_column(Column('id_unit', Integer, nullable=True))
        batch_op.create_foreign_key('fk_nakladnas_units', 'units', ['id_unit'], ['id'])
        batch_op.drop_column('adresa1')
        batch_op.drop_column('adresa2')

    with op.batch_alter_table("resurs") as batch_op:
        batch_op.add_column(Column('number', Integer, nullable=True))
        batch_op.drop_column('inumber')

    with op.batch_alter_table("units") as batch_op:
        batch_op.create_index(op.f('ix_units_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_units_id'), table_name='units')
    op.add_column('resurs', sa.Column('inumber', sa.INTEGER(), nullable=True))
    op.drop_column('resurs', 'number')
    op.add_column('nakladnas', sa.Column('adresa2', sa.INTEGER(), nullable=True))
    op.add_column('nakladnas', sa.Column('adresa1', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'nakladnas', type_='foreignkey')
    op.drop_column('nakladnas', 'id_unit')
    op.drop_constraint(None, 'materials', type_='foreignkey')
    op.drop_constraint(None, 'materials', type_='foreignkey')
    # ### end Alembic commands ###
