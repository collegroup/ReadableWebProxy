import sys
import multiprocessing
import threading
import time
import traceback
import queue
import random
import datetime
import signal
import socket
import runStatus

# import sqlalchemy.exc
# from sqlalchemy.sql import text

if '__pypy__' in sys.builtin_module_names:
	import psycopg2cffi as psycopg2
else:
	import psycopg2

import sys

import settings
import common.NetlocThrottler
import common.LogBase as LogBase
# import WebMirror.OutputFilters.AmqpInterface
import RawArchiver.misc
import common.get_rpyc

import WebMirror.JobUtils
import common.util.urlFuncs

########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################



NO_JOB_TIMEOUT_MINUTES = 15


largv = [tmp.lower() for tmp in sys.argv]
if "twoprocess" in largv or "oneprocess" in largv:
	MAX_IN_FLIGHT_JOBS = 2
else:
	# MAX_IN_FLIGHT_JOBS = 5
	# MAX_IN_FLIGHT_JOBS = 50
	# MAX_IN_FLIGHT_JOBS = 75
	MAX_IN_FLIGHT_JOBS = 250
	# MAX_IN_FLIGHT_JOBS = 500
	# MAX_IN_FLIGHT_JOBS = 1000
	# MAX_IN_FLIGHT_JOBS = 3000



