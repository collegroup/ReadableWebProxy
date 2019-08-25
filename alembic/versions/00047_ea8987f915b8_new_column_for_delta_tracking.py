"""New column for delta tracking

Revision ID: ea8987f915b8
Revises: 4f22490b9071
Create Date: 2019-08-25 00:08:42.160373

"""

# revision identifiers, used by Alembic.
revision = 'ea8987f915b8'
down_revision = '4f22490b9071'
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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TSVECTOR
ischema_names['citext'] = citext.CIText

from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('raw_web_pages_version', sa.Column('is_delta', sa.Boolean(), nullable=True, default=False))
    op.add_column('rss_parser_feed_name_lut_version', sa.Column('is_delta', sa.Boolean(), nullable=True, default=False))
    op.add_column('rss_parser_funcs_version', sa.Column('is_delta', sa.Boolean(), nullable=True, default=False))
    op.add_column('web_pages_version', sa.Column('is_delta', sa.Boolean(), nullable=True, default=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('web_pages_version', 'is_delta')
    op.drop_column('rss_parser_funcs_version', 'is_delta')
    op.drop_column('rss_parser_feed_name_lut_version', 'is_delta')
    op.drop_column('raw_web_pages_version', 'is_delta')

    # ### end Alembic commands ###