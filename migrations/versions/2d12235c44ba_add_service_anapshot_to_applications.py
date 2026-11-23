"""Add service snapshot to applications

Revision ID: 2d12235c44ba
Revises: a69a21ba9c0c
Create Date: 2026-11-21 11:59:21.038695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d12235c44ba'
down_revision = 'a69a21ba9c0c'
branch_labels = None
depends_on = None


def upgrade():
    # First add the column as nullable.
    with op.batch_alter_table('service_requests', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('service_snapshot', sa.JSON(), nullable=True)
        )

    # Give existing applications an empty JSON object.
    op.execute(
        "UPDATE service_requests "
        "SET service_snapshot = '{}' "
        "WHERE service_snapshot IS NULL"
    )

    # Now make the column non-nullable.
    with op.batch_alter_table('service_requests', schema=None) as batch_op:
        batch_op.alter_column(
            'service_snapshot',
            existing_type=sa.JSON(),
            nullable=False
        )


def downgrade():
    with op.batch_alter_table('service_requests', schema=None) as batch_op:
        batch_op.drop_column('service_snapshot')
