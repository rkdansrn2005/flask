"""empty message

Revision ID: 73df53323ae2
Revises: 8a21aff891fd
Create Date: 2020-08-06 17:48:28.522983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73df53323ae2'
down_revision = '8a21aff891fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_voter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name=op.f('fk_question_voter_question_id_question'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_question_voter_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'question_id', name=op.f('pk_question_voter'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question_voter')
    # ### end Alembic commands ###
