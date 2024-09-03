"""Add content columnto post table

Revision ID: d58924a949d6
Revises: bff5dd3c9ec0
Create Date: 2024-08-20 13:15:44.264954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd58924a949d6'
down_revision: Union[str, None] = 'bff5dd3c9ec0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
