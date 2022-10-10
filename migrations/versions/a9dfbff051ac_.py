"""empty message

Revision ID: a9dfbff051ac
Revises: 
Create Date: 2022-10-10 00:01:18.091276

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a9dfbff051ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=True),
                    sa.Column('last_name', sa.String(), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###