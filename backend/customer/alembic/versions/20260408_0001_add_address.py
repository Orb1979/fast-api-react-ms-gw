"""add address to customer"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260408_0002"
down_revision: Union[str, Sequence[str], None] = "20260407_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("customer", sa.Column("address", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("customer", "address")
