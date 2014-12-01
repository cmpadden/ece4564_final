ece4564_final
=============
The Raspberry Pi will run an application that will interface with the user’s Gmail account in order to notify the user via an LED system when they receive emails. The same LED system will be used to notify the user if there is any upcoming storms or inclimate weather. The weather information will be obtained from Weather Underground. The application will be modular and additional services will be able to be added using the same LED notification system.

The LED notification system will be made up of one red, one yellow, and one green LED. These will be lit in various combinations to indicate a priority level of a notification. The LEDs may be lit in any of the following combinations and are listed in order of priority from lowest to highest: off, red, red/yellow, yellow, yellow/green and green. Each service will have its own set of LEDs. Each service will also have a pushbutton that will allow the user to clear a notification at any point.


collaborators
=============

Name | Task
--- | ---
Joe Callen | Implement Gmail module to check if the user has a new email, and update LED system appropriately depending on number of emails or importance of emails.
Chris Cronin | Create a standard interface for services which will allow new services to be easily added to the system. Main module which calls the individual service functions.
Andrew Gardner | Implement module to get weather data and update LED system appropriately for inclimate weather.
Cole Padden | Implement a module to control LEDs based on input parameters of GPIO pin, blink duration, blink frequency, and LED color. Main module which subscribes to the AMQP Server and call the led control module functions.


Dependencies
============
Name | location
--- | ---
google-api-python-client | https://pypi.python.org/pypi/google-api-python-client/
gflags | apt-get python-gflags or pip install python-gflags
oauth2client | pip install oauth2client
wiringpi2 | https://pypi.python.org/pypi/wiringpi2/1.0.10
pika | https://pika.readthedocs.org/en/0.9.14/


