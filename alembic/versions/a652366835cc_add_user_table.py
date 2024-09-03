"""Add user table

Revision ID: a652366835cc
Revises: d58924a949d6
Create Date: 2024-08-20 13:20:44.072405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a652366835cc'
down_revision: Union[str, None] = 'd58924a949d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'), # Primary constraint added at the end
        sa.UniqueConstraint('email')
    )



def downgrade() -> None:
    op.drop_table('users')
    pass
