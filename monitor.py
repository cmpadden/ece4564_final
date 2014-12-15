#!/usr/bin/env python

import pika
import logging
import sys
import json
import time
import argparse
from test_service import TestService
from gmail import GmailService
from weather import WeatherService

logging.getLogger('pika').setLevel(logging.ERROR)

# Instantiate the services
s1 = TestService()
s2 = GmailService()
#s3 = WeatherService()
services = [s1, s2];

# Parse command line arguments
parser = argparse.ArgumentParser(description='Stat Cleint')
parser.add_argument('-b', metavar='broker-address', dest='ip', required=True)
parser.add_argument('-p', metavar='virtual-host', dest='virtualhost', default='/')
parser.add_argument('-c', metavar='username:password', dest='credentials', default='guest:guest')
cla = parser.parse_args()

try:
	#connect to message broker
	credentials = cla.credentials.split(':')
	msg_broker = pika.BlockingConnection(
	pika.ConnectionParameters(host=cla.ip,
							  virtual_host=cla.virtualhost,
							  credentials=pika.PlainCredentials(credentials[0],
							 								    credentials[1],
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
					data[service.getName()] = service.getPriority()	# Add the name and priority to the dict
					dataString = json.dumps(data)					# Dump the data to json
					if hasattr(service, 'comment'):
						service.comment()
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

except Exception, ee:
	print("Error: {0}".format(ee))

finally:
	# close the connection
	msg_broker.close()	

