"""teste

Revision ID: 8e96e27e03f2
Revises: 
Create Date: 2020-05-08 13:42:05.275550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e96e27e03f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=100), nullable=True),
    sa.Column('_value', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('process',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('script', sa.Text(), nullable=True),
    sa.Column('perito', sa.String(length=300), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=True),
    sa.Column('start_waiting', sa.DateTime(), nullable=True),
    sa.Column('finish', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('stdout', sa.Text(), nullable=True),
    sa.Column('stderr', sa.Text(), nullable=True),
    sa.Column('telegram', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dependency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blocked_id', sa.Integer(), nullable=True),
    sa.Column('blocker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blocked_id'], ['process.id'], ),
    sa.ForeignKeyConstraint(['blocker_id'], ['process.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dependency')
    op.drop_table('process')
    op.drop_table('doc')
    # ### end Alembic commands ###
