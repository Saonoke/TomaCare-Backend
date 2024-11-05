"""initial migration

Revision ID: f363c5d5885b
Revises:
Create Date: 2024-10-28 12:35:10.425106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import enum

# revision identifiers, used by Alembic.
revision: str = 'f363c5d5885b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

class ClResult(enum.Enum):
    SEHAT='Sehat'
    SAKIT='Sakit'

class PlCond(enum.Enum):
    SEHAT='Sehat'
    SAKIT='Sakit'

class LikeCond(enum.Enum):
    like=1
    netral=0
    dislike=-1

def upgrade() -> None:
    op.create_table('images',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('image_path', sa.Text(), nullable=False),
    )

    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('email', sa.String(50), nullable=False, unique=True),
        sa.Column('password', sa.String(100), nullable=False),
        sa.Column('profile_img', sa.Integer(), default=0)
    )
    op.create_foreign_key(
        None,
        source_table='users',
        referent_table='images',
        local_cols=['profile_img'],
        remote_cols=['id']
    )

    op.create_table('plants',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('condition', sa.Enum(PlCond), nullable=False),
        sa.Column('image_id', sa.Integer(), default=0)
    )
    op.create_foreign_key(
        None,
        source_table='plants',
        referent_table='images',
        local_cols=['image_id'],
        remote_cols=['id']
    )
    op.create_foreign_key(
        None,
        source_table='plants',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id']
    )

    op.create_table('results',
        sa.Column('plant_id', sa.Integer),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('classification_result', sa.Enum(ClResult), nullable=False)
    )
    op.create_foreign_key(
        None,
        source_table='results',
        referent_table='plants',
        local_cols=['plant_id'],
        remote_cols=['id']
    )

    op.create_table('posts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('image_id', sa.Integer(), default=0),
        sa.Column('title', sa.Text(100), nullable=True),
        sa.Column('body', sa.Text(1000), nullable=True),

    )
    
    op.create_foreign_key(
        None,
        source_table='posts',
        referent_table='images',
        local_cols=['image_id'],
        remote_cols=['id']
    )
    op.create_foreign_key(
        None,
        source_table='posts',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id']
    )
    
    op.create_table('likes',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('like', sa.Enum(LikeCond), nullable=False),
    )

    op.create_foreign_key(
        None,
        source_table='likes',
        referent_table='posts',
        local_cols=['post_id'],
        remote_cols=['id']
    )
    op.create_foreign_key(
        None,
        source_table='likes',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id']
    )

    op.create_table('comments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.column('comments', sa.Text(1000))
    )
    op.create_foreign_key(
        None,
        source_table='comments',
        referent_table='posts',
        local_cols=['post_id'],
        remote_cols=['id']
    )
    op.create_foreign_key(
        None,
        source_table='comments',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id']
    )


def downgrade() -> None:
    op.drop_table('results')
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('likes')
    op.drop_table('plants')
    op.drop_table('users')
    op.drop_table('images')
