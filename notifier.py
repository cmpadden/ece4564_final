"""
Subscribes to server to monitor for notifications
"""

import pika
import json
from notification import Notification

# global class instantiation 
myNotification = Notification()

# Chat message callback
def on_new_msg(channel, method, properties, msg_body):

    # convert the message into a JSON object
    message = json.loads(msg_body)

    # iterate over the dictionary
    for item in message:
        
        # check if the service has been added already
        if myNotification.checkServiceAdded(str(item)):
            pass
        # otherwise add the service to the class and turn on LEDs
        else:
            myNotification.addService(str(item))

        # turn on the LEDs for that service and priority
        myNotification.leds_on(str(item), str(message[item]))

        # if the priority is zero, turn off the LEDs, otherwise turn on based on priority
        print
        print "SERVICE NAME: " + str(item)
        print "PRIORITY: " + str(message[item])
        print


print "Notifer: Connected to message broker"

#################################
# connect to the message broker #
#################################

messageBroker = pika.BlockingConnection(
    pika.ConnectionParameters(host="netapps.ece.vt.edu",
                              virtual_host="sandbox",
                              credentials=pika.PlainCredentials("ECE4564-Fall2014",
                                                                "13ac0N!",
                                                                True)))

##################################
# setup the channel and exchange #
##################################

channel = messageBroker.channel()
channel.exchange_declare(exchange="services",
                         type="direct")

myQueue = channel.queue_declare(exclusive=True)

# Bind your queue to the message exchange, and register your
# new message event handler
channel.queue_bind(exchange="services",
                   queue=myQueue.method.queue,
                   routing_key="monitor")

# Start Pika's event loop
# Setup the callback for when a subscribed message is received
channel.basic_consume(on_new_msg,
                      queue=myQueue.method.queue,
                      no_ack=True)

# Start a blocking consume operation
channel.start_consuming()
