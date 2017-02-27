"""More rss stuff

Revision ID: c92e0c8632d7
Revises: 34f427187628
Create Date: 2017-02-27 02:49:55.768394

"""

# revision identifiers, used by Alembic.
revision = 'c92e0c8632d7'
down_revision = '34f427187628'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
import sqlalchemy_utils

# Patch in knowledge of the citext type, so it reflects properly.
from sqlalchemy.dialects.postgresql.base import ischema_names
import citext
import queue
import datetime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import TSVECTOR
ischema_names['citext'] = citext.CIText

from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rss_parser_feed_name_lut', sa.Column('feed_id', sa.BigInteger(), nullable=False))
    op.create_index(op.f('ix_rss_parser_feed_name_lut_feed_id'), 'rss_parser_feed_name_lut', ['feed_id'], unique=False)
    op.drop_index('ix_rss_parser_feed_name_lut_feed_name', table_name='rss_parser_feed_name_lut')
    op.drop_constraint('rss_parser_feed_name_lut_feed_netloc_feed_name_key', 'rss_parser_feed_name_lut', type_='unique')
    op.create_unique_constraint(None, 'rss_parser_feed_name_lut', ['feed_netloc', 'feed_id'])
    op.drop_constraint('rss_parser_feed_name_lut_feed_name_fkey', 'rss_parser_feed_name_lut', type_='foreignkey')
    op.create_foreign_key(None, 'rss_parser_feed_name_lut', 'rss_parser_funcs', ['feed_id'], ['id'])
    op.drop_column('rss_parser_feed_name_lut', 'feed_name')
    op.add_column('rss_parser_feed_name_lut_version', sa.Column('feed_id', sa.BigInteger(), autoincrement=False, nullable=True))
    op.create_index(op.f('ix_rss_parser_feed_name_lut_version_feed_id'), 'rss_parser_feed_name_lut_version', ['feed_id'], unique=False)
    op.drop_index('ix_rss_parser_feed_name_lut_version_feed_name', table_name='rss_parser_feed_name_lut_version')
    op.drop_column('rss_parser_feed_name_lut_version', 'feed_name')
    op.alter_column('rss_parser_funcs', 'func',
               existing_type=sa.TEXT(),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rss_parser_funcs', 'func',
               existing_type=sa.TEXT(),
               nullable=False)
    op.add_column('rss_parser_feed_name_lut_version', sa.Column('feed_name', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_rss_parser_feed_name_lut_version_feed_name', 'rss_parser_feed_name_lut_version', ['feed_name'], unique=False)
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_version_feed_id'), table_name='rss_parser_feed_name_lut_version')
    op.drop_column('rss_parser_feed_name_lut_version', 'feed_id')
    op.add_column('rss_parser_feed_name_lut', sa.Column('feed_name', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'rss_parser_feed_name_lut', type_='foreignkey')
    op.create_foreign_key('rss_parser_feed_name_lut_feed_name_fkey', 'rss_parser_feed_name_lut', 'rss_parser_funcs', ['feed_name'], ['feed_name'])
    op.drop_constraint(None, 'rss_parser_feed_name_lut', type_='unique')
    op.create_unique_constraint('rss_parser_feed_name_lut_feed_netloc_feed_name_key', 'rss_parser_feed_name_lut', ['feed_netloc', 'feed_name'])
    op.create_index('ix_rss_parser_feed_name_lut_feed_name', 'rss_parser_feed_name_lut', ['feed_name'], unique=False)
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_feed_id'), table_name='rss_parser_feed_name_lut')
    op.drop_column('rss_parser_feed_name_lut', 'feed_id')
    ### end Alembic commands ###
