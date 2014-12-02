# Each service should be encapuslated in a class following the structure below.
# It doesnt matter how you implement the class, as long as it implements at least the 
# four functions below and matches their signatures and return types. My part of the 
# project will call these functions to get the priority and name of the service and 
# send it to the AMQP Server.


class TestService:
	'''A class for testing that implements minimum functionality required'''

	def __init__(self):
		self.name = "Test Service"	# Name of the service
		self.priority = 6			# Holds a priority level as an int 0-5
		self.updatePeriod = 1		# Update period in minutes, must be greater than zero
		self.updateCount = 1

		# Can read from a config file to get things like
		# zipcode, OAuth token, update period, etc...

		# Create a connection to the service

	def __str__(self):
		return "{0}: {1}".format(self.name, str(self.priority))

	# Returns the name of the service as a string
	def getName(self):
		return self.name

	# Returns a boolean indicating if a new notification should be checked for.
	# This function will be called once per minute, so a counter is used to make
	# it update once per 5 minutes for this test class. If true is returned, 
	# getPriority() is the next function to get called.
	def doUpdate(self):
		if(self.updateCount == self.updatePeriod):
			self.updateCount = 1
			#print("update")
			return True
		else:
			self.updateCount += 1
			return False

	# Retruns an int 0-5 indicating the priority
	def getPriority(self):
		# Call a function that queries the service for new data
		# set the priority based on the data
		#print(str(self))
		self.priority += 1;
		if(self.priority > 5):
			self.priority = 0
		return self.priority

	def doCleanUp(self):
		pass
