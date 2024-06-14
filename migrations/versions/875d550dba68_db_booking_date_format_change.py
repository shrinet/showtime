"""DB booking date format change

Revision ID: 875d550dba68
Revises: e23b78e77f6b
Create Date: 2023-04-09 18:12:08.641837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '875d550dba68'
down_revision = 'e23b78e77f6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.DATE(),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.String(length=100),
               type_=sa.DATE(),
               existing_nullable=False)

    # ### end Alembic commands ###
