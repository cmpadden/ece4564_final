#!/usr/bin/env python

import urllib
import urllib2
import json
import re




class WeatherService:
	#Initialization
	def __init__(self):
		#Get the user's zip code for the query
		properZipCode = 0;
		while(not properZipCode):
			temp = raw_input('Enter your zip code: ')
			if re.match('^\d{5}$', temp) is None:
				print "Invalid zipcode"
			else:
				self.zipCode = int(temp)
				properZipCode = 1
		#Name of the service
		self.name = "Weather"
		self.priority = 0
		#To be updated every 30 mins
		self.updatePeriod = 30
		#Keeps track of time since last update, set to 30 initially so an update will occur on the first run
		self.updateCount = 30
		self.theComment = ""
	
	#Returns the name of the service
	def getName(self):
		return self.name

	#Returns the current priority
	def getPriority(self):
		return self.priority

	#Updates the priority is 30 minutes have gone by
	def doUpdate(self):
		if(self.updateCount == self.updatePeriod):
			#Creation of the query
			query = 'http://api.wunderground.com/api/b60f147d6b774dea/hourly/q/' + str(self.zipCode) + '.json'
			#Gets the data in JSON formate from weather underground
			try:
				weather_data = urllib2.urlopen(query)
			except NameError:
				print "Error with querying weather underground"
			jsonData = weather_data.read()
			searchable = json.loads(jsonData)
			#Gets the forecast for the next three hours
			firstHour = searchable["hourly_forecast"][0]
			secondHour = searchable["hourly_forecast"][1]
			thirdHour = searchable["hourly_forecast"][2]
			#Flag to check if the priority has been set
			setFlag = 0
			#Sets the priority depending on the temperature
			if(float(firstHour["temp"]["english"]) < 60 or float(secondHour["temp"]["english"]) < 60 or float(thirdHour["temp"]["english"]) < 60):
				self.priority = 1
				setFlag = 1
				self.theComment = "Moderate temperature"
			if(float(firstHour["temp"]["english"]) < 40 or float(secondHour["temp"]["english"]) < 40 or float(thirdHour["temp"]["english"]) < 40):
				self.priority = 2
				setFlag = 1
				self.theComment = "Moderate temperature"
			if(float(firstHour["temp"]["english"]) < 30 or float(secondHour["temp"]["english"]) < 30 or float(thirdHour["temp"]["english"]) < 30):
				self.priority = 3
				setFlag = 1
				self.theComment = "Cold temperature"
			if(float(firstHour["temp"]["english"]) < 20 or float(secondHour["temp"]["english"]) < 20 or float(thirdHour["temp"]["english"]) < 20):
				self.priority = 4
				setFlag = 1
				self.theComment = "Cold temperature"
			if(float(firstHour["temp"]["english"]) < 10 or float(secondHour["temp"]["english"]) < 10 or float(thirdHour["temp"]["english"]) < 10):
				self.priority = 5
				setFlag = 1
				self.theComment = "Cold temperature"
			#Sets the priority depending on the rainfall if it is of greater priority than the temperature priority
			#or if a priority was not set for the temperature
			if(float(firstHour["qpf"]["english"]) > 0 or float(secondHour["qpf"]["english"]) > 0 or float(thirdHour["qpf"]["english"]) > 0):
				if(setFlag == 0 or self.priority < 1):
					self.priority = 1
					setFlag = 1
					self.theComment = "Light rain"
			if(float(firstHour["qpf"]["english"]) > 1 or float(secondHour["qpf"]["english"]) > 1 or float(thirdHour["qpf"]["english"]) > 1):
				if(setFlag == 0 or self.priority < 2):
					self.priority = 2
					setFlag = 1
					self.theComment = "Light rain"
			if(float(firstHour["qpf"]["english"]) > 2 or float(secondHour["qpf"]["english"]) > 2 or float(thirdHour["qpf"]["english"]) > 2):
				if(setFlag == 0 or self.priority < 3):
					self.priority = 3
					setFlag = 1
					self.theComment = "Moderate rain"
			if(float(firstHour["qpf"]["english"]) > 3 or float(secondHour["qpf"]["english"]) > 3 or float(thirdHour["qpf"]["english"]) > 3):
				if(setFlag == 0 or self.priority < 4):
					self.priority = 4
					setFlag = 1
					self.theComment = "Moderate rain"
			if(float(firstHour["qpf"]["english"]) > 4 or float(secondHour["qpf"]["english"]) > 4 or float(thirdHour["qpf"]["english"]) > 4):
				if(setFlag == 0 or self.priority < 5):
					self.priority = 5
					setFlag = 1
					self.theComment = "Heavy rain"
			#Sets the priority depending on the snow fall if it is of greater priority than the temperature or rain fall priority
			#or if a priority was not set for the temperature or rain fall
			if(float(firstHour["snow"]["english"]) > 0 or float(secondHour["snow"]["english"]) > 0 or float(thirdHour["snow"]["english"]) > 0):
				if(setFlag == 0 or self.priority < 2):
					self.priority = 2
					setFlag = 1
					self.theComment = "Light snow"
			if(float(firstHour["snow"]["english"]) > 1 or float(secondHour["snow"]["english"]) > 1 or float(thirdHour["snow"]["english"]) > 1):
				if(setFlag == 0 or self.priority < 3):
					self.priority = 3
					setFlag = 1
					self.theComment = "Moderate rain"
			if(float(firstHour["snow"]["english"]) > 2 or float(secondHour["snow"]["english"]) > 2 or float(thirdHour["snow"]["english"]) > 2):
				if(setFlag == 0 or self.priority < 4):
					self.priority = 4
					setFlag = 1
					self.theComment = "Moderate rain"
			if(float(firstHour["snow"]["english"]) > 3 or float(secondHour["snow"]["english"]) > 3 or float(thirdHour["snow"]["english"]) > 3):
				if(setFlag == 0 or self.priority < 5):
					self.priority = 5
					setFlag = 1
					self.theComment = "Heavy rain"
			#If no update occurs then set the priority to 0
			if(setFlag == 0):
				self.priority = 0
			self.updateCount = 0
			return True

		else:
			self.updateCount += 1
			return False

	def comment(self):
		print self.theComment
		return self.theComment
		
#For testing the class
#theWeather = WeatherService()
#theWeather.doUpdate()
#theWeather.comment()
