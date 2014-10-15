#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
import gevent.monkey
gevent.monkey.patch_all()

import gevent
from gevent.queue import Queue
import parsedatetime
import twitter

from datetime import datetime, timedelta
import time
import math

__version__ = "0.1.0"


class Churros(object):
	""" Don't forget to set the timezone first!

		import os, time
		os.environ['TZ'] = "Australia/Sydney"
		time.tzset()

		auth - a tuple/list with the information from the Twitter dev site:
				(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	"""

	dry = False
	auth = None
	day = "Thursday"
	start = "1900"  # 24h; %H%M format.
	length = 1  # length in hours
	prewarn = 6  # 6 hours prior start tweeting.

	def __init__(self):
		if self.auth is None:
			raise RuntimeError("No auth tokens set.")
		self.t = twitter.Twitter(auth=twitter.OAuth(*self.auth))
		self.cal = parsedatetime.Calendar()
		#self.queue = Queue()
		self.events = []
		self.prep_events()

	def name(self, hours):
		return "{0} hour{s} until Some Event.".format(
			hours,
			"s" if hours != 1 else ""
		)

	def starting(self):
		return "Some Event is starting!"

	def finished(self):
		return "Some Event is over!"

	def tweet(self, text):
		print("[TWEET]", text)
		if self.dry:
			print("dry, not tweeting")
			return
		self.t.statuses.update(status=text)

	def right_day(self):
		return time.strftime("%A") == self.day

	def next_event(self):
		n = self.cal.parse("{0}, {1}".format(self.day, self.start))
		if self.right_day():  # correct day of week
			if time.strftime("%H%M") >= self.start:  # we've passed the event
				return n
			return self.cal.parse(self.start)
		return n

	def prep_events(self):
		if len(self.events) > 0:
			# Nope.
			return
		ne = self.next_event()
		now = datetime.now()
		event = datetime(*ne[0][:7])

		# Add prewarning tweets.
		for i in xrange(self.prewarn):
			delta = timedelta(hours=i+1)  # +1 since i starts at 0
			self.events.insert(0, (event - delta, self.name(i+1)))
		# Event begins!
		self.events.append((event, self.starting())
		# Add 'event finished' tweet.
		self.events.append((event + timedelta(hours=self.length),
							self.finished()))

		# Trim events we've already passed.
		self.events[:] = [e for e in self.events if e[0] > now]

	def loop(self):
		while True:
			if len(self.events) == 0:
				self.prep_events()

			now = datetime.now()
			if now < self.events[0][0]:
				#print(now, "<", self.events[0][0])
				gevent.sleep(10)
				continue

			event = self.events.pop(0)
			self.tweet(event[1])
