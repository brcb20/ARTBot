"""slugs

Revision ID: 146536b92528
Revises: c902975ece6d
Create Date: 2020-01-08 09:23:27.646664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '146536b92528'
down_revision = 'c902975ece6d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('new_artpieces',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=60), nullable=False),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('submit_date', sa.DateTime(), nullable=False),
        sa.Column('art_encoding', sa.JSON(), nullable=False),
        sa.Column('submission_status'
        , sa.Enum('Submitted', 'Processing', 'Processed', name='submissionstatus')
        , nullable=False),
        sa.Column('raw_image', sa.LargeBinary(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('confirmed', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.execute(("INSERT INTO "
        "new_artpieces("
        "id, slug, title, submit_date, art_encoding, submission_status, raw_image, user_id, "
        "confirmed) "
        "SELECT "
        "id, 'DEFAULT', title, submit_date, art_encoding, submission_status, raw_image, "
        "user_id, confirmed "
        "FROM artpieces ")
    )
    op.drop_table('artpieces')
    op.execute('ALTER TABLE new_artpieces RENAME TO artpieces')

    from migrations.scripts import slug_upgrade

    op.create_index(op.f('ix_artpieces_slug'), 'artpieces', ['slug'], unique=True)


def downgrade():
    op.create_table('new_artpieces',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('submit_date', sa.DateTime(), nullable=False),
        sa.Column('art_encoding', sa.JSON(), nullable=False),
        sa.Column('submission_status'
        , sa.Enum('Submitted', 'Processing', 'Processed', name='submissionstatus')
        , nullable=False),
        sa.Column('raw_image', sa.LargeBinary(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('confirmed', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.execute(("INSERT INTO "
        "new_artpieces("
        "id, title, submit_date, art_encoding, submission_status, raw_image, user_id, confirmed) "
        "SELECT "
        "id, title, submit_date, art_encoding, submission_status, raw_image, user_id, confirmed "
        "FROM artpieces ")
    )
    op.drop_table('artpieces')
    op.execute('ALTER TABLE new_artpieces RENAME TO artpieces')
