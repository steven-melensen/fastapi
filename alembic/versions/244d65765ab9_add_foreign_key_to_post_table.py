"""add foreign key to post table

Revision ID: 244d65765ab9
Revises: a652366835cc
Create Date: 2024-08-20 13:28:02.824977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '244d65765ab9'
down_revision: Union[str, None] = 'a652366835cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('post_users_fk', 
                          source_table = 'posts', 
                          referent_table='users',
                          local_cols=['owner_id'], 
                          remote_cols=['id'], 
                          ondelete='CASCADE')

def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    
    