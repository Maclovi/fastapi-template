"""init tables

Revision ID: 2cd846da1754
Revises: 
Create Date: 2024-10-19 13:48:35.536076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cd846da1754'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('breeds',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_breeds')),
    sa.UniqueConstraint('title', name=op.f('uq_breeds_title'))
    )
    op.create_table('cats',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('color', sa.String(length=30), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('breed_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['breed_id'], ['breeds.id'], name=op.f('fk_cats_breed_id_breeds'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_cats'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cats')
    op.drop_table('breeds')
    # ### end Alembic commands ###
