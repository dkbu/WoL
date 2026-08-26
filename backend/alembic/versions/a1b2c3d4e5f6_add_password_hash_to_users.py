"""add password_hash to users

Revision ID: a1b2c3d4e5f6
Revises: 379d8a505a75
Create Date: 2026-08-26 00:00:00.000000

"""
from __future__ import annotations

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '379d8a505a75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # server_default is a temporary placeholder for existing rows; drop the
    # default afterwards so all future inserts must supply a real hash.
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(
            sa.Column('password_hash', sa.String(length=255), nullable=False, server_default='')
        )
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('password_hash', server_default=None)


def downgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('password_hash')
