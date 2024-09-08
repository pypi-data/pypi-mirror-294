"""create users table

Revision ID: d100f32b0d1f
Revises: 
Create Date: 2024-08-31 14:27:05.188218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
from alembic import op
from sqlalchemy import (
Column, DateTime, ForeignKey, Integer, String
)

from sqlalchemy.engine import reflection

def upgrade() -> None:
    conn = op.get_bind()
    inspect_obj = reflection.Inspector.from_engine(conn)
    tables = inspect_obj.get_table_names()
    if 'users' not in tables:
        op.create_table(
            'users',
            Column('id', Integer, primary_key=True, nullable=False),
            Column('username', String(255), nullable=False),
            Column('email', String(255), nullable=False),
            Column('password', String(255), nullable=False),

        )


def downgrade() -> None:
    raise NotImplementedError('downgrade is not yet implemented.')
