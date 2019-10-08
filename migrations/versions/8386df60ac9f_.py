"""empty message

Revision ID: 8386df60ac9f
Revises: 4cca6239c5f7
Create Date: 2019-10-08 01:52:34.944566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8386df60ac9f'
down_revision = '4cca6239c5f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('site_vars',
    sa.Column('var', sa.String(), nullable=False),
    sa.Column('val', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('var')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('site_vars')
    # ### end Alembic commands ###