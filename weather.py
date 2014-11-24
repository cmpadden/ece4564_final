#!/usr/bin/env python

import urllib
import urllib2
import json




class weather:

	def __init__(self):
		self.zipCode = int(raw_input('Enter your zip code: '))
		self.name = "Weather"
		self.priority = 0;
		self.updatePeriod = 30;
		self.updateCount = 30;

	def getName(self):
		return self.name

	def getPriority(self):
		return self.priority

	def update(self):
		if(self.updateCount == self.updatePeriod):
			query = 'http://api.wunderground.com/api/b60f147d6b774dea/hourly/q/' + str(self.zipCode) + '.json'
			weather_data = urllib2.urlopen(query)
			jsonData = weather_data.read()
			searchable = json.loads(jsonData)
			print (searchable)
			self.updateCount = 0
			return True

		else:
			self.updateCount += 1
			return False
		