class RawJobFetcher(LogBase.LoggerMixin):

	loggerPath = "Main.RawJobFetcher"

	def __init__(self, start_thread=True):
		# print("Job __init__()")
		super().__init__()

		self.last_rx = datetime.datetime.now()
		self.active_jobs = 0
		self.jobs_out = 0
		self.jobs_in = 0

		self.run_flag = multiprocessing.Value("b", 1, lock=False)

		self.ratelimiter = common.NetlocThrottler.NetlockThrottler(fifo_limit = 1000 * 1000 * 10)

		self.db_interface = psycopg2.connect(
				database = settings.DATABASE_DB_NAME,
				user     = settings.DATABASE_USER,
				password = settings.DATABASE_PASS,
				host     = settings.DATABASE_IP,
			)

		# This queue has to be a multiprocessing queue, because it's shared across multiple processes.
		self.normal_out_queue  = multiprocessing.Queue(maxsize=MAX_IN_FLIGHT_JOBS * 2)
		self.j_fetch_proc = None
		if start_thread:
			self.j_fetch_proc = threading.Thread(target=self.queue_filler_proc)
			self.j_fetch_proc.start()

		self.print_mod = 0

	def outbound_job_wanted(self, netloc, joburl):

		bad = common.util.urlFuncs.hasDuplicatePathSegments(joburl)
		if bad:
			self.log.warn("Unwanted URL (pathchunks): '%s' - %s", joburl, bad)
			return False

		if joburl.startswith("data:"):
			self.log.warn("Data URL: '%s' - %s", joburl, netloc)
			return False
		if joburl.startswith("mailto:"):
			self.log.warn("Email URL: '%s' - %s", joburl, netloc)
			return False
		if not joburl.startswith("http"):
			self.log.warn("Non HTTP URL: '%s' - %s", joburl, netloc)
			return False
		for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
			if module.cares_about_url(joburl):
				return True

		self.log.warn("Unwanted URL: '%s' - %s", joburl, netloc)

		return False

	def outbound_job_disabled(self, netloc, joburl):

		for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
			if module.cares_about_url(joburl):
				if module.is_disabled(netloc, joburl):
					self.log.warn("Disabled fetching for URL: '%s' - %s", joburl, netloc)
					return True
		return False

	def get_queue(self):
		return self.normal_out_queue

	def join_proc(self):
		self.run_flag.value = 0

		for _ in range(60 * 5):
			self.j_fetch_proc.join(timeout=1)
			if self.j_fetch_proc.is_alive() is False:
				return
			self.log.info("Waiting for job dispatcher to join. Currently active jobs in queue: %s",
					self.normal_out_queue.qsize()
				)

		while True:
			self.j_fetch_proc.join(timeout=1)
			if self.j_fetch_proc.is_alive() is False:
				return
			self.log.error("Timeout when waiting for join. Bulk consuming from intermediate queue.")
			try:
				while 1:
					self.normal_out_queue.get_nowait()
			except queue.Empty:
				pass


	def put_outbound_job(self, jobid, joburl, netloc=None):
		self.active_jobs += 1
		self.log.info("Dispatching new job (active jobs: %s of %s)", self.active_jobs, MAX_IN_FLIGHT_JOBS)
		self.jobs_out += 1
		raw_job = WebMirror.JobUtils.buildjob(
			module         = 'WebRequest',
			call           = 'getItem',
			dispatchKey    = "fetcher",
			jobid          = jobid,
			args           = [joburl],
			kwargs         = {},
			additionalData = {'mode' : 'fetch', 'netloc' : netloc},
			postDelay      = 0
		)

		# Recycle the rpc interface if it ded
		while 1:
			try:
				self.rpc_interface.put_job(raw_job)
				return
			except TypeError:
				self.open_rpc_interface()
			except KeyError:
				self.open_rpc_interface()
			except socket.timeout:
				self.open_rpc_interface()
			except ConnectionRefusedError:
				self.open_rpc_interface()

	def fill_jobs(self):

		if 'drain' in sys.argv:
			return
		escape_count = 0
		while self.active_jobs < MAX_IN_FLIGHT_JOBS and escape_count < 25:
			old = self.normal_out_queue.qsize()
			num_new = self._get_task_internal()
			self.log.info("Need to add jobs to the job queue (%s active, %s added)!", self.active_jobs, self.active_jobs-old)

			if self.run_flag.value != 1:
				return

			new_j_l =self.ratelimiter.get_available_jobs()

			for rid, joburl, netloc in new_j_l:
				self.put_outbound_job(rid, joburl, netloc)

			# If there weren't any new items, stop looping because we're not going anywhere.
			if num_new == 0:
				break

			escape_count += 1

			self.process_responses()

	def open_rpc_interface(self):
		try:
			self.rpc_interface.close()
		except Exception:
			pass
		self.rpc_interface = common.get_rpyc.RemoteJobInterface("RawMirror")




	def process_responses(self):
		while 1:

			# Something in the RPC stuff is resulting in a typeerror I don't quite
			# understand the source of. anyways, if that happens, just reset the RPC interface.
			try:
				tmp = self.rpc_interface.get_job()
			except queue.Empty:
				return

			except TypeError:
				self.open_rpc_interface()
				return
			except KeyError:
				self.open_rpc_interface()
				return
			except socket.timeout:
				self.open_rpc_interface()
				return
			except ConnectionRefusedError:
				self.open_rpc_interface()
				return

			if tmp:



				nl = None
				if 'extradat' in tmp and 'netloc' in tmp['extradat']:
					nl = tmp['extradat']['netloc']

				if nl:
					if 'success' in tmp and tmp['success']:
						self.ratelimiter.netloc_ok(nl)
					else:
						print("Success val: ", 'success' in tmp, list(tmp.keys()))
						self.ratelimiter.netloc_error(nl)
				else:
					self.log.warning("Missing netloc in response extradat!")



				self.active_jobs -= 1
				self.jobs_in += 1
				if self.active_jobs < 0:
					self.active_jobs = 0
				self.log.info("Job response received. Jobs in-flight: %s (qsize: %s)", self.active_jobs, self.normal_out_queue.qsize())
				self.last_rx = datetime.datetime.now()
				self.blocking_put_response(("processed", tmp))
			else:
				self.print_mod += 1
				if self.print_mod > 20:
					self.log.info("No job responses available.")
					self.print_mod = 0
				time.sleep(1)
				break

	def blocking_put_response(self, item):
		while self.run_flag.value == 1:
			try:
				self.normal_out_queue.put_nowait(item)
				return
			except queue.Full:
				self.log.warning("Response queue full (%s items). Sleeping", self.normal_out_queue.qsize())
				time.sleep(1)

	def queue_filler_proc(self):

		self.open_rpc_interface()

		try:
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		except ValueError:
			self.log.warning("Cannot configure job fetcher task to ignore SIGINT. May be an issue.")

		self.log.info("Job queue fetcher starting.")

		msg_loop = 0
		while self.run_flag.value == 1:
			self.fill_jobs()
			self.process_responses()

			msg_loop += 1
			time.sleep(0.2)
			if msg_loop > 250:
				self.log.info("Job queue filler process. Current job queue size: %s (out: %s, in: %s). Runstate: %s", self.active_jobs, self.jobs_out, self.jobs_in, self.run_flag.value==1)
				msg_loop = 0
				self.ratelimiter.job_reduce()


		self.log.info("Job queue fetcher saw exit flag. Halting.")
		self.rpc_interface.close()

		# Consume the remaining items in the output queue so it shuts down cleanly.
		try:
			while 1:
				self.normal_out_queue.get_nowait()
		except queue.Empty:
			pass

		self.log.info("Job queue filler process. Current job queue size: %s. ", self.active_jobs)
		self.log.info("Job queue fetcher halted.")

	def _get_task_internal(self):

		cursor = self.db_interface.cursor()
		# Hand-tuned query, I couldn't figure out how to
		# get sqlalchemy to emit /exactly/ what I wanted.
		# TINY changes will break the query optimizer, and
		# the 10 ms query will suddenly take 10 seconds!
		raw_query = '''
				UPDATE
				    raw_web_pages
				SET
				    state = 'fetching'
				WHERE
				    raw_web_pages.id IN (
				        SELECT
				            raw_web_pages.id
				        FROM
				            raw_web_pages
				        WHERE
				            raw_web_pages.state = 'new'
				        AND
				            raw_web_pages.priority <= (
				               SELECT
				                    min(priority)
				                FROM
				                    raw_web_pages
				                WHERE
				                    state = 'new'::dlstate_enum
				                AND
				                    raw_web_pages.ignoreuntiltime < now() + '5 minutes'::interval
				            ) + 1
				        AND
				            raw_web_pages.ignoreuntiltime < now() + '5 minutes'::interval
				        LIMIT {in_flight}
				    )
				AND
				    raw_web_pages.state = 'new'
				RETURNING
				    raw_web_pages.id, raw_web_pages.netloc, raw_web_pages.url;
			'''.format(in_flight=min((MAX_IN_FLIGHT_JOBS, 150)))


		start = time.time()

		while self.run_flag.value == 1:
			try:
				cursor.execute(raw_query)
				rids = cursor.fetchall()
				self.db_interface.commit()
				break
			except psycopg2.Error:
				delay = random.random() / 3
				# traceback.print_exc()
				self.log.warn("Error getting job (psycopg2.Error)! Delaying %s.", delay)
				time.sleep(delay)
				self.db_interface.rollback()

		if self.run_flag.value != 1:
			return 0

		if not rids:
			return 0

		rids = list(rids)
		# If we broke because a user-interrupt, we may not have a
		# valid rids at this point.
		if self.run_flag.value != 1:
			return 0

		xqtim = time.time() - start

		if not rids:
			self.log.warning("No jobs available! Sleeping for 5 seconds waiting for new jobs to become available!")
			for dummy_x in range(5):
				if self.run_flag.value == 1:
					time.sleep(1)
			return 0

		if xqtim > 0.5:
			self.log.error("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		elif xqtim > 0.1:
			self.log.warn("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		else:
			self.log.info("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))

		for rid, netloc, joburl in rids:
			try:

				# If we don't have a thread affinity, do distributed fetch.
				# If we /do/ have a thread affinity, fetch locally.

				if not self.outbound_job_wanted(netloc, joburl):
					self.delete_job(rid, joburl)
					continue
				if self.outbound_job_disabled(netloc, joburl):
					self.disable_job(rid, joburl)
					continue

				threadn = RawArchiver.misc.thread_affinity(joburl, 1)
				if threadn is True:
					self.ratelimiter.put_job(rid, joburl, netloc)
					# self.put_outbound_job(rid, joburl, netloc=netloc)
				else:
					self.blocking_put_response(("unfetched", rid))

			except RawArchiver.misc.UnwantedUrlError:
				self.log.warning("Unwanted url in database? Url: '%s'", joburl)
				self.log.warning("Deleting entry.")
				cursor.execute("""DELETE FROM raw_web_pages WHERE url = %s AND id = %s;""", (joburl, rid))
				self.db_interface.commit()


		cursor.close()

		return len(rids)

	def delete_job(self, rid, joburl):
		self.log.warning("Deleting job for url: '%s'", joburl)
		cursor = self.db_interface.cursor()
		cursor.execute("""DELETE FROM raw_web_pages WHERE raw_web_pages.id = %s AND raw_web_pages.url = %s;""", (rid, joburl))
		self.db_interface.commit()


	def disable_job(self, rid, joburl):
		self.log.warning("Disabling job for url: '%s'", joburl)
		cursor = self.db_interface.cursor()
		cursor.execute("""UPDATE raw_web_pages SET state = %s WHERE raw_web_pages.id = %s AND raw_web_pages.url = %s;""", ('disabled', rid, joburl))
		self.db_interface.commit()

	def get_status(self):
		if self.j_fetch_proc:
			return "Worker: %s, alive: %s." % (self.j_fetch_proc.ident, self.j_fetch_proc.is_alive())

		return "Worker is none! Error!"

def test2():
	import logSetup
	import pprint
	logSetup.initLogging()

	agg = RawJobAggregator()
	outq = agg.get_queues()
	for x in range(20):
		print("Sleeping, ", x)
		time.sleep(1)
		try:
			j = outq.get_nowait()
			print("Received job! %s", len(j))
			with open("jobs.txt", "a") as fp:
				fp.write("\n\n\n")
				fp.write(pprint.pformat(j))
			print(j)
		except queue.Empty:
			pass
	print("Joining on the aggregator")
	agg.join_proc()
	print("Joined.")

if __name__ == "__main__":
	test2()


