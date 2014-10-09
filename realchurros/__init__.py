#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
import gevent.monkey
gevent.monkey.patch_all()

import gevent
from gevent.queue import Queue
import parsedatetime
import twitter

from datetime import datetime
import time

__version__ = "0.1.0"


class Churros(object):
	""" Don't forget to set the timezone first!

		import os, time
		os.environ['TZ'] = "Australia/Sydney"
		time.tzset()
	"""

	dry = False
	auth = None
	day = "Thursday"
	time = "2200"  # 24h; %H%M format.

	def __init__(self):
		if self.auth is None:
			raise RuntimeError("No auth tokens set.")
		self.t = twitter.Twitter(auth=twitter.OAuth(*self.auth))
		self.cal = parsedatetime.Calendar()
		self.queue = Queue()

	def tweet(self, text):
		if self.dry:
			print("-->", text)
			return
		self.t.statuses.update(status=text)

	def right_day(self):
		return time.strftime("%A") == self.day

	def next_event(self):
		n = self.cal.parse("{0}, {1}".format(self.day, self.time))
		if self.right_day():  # correct day of week
			if time.strftime("%H%M") >= self.time:  # we've passed the event
				return n
			return self.cal.parse(self.time)
		return n
