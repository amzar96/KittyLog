"""cat dob

Revision ID: 86dc470e01b4
Revises: db2f20872a10
Create Date: 2024-10-31 12:41:24.962080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86dc470e01b4'
down_revision: Union[str, None] = 'db2f20872a10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cat', sa.Column('dob', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cat', 'dob')
    # ### end Alembic commands ###