"""Cookie Database system stuff

Revision ID: d37cc90c5586
Revises: 3b631f898e9f
Create Date: 2016-09-17 06:34:11.841957

"""

# revision identifiers, used by Alembic.
revision = 'd37cc90c5586'
down_revision = '3b631f898e9f'
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
    op.create_table('web_cookie_db',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('age', sa.DateTime(), nullable=True),
    sa.Column('ua_user_agent', sa.Text(), nullable=True),
    sa.Column('ua_accept_language', sa.Text(), nullable=True),
    sa.Column('ua_accept', sa.Text(), nullable=True),
    sa.Column('ua_accept_encoding', sa.Text(), nullable=True),
    sa.Column('c_version', sa.Integer(), nullable=True),
    sa.Column('c_name', sa.Text(), nullable=True),
    sa.Column('c_value', sa.Text(), nullable=True),
    sa.Column('c_port', sa.Integer(), nullable=True),
    sa.Column('c_port_specified', sa.Boolean(), nullable=True),
    sa.Column('c_domain', sa.Text(), nullable=True),
    sa.Column('c_domain_specified', sa.Boolean(), nullable=True),
    sa.Column('c_domain_initial_dot', sa.Boolean(), nullable=True),
    sa.Column('c_path', sa.Text(), nullable=True),
    sa.Column('c_path_specified', sa.Boolean(), nullable=True),
    sa.Column('c_secure', sa.Boolean(), nullable=True),
    sa.Column('c_expires', sa.Integer(), nullable=True),
    sa.Column('c_discard', sa.Boolean(), nullable=True),
    sa.Column('c_comment', sa.Text(), nullable=True),
    sa.Column('c_comment_url', sa.Text(), nullable=True),
    sa.Column('c_rest', sa.Text(), nullable=True),
    sa.Column('c_rfc2109', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ua_user_agent', 'ua_accept_language', 'ua_accept', 'ua_accept_encoding', 'c_version', 'c_name', 'c_value', 'c_port', 'c_port_specified', 'c_domain', 'c_domain_specified', 'c_domain_initial_dot', 'c_path', 'c_path_specified', 'c_secure', 'c_expires', 'c_discard', 'c_comment', 'c_comment_url', 'c_rest', 'c_rfc2109')
    )
    op.create_index(op.f('ix_web_cookie_db_id'), 'web_cookie_db', ['id'], unique=False)
    op.create_index('ua_user_agent', 'web_cookie_db', ['ua_accept_language', 'ua_accept', 'ua_accept_encoding'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ua_user_agent', table_name='web_cookie_db')
    op.drop_index(op.f('ix_web_cookie_db_id'), table_name='web_cookie_db')
    op.drop_table('web_cookie_db')
    ### end Alembic commands ###