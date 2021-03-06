

import sys

from sqlalchemy_continuum_vendored import make_versioned

from settings import DO_VERSIONING

def cares_about_change(op, row):
	table_name = row.__tablename__
	if table_name == "web_pages":
		# Ignore insert and deletes
		if op == 'insert':
			print("[continuum] Ignoring insert", row.url)
			return False
		if op == 'delete':
			print("[continuum] Ignoring delete", row.url)
			return False

		# Also ignore history where things aren't complete.
		if row.state != 'complete':
			# print("[continuum] Ignoring row update to not-complete")
			return False

		rss_mimetypes = [
							'application/atom+xml',
							'application/rdf+xml',
							'application/rss+xml',
							'application/xml',
							'text/xml',
						]
		# Also ignore history where things aren't complete.
		if row.mimetype in rss_mimetypes:
			print("[continuum] Ignoring rss row update")
			return False

		print("[continuum] Pushing row into history: %s" % (row.url, ))
		return True

	elif table_name == "raw_web_pages":
		return True

	else:
		print("[continuum] Unknown table: ", table_name)
		return True

if DO_VERSIONING:
	make_versioned(user_cls=None, options={'strategy' : 'subquery'}, cares_about_checker=cares_about_change)

# Import the DB things.
from common.main_archive_db import WebPages
from common.main_archive_db import WebFiles
from common.main_archive_db import PluginStatus
from common.main_archive_db import NuReleaseItem
from common.main_archive_db import NuResolvedOutbound

from common.raw_archive_db import RawWebPages

from common.rss_func_db import Tags
from common.rss_func_db import Author
from common.rss_func_db import RssFeedPost
from common.rss_func_db import RssFeedUrlMapper
from common.rss_func_db import RssFeedEntry
from common.rss_func_db import QidianFeedPostMeta

from common.misc_db import NewNetlocTracker
from common.misc_db import KeyValueStore
from common.misc_db import get_from_db_key_value_store
from common.misc_db import set_in_db_key_value_store
from common.misc_db import get_from_version_check_table
from common.misc_db import set_in_version_check_table

from common.cookie_db import WebCookieDb

from common.db_engine import get_engine
from common.db_engine import get_db_session
from common.db_engine import delete_db_session
from common.db_engine import session_context

from common.db_constants import DB_REALTIME_PRIORITY
from common.db_constants import DB_HIGH_PRIORITY
from common.db_constants import DB_MED_PRIORITY
from common.db_constants import DB_LOW_PRIORITY
from common.db_constants import DB_IDLE_PRIORITY
from common.db_constants import DB_DEFAULT_DIST
from common.db_constants import MAX_DISTANCE

from common.db_base import Base

from common.redis import redis_session_context

import sqlalchemy as sa
sa.orm.configure_mappers()

# from sqlalchemy_searchable import make_searchable
# make_searchable()
