"""coops name index added

Revision ID: 0fcac8534431
Revises: f3a356122c16
Create Date: 2024-09-22 23:09:55.657751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fcac8534431'
down_revision: Union[str, None] = 'f3a356122c16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_coops_name'), 'coops', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_coops_name'), table_name='coops')
    # ### end Alembic commands ###
