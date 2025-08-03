"""remove_grades_check_constraint

Revision ID: f6170fe90d24
Revises: b8ae630b1c91
Create Date: 2025-08-03 19:16:29.815742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6170fe90d24'
down_revision: Union[str, Sequence[str], None] = 'b8ae630b1c91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the problematic check constraint
    with op.batch_alter_table('teacher_subjects', schema=None) as batch_op:
        batch_op.drop_constraint('ck_grades_not_empty', type_='check')


def downgrade() -> None:
    """Downgrade schema."""
    # Note: Not recreating the constraint on downgrade since it was problematic
    # Validation is now handled in application code
    pass
