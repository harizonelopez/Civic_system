"""Add national ID to users

Revision ID: bfba7181ef44
Revises: 7f188d8ef474
Create Date: 2026-11-22 20:30:23.701312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfba7181ef44'
down_revision = '7f188d8ef474'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('national_id', sa.String(length=8), nullable=True)
        )
        batch_op.create_unique_constraint(
            'uq_users_national_id',
            ['national_id']
        )


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(
            'uq_users_national_id',
            type_='unique'
        )
        batch_op.drop_column('national_id')
