#!/usr/bin/env python

import pika
import sys
import json
import time
from test_service import TestService

# Instantiate the services
s1 = TestService()
services = [s1];

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

	for service in services:
		data = {}
		if service.doUpdate():								# If the service should be updated
			data[service.getName()] = service.getPriority()	# Add the name and priority to the dict
			dataString = json.dumps(data)					# Dump the data to json
	
	if(len(services) > 0):									# If there is updated info to send
		channel.basic_publish(exchange="services", routing_key='monitor', body=dataString)	# Send updated info
	
	time.sleep(1)	# Sleep of 1 minute

# close the connection
msg_broker.close()