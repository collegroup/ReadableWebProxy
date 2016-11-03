

import time
import urllib.parse
import pprint
import json
import datetime
import traceback
import os.path
import json
import calendar

import sqlalchemy.exc
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from sqlalchemy import func

import common.database as db

import common.get_rpyc
import common.LogBase as LogBase
import settings
from WebMirror.NewJobQueue import buildjob




class NuHeader(LogBase.LoggerMixin):
	'''
		NU Updates are batched and only forwarded to the output periodically,
		to make timing attacks somewhat more difficult.
		It's still possible to look at execution edge-times, albeit somewhat
		smeared out by the multiple intercontinental message queues, but if that
		becomes an issue, it'll be simple enough to introduce fuzzy delays.

		Also, hurrah, I got my distributed RPC system going again, so that's nice.

		Example JSON response from distributed worker:
			{
			    "nu_release": {
			        "actual_target": "http://shiroyukitranslations.com/the-strongest-dan-god-chapter-63-dominating-business-channels/",
			        "seriesname": "The Strongest Dan God",
			        "outbound_wrapper": "http://www.novelupdates.com/extnu/134595/",
			        "groupinfo": "Shiroyukineko Translations",
			        "releaseinfo": "c63",
			        "addtime": "2016-05-30T04:16:41.351430",
			        "referrer": "https://www.novelupdates.com"
			    }
			}
	'''

	loggerPath = "Main.Neader.Nu"


	def __init__(self):
		super().__init__()

		self.db_sess = db.get_db_session(postfix='nu_header')
		self.rpc = common.get_rpyc.RemoteJobInterface("NuHeader")

	def put_job(self):
		self.log.info("Loading a row to fetch...")
		have = self.db_sess.query(db.NuReleaseItem)      \
			.join(db.NuResolvedOutbound)                 \
			.filter(db.NuReleaseItem.validated == False) \
			.having(func.count(db.NuResolvedOutbound.parent) < 3)  \
			.order_by(func.random())                     \
			.group_by(db.NuReleaseItem.id)               \
			.limit(1)

		have = have.scalar()

		if not have:
			self.log.info("No jobs to remote HEAD.")
			return

		if len(list(have.resolved)) >= 3:
			raise RuntimeError("Overresolved item that's not valid.")


		self.log.info("Putting job for url '%s'", have.outbound_wrapper)
		self.log.info("Referring page '%s'", have.referrer)
		raw_job = buildjob(
			module         = 'NUWebRequest',
			call           = 'getHeadPhantomJS',
			dispatchKey    = "fetcher",
			jobid          = -1,
			args           = [have.outbound_wrapper, have.referrer],
			kwargs         = {},
			additionalData = {
				'mode'        : 'fetch',
				'wrapper_url' : have.outbound_wrapper,
				'referrer'    : have.referrer
				},
			postDelay      = 0,
			unique_id      = have.outbound_wrapper
		)

		self.rpc.put_job(raw_job)


	def process_avail(self):
		'''
		Example response:

		{
			'call': 'getHeadPhantomJS',
			'cancontinue': True,
			'dispatch_key': 'fetcher',
			'extradat': {'mode': 'fetch'},
			'jobid': -1,
			'jobmeta': {'sort_key': 'a269f164a16e11e6891500163ef6fe07'},
			'module': 'NUWebRequest',
			'ret': 'http://lightnovels.world/the-nine-godheads/nine-godheads-chapter-74/',
			'success': True,
			'user': 'scrape-worker-2',
			'user_uuid': 'urn:uuid:0a243518-834f-46d8-b34c-7f2afd20d37f'
		 }

		'''
		new = self.rpc.get_job()
		print(new)
		expected_keys = ['call', 'cancontinue', 'dispatch_key', 'extradat', 'jobid',
					'jobmeta', 'module', 'ret', 'success', 'user', 'user_uuid']
		if new is None:
			self.log.info("No NU Head requests!")
			return

		try:
			self.log.info("Processing remote head response: %s")
			assert all([key in new for key in expected_keys])
			assert new['call'] == 'getHeadPhantomJS'

			assert 'referrer'    in new['extradat']
			assert 'wrapper_url' in new['extradat']

			have = self.db_sess.query(db.NuReleaseItem)                                    \
				.options(joinedload('resolved'))                                           \
				.filter(db.NuReleaseItem.outbound_wrapper==new['extradat']['wrapper_url']) \
				.filter(db.NuReleaseItem.referrer==new['extradat']['referrer'])            \
				.one()

			new = db.NuResolvedOutbound(
					client_id      = new['user'],
					client_key     = new['user_uuid'],
					actual_target  = new['ret'],
					fetched_on     = datetime.datetime.now(),
				)

			have.resolved.append(new)
			self.db_sess.commit()
		except Exception:
			self.log.error("Error when processing job response!")
			for line in traceback.format_exc().split("\n"):
				self.log.error(line)

			self.log.error("Contents of head response:")

			for line in pprint.pformat(new).split("\n"):
				self.log.error(line)
