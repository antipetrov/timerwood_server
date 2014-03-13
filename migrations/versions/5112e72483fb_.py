"""empty message

Revision ID: 5112e72483fb
Revises: 10ac36852c1b
Create Date: 2014-03-13 20:34:46.034299

"""

# revision identifiers, used by Alembic.
revision = '5112e72483fb'
down_revision = '10ac36852c1b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timer_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=True),
    sa.Column('code_type', sa.Enum('master', 'guest'), nullable=True),
    sa.Column('timer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['timer_id'], ['timer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timer_code')
    ### end Alembic commands ###