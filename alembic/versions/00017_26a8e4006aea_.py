"""empty message

Revision ID: 26a8e4006aea
Revises: 59204390db12
Create Date: 2016-10-31 03:07:24.873419

"""

# revision identifiers, used by Alembic.
revision = '26a8e4006aea'
down_revision = '59204390db12'
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



def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_feed_pages_contenturl'), 'feed_pages', ['contenturl'], unique=False)
    op.create_index(op.f('ix_feed_pages_feedurl'), 'feed_pages', ['feedurl'], unique=False)
    op.create_index(op.f('ix_feed_pages_type'), 'feed_pages', ['type'], unique=False)
    op.create_index(op.f('ix_nu_outbound_wrappers_released_on'), 'nu_outbound_wrappers', ['released_on'], unique=False)
    op.drop_index('nu_outbound_wrappers_released_on_idx', table_name='nu_outbound_wrappers')
    op.drop_index('web_pages_file', table_name='web_pages')

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('web_pages_file', 'web_pages', ['file'], unique=False)
    op.create_index('nu_outbound_wrappers_released_on_idx', 'nu_outbound_wrappers', ['released_on'], unique=False)
    op.drop_index(op.f('ix_nu_outbound_wrappers_released_on'), table_name='nu_outbound_wrappers')
    op.drop_index(op.f('ix_feed_pages_type'), table_name='feed_pages')
    op.drop_index(op.f('ix_feed_pages_feedurl'), table_name='feed_pages')
    op.drop_index(op.f('ix_feed_pages_contenturl'), table_name='feed_pages')
    ### end Alembic commands ###
