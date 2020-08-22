"""empty message

Revision ID: 106a7bbeb93e
Revises: 28beeaf14055
Create Date: 2020-08-12 00:41:52.910088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '106a7bbeb93e'
down_revision = '28beeaf14055'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('myprofile', schema=None) as batch_op:
        batch_op.alter_column('age',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key(batch_op.f('fk_myprofile_username_user'), 'user', ['username'], ['username'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('myprofile', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_myprofile_username_user'), type_='foreignkey')
        batch_op.alter_column('age',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###