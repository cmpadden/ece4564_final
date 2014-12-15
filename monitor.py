#!/usr/bin/env python

import pika
import sys
import json
import time
from test_service import TestService
from gmail import GmailService
from weather import WeatherService

# Instantiate the services
s1 = TestService()
#s2 = GmailService()
s3 = WeatherService()
services = [s1, s3];

try:
	#connect to message broker
	msg_broker = pika.BlockingConnection(
		pika.ConnectionParameters(host="netapps.ece.vt.edu",
								  virtual_host="sandbox",
								  credentials=pika.PlainCredentials("ECE4564-Fall2014",
								  									 "13ac0N!",
								  									 True)))
	#setup Exchange
	channel = msg_broker.channel()
	channel.exchange_declare(exchange="services", type="direct")

	while(1):
		dataString = ''
		data = {}
		for service in services:
			
			if service.doUpdate():								# If the service should be updated
				try:
					if hasattr(service, 'comment'):
						service.comment()
					data[service.getName()] = service.getPriority()	# Add the name and priority to the dict
					dataString = json.dumps(data)					# Dump the data to json
				except:
					print("Unable to update " + service.getName() + ", skipping...")
		if data:												# If there is updated info to send
			channel.basic_publish(exchange="services", routing_key='monitor', body=dataString)	# Send updated info
			print(data)
		
		time.sleep(1)	# Sleep of 1 minute

except KeyboardInterrupt:
	for service in services:
		if hasattr(service, 'doCleanup'):
			service.doCleanup()

# close the connection
msg_broker.close()