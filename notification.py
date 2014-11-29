"""
Takes input parameters and controls LEDs connected to the
general purpose input-output pins accordingly using the
WiringPi2 library as seen in the following URL:

http://raspi.tv/2013/how-to-use-wiringpi2-for-python-on-the-raspberry-pi-in-raspbian

|-------------------------------------------------------|
|     Raspberry Pi GPIO Connector Numbering Schemes     |
|--------------|-------|---------|-------|--------------|
| WiringPi Pin | Name  | Header  | Name  | WiringPi Pin |
|--------------|-------|----|----|-------|--------------|
| -            | 3.3v  | 1  | 2  | 5v    | -            |
| 8: green     | SIJA  | 3  | 4  | 5v    | -            |
| 9: yellow    | SCL   | 5  | 6  | Ov    | -            |
| 7: red       | GPIO7 | 7  | 8  | TxO   | 15           |
| -            | Ov    | 9  | 10 | RxO   | 16           |
| 0: green     | GPIOO | 11 | 12 | GPIO1 | 1            |
| 2: yellow    | GP102 | 13 | 14 | Ov    | -            |
| 3: red       | GPIO3 | 15 | 16 | GPI04 | 4            |
| -            | 3.3v  | 17 | 18 | GPIO5 | -            |
| 12           | MOSI  | 19 | 20 | Ov    | -            |
| 13           | MISO  | 21 | 22 | GPIO6 | 6            |
| 14           | SCLK  | 23 | 24 | CEO   | 10           |
| -            | Ov    | 25 | 26 | CE1   | 11           |
|--------------|-------|---------|-------|--------------|
| WiringPi Pin | Name  | Header  | Name  | WiringPi Pin |
|--------------|-------|---------|-------|--------------|


|------------------------------------------------|
| Priorities                                     |
|-------------|---------|------------|-----------|
| Level (0-5) | Red LED | Yellow LED | Green LED |
|-------------|---------|------------|-----------|
| 0           | off     | off        | off       |
| 1           | off     | off        | on        |
| 2           | off     | on         | on        |
| 3           | off     | on         | off       |
| 4           | on      | on         | off       |
| 5           | on      | off        | off       |
|-------------|---------|------------|-----------|

"""

#import wiringpi2 as wiringpi
from time import sleep

class Notification:


    def __init__ (self):

        # tuple of lists containing groups of pins and their associated service
        self.pinGroups = ["unused", 8, 9, 7],\
                         ["unused", 0, 2, 3],\
                         ["unused", 12, 13, 14],\
                         ["unused", 15, 16, 1],\
                         ["unused", 6, 10, 11]


    def addService(self, name):
        """ Maps the service to a group of pins if it is not yet taken
        :param name:    name of the service
        :return:
        """

        # locate the first unused group of pins, and assign that to the service
        for group in self.pinGroups:
            if group[0] == "unused":
                # assign service name to that group of pins
                group[0] = str(name)
                # break to prevent assigning service to multiple groups
                break

    def removeServer(self, name):
        """ Removes the service and replaces it with an unused token
        """

        # locate the service in the tuple
        for groups in self.pinGroups:
            if group[0] == str(name):
                # replace the service name with unused
                group[0] = "unused"
                break


    def blink(self, name, priority ):
        """ Performs desired notification operation based on input
        :param name:           name of the service
        :param priority:       priority level between 0 and 5
        :return:
        """

        # set wiring pi to use pins
        # wiringpi.wiringPiSetup()

        # temporary list of pins from service
        servicePins = []
        for group in self.pinGroups:
            if group[0] == str(name):
                servicePins = group[1:4]

        # index 0 will be GREEN, 1 will be YELLOW, 2 will be RED
        # enable the three pins for output for that service and set to off 0V
        print "Enabling pin: " + str(servicePins[0])
        # wiringpi.pinMode(servicePins[0], 1)
        # wiringpi.digitalWrite(servicePins[0], 0)
        print "Enabling pin: " + str(servicePins[1])
        # wiringpi.pinMode(servicePins[1], 1)
        # wiringpi.digitalWrite(servicePins[1], 0)
        print "Enabling pin: " + str(servicePins[2])
        # wiringpi.pinMode(servicePins[2], 1)
        # wiringpi.digitalWrite(servicePins[2], 0)


        # loops 20 times, so that will be 1 minute of blinking with 1s on, 2s off
        for i in xrange(20):

            # turn on LEDs 3.3V
            # index 0, green is enabled for priority levels 1 and 2
            if (int(priority) == 1) or (int(priority) == 2):
                # wiringpi.digitalWrite(servicePins[0], 1)
                print "on green at " + str(servicePins[0])

            # index 1, yellow is enabled for priority levels 2, 3, and 4
            if (int(priority) == 2) or (int(priority) == 3) or (int(priority) == 4):
                # wiringpi.digitalWrite(servicePins[1], 1)
                print "on yellow at " + str(servicePins[1])

            # index 2, red is enabled for priority levels 4 and 5
            if (int(priority) == 4) or (int(priority) == 5):
                # wiringpi.digitalWrite(servicePins[2], 1)
                print "on red at " + str(servicePins[2])

            # wait a second before disabling LEDs before next blink
            sleep(1)

            # turn off lEDs and wait another second
            print "off"
            # wiringpi.digitalWrite(servicePins[0], 0)
            # wiringpi.digitalWrite(servicePins[1], 0)
            # wiringpi.digitalWrite(servicePins[2], 0)

            #  wait one more second of being off
            sleep(2)

        # clean up the pins by making sure they are off and setting them back to inputs
        # wiringpi.digitalWrite(servicePins[0], 0)
        # wiringpi.digitalWrite(servicePins[1], 0)
        # wiringpi.digitalWrite(servicePins[2], 0)
        # wiringpi.pinMode(servicePins[0], 1)
        # wiringpi.pinMode(servicePins[1], 1)
        # wiringpi.pinMode(servicePins[2], 1)




# TESTING THE CLASS

myNotification = Notification()
print myNotification.pinGroups

# add a service and print to check
myNotification.addService("testService")
print myNotification.pinGroups

# add another service and print to check
myNotification.addService("secondService")
print myNotification.pinGroups

# attempt to blink LEDs
print "\n attempting to blink leds \n "
myNotification.blink("secondService", 4)

