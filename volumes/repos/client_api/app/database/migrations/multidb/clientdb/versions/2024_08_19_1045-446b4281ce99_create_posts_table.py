"""create posts table

Revision ID: 446b4281ce99
Revises: 
Create Date: 2024-08-19 10:45:57.130308+00:00

"""
import uuid
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = '446b4281ce99'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True, nullable=False),
            sa.Column('uuid', sa.Uuid(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4),
            sa.Column('title'  , sa.String(length=100), index=True, nullable=False),
            sa.Column('content', sa.Text, nullable=False),
            sa.Column('published', sa.Boolean, default=True, nullable=False),
            sa.Column('rating', sa.Float, default=0.0, nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
            sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
            sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True, server_default=text('null')),
    )


def downgrade() -> None:
    op.drop_table('posts')
