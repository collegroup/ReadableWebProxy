"""Add rss bits!

Revision ID: 34f427187628
Revises: b88c4e0d8ed4
Create Date: 2017-02-27 02:45:31.776790

"""

# revision identifiers, used by Alembic.
revision = '34f427187628'
down_revision = 'b88c4e0d8ed4'
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
    op.create_table('rss_parser_feed_name_lut_version',
    sa.Column('id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('feed_netloc', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('feed_name', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    op.create_index(op.f('ix_rss_parser_feed_name_lut_version_end_transaction_id'), 'rss_parser_feed_name_lut_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_rss_parser_feed_name_lut_version_feed_name'), 'rss_parser_feed_name_lut_version', ['feed_name'], unique=False)
    op.create_index(op.f('ix_rss_parser_feed_name_lut_version_feed_netloc'), 'rss_parser_feed_name_lut_version', ['feed_netloc'], unique=False)
    op.create_index(op.f('ix_rss_parser_feed_name_lut_version_id'), 'rss_parser_feed_name_lut_version', ['id'], unique=False)
    op.create_index(op.f('ix_rss_parser_feed_name_lut_version_operation_type'), 'rss_parser_feed_name_lut_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_rss_parser_feed_name_lut_version_transaction_id'), 'rss_parser_feed_name_lut_version', ['transaction_id'], unique=False)
    op.create_table('rss_parser_funcs',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('feed_name', sa.Text(), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('func', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rss_parser_funcs_feed_name'), 'rss_parser_funcs', ['feed_name'], unique=True)
    op.create_index(op.f('ix_rss_parser_funcs_id'), 'rss_parser_funcs', ['id'], unique=False)
    op.create_table('rss_parser_funcs_version',
    sa.Column('id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('version', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('feed_name', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('enabled', sa.Boolean(), autoincrement=False, nullable=True),
    sa.Column('func', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    op.create_index(op.f('ix_rss_parser_funcs_version_end_transaction_id'), 'rss_parser_funcs_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_rss_parser_funcs_version_feed_name'), 'rss_parser_funcs_version', ['feed_name'], unique=False)
    op.create_index(op.f('ix_rss_parser_funcs_version_id'), 'rss_parser_funcs_version', ['id'], unique=False)
    op.create_index(op.f('ix_rss_parser_funcs_version_operation_type'), 'rss_parser_funcs_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_rss_parser_funcs_version_transaction_id'), 'rss_parser_funcs_version', ['transaction_id'], unique=False)
    op.create_table('rss_parser_feed_name_lut',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('feed_netloc', sa.Text(), nullable=False),
    sa.Column('feed_name', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['feed_name'], ['rss_parser_funcs.feed_name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('feed_netloc', 'feed_name')
    )
    op.create_index(op.f('ix_rss_parser_feed_name_lut_feed_name'), 'rss_parser_feed_name_lut', ['feed_name'], unique=False)
    op.create_index(op.f('ix_rss_parser_feed_name_lut_feed_netloc'), 'rss_parser_feed_name_lut', ['feed_netloc'], unique=False)
    op.create_index(op.f('ix_rss_parser_feed_name_lut_id'), 'rss_parser_feed_name_lut', ['id'], unique=False)


    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###

    op.drop_index(op.f('ix_rss_parser_feed_name_lut_id'), table_name='rss_parser_feed_name_lut')
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_feed_netloc'), table_name='rss_parser_feed_name_lut')
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_feed_name'), table_name='rss_parser_feed_name_lut')
    op.drop_table('rss_parser_feed_name_lut')
    op.drop_index(op.f('ix_rss_parser_funcs_version_transaction_id'), table_name='rss_parser_funcs_version')
    op.drop_index(op.f('ix_rss_parser_funcs_version_operation_type'), table_name='rss_parser_funcs_version')
    op.drop_index(op.f('ix_rss_parser_funcs_version_id'), table_name='rss_parser_funcs_version')
    op.drop_index(op.f('ix_rss_parser_funcs_version_feed_name'), table_name='rss_parser_funcs_version')
    op.drop_index(op.f('ix_rss_parser_funcs_version_end_transaction_id'), table_name='rss_parser_funcs_version')
    op.drop_table('rss_parser_funcs_version')
    op.drop_index(op.f('ix_rss_parser_funcs_id'), table_name='rss_parser_funcs')
    op.drop_index(op.f('ix_rss_parser_funcs_feed_name'), table_name='rss_parser_funcs')
    op.drop_table('rss_parser_funcs')
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_version_transaction_id'), table_name='rss_parser_feed_name_lut_version')
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_version_operation_type'), table_name='rss_parser_feed_name_lut_version')
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_version_id'), table_name='rss_parser_feed_name_lut_version')
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_version_feed_netloc'), table_name='rss_parser_feed_name_lut_version')
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_version_feed_name'), table_name='rss_parser_feed_name_lut_version')
    op.drop_index(op.f('ix_rss_parser_feed_name_lut_version_end_transaction_id'), table_name='rss_parser_feed_name_lut_version')
    op.drop_table('rss_parser_feed_name_lut_version')
    ### end Alembic commands ###
