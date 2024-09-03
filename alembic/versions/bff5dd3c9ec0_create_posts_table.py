"""Create posts table

Revision ID: bff5dd3c9ec0
Revises: 
Create Date: 2024-08-20 12:49:01.215942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bff5dd3c9ec0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(),nullable=False, primary_key = True),
                    sa.Column('title', sa.String(),nullable=False))
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
