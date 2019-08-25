"""empty message

Revision ID: 9abd467440df
Revises: d37cc90c5586
Create Date: 2016-10-30 23:55:43.694941

"""

# revision identifiers, used by Alembic.
revision = '9abd467440df'
down_revision = 'd37cc90c5586'
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
    op.alter_column('feed_author', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('feed_authors_link', 'author_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('feed_authors_link', 'releases_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('feed_pages', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('feed_tags', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('feed_tags_link', 'releases_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('feed_tags_link', 'tags_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('nu_outbound_wrappers', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    op.alter_column('plugin_status', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger())
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('plugin_status', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('nu_outbound_wrappers', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('feed_tags_link', 'tags_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('feed_tags_link', 'releases_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('feed_tags', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('feed_pages', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('feed_authors_link', 'releases_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('feed_authors_link', 'author_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    op.alter_column('feed_author', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER())
    ### end Alembic commands ###