#!/usr/bin/env python
"""
Gmail Service client

Parts of the gmail service class created based on the example in the Gmail API sample code located
at https://developers.google.com/gmail/api/quickstart/quickstart-python

"""
import httplib2
import os
import time

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run


class GmailService:
    def __init__(self):
        self.name = 'Gmail Service'
        self.priority = 0
        self.updatePeriod = 5
        # Asks for Authorization immediately
        self.updateCount = 5

        # The file exists, but not pushed to git.
        if os.path.isfile('client_secret.json'):
            self.CLIENT_SECRET_FILE = 'client_secret.json'
        elif os.path.isfile('../client_secret.json'):
            self.CLIENT_SECRET_FILE = '../client_secret.json'
        else:
            raise GmailException('Error Gmail Client Secret Not found.  Service will not work')

        # Allows readonly access
        self.OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

        # Location of Credentials storage
        self.STORAGE = Storage('gmail.storage')

        #OAuth flow to retrieve credentials
        self.flow = flow_from_clientsecrets(self.CLIENT_SECRET_FILE, scope=self.OAUTH_SCOPE)

    def __str__(self):
        return "{0}: {1}".format(self.name, str(self.priority))

    def getName(self):
        """
        Returns the service name
        :return: Service name
        """
        return self.name

    def doUpdate(self):
        """
        If the number of times this is called is the update period, updates the message count
        otherwise, updates counter
        :return:  True if update executed, otherwise false
        """
        if self.updateCount == self.updatePeriod:
            self.updateCount = 0
            return True
        else:
            self.updateCount += 1
            return False

    def getPriority(self):
        """
        Updates and gets the current priority
        :return: The services priority
        """
        # Get new message count and update priority
        self.getMessageCount()
        print(str(self))
        return self.priority

    def getMessageCount(self):
        """
        Makes the request to the Gmail API for the number of unread messages within the past day
        Initial usage requires the user to go to a website and authorize the application
        Calls updatePriority with the new message count
        :return: None
        """
        messageCount = 0

        http = httplib2.Http()

        try:
            credentials = self.STORAGE.get()
            if credentials is None or credentials.invalid:
                credentials = run(self.flow, self.STORAGE, http=http)
        except:
            self.doCleanUp()
            raise GmailException('Error:  Authentication request was rejected')

        # Authorize httplib2.Http object with credentials
        http = credentials.authorize(http)

        # Build the gmail service from discovery
        gmail_service = build('gmail', 'v1', http=http)

        # Retrieve all new unread messages within the past day
        try:
            messages = gmail_service.users().messages().list(
                userId='me',
                q='is:unread AND newer_than:7d').execute()
        except:
            self.doCleanUp()
            raise GmailException('Error: Something went wrong while making the gmail request')

        try:
            if messages['messages']:
                messageCount = len(messages['messages'])
        # if messages['message'] doesn't exist, then there are no new unread messages
        except KeyError:
            messageCount = 0

        self.updatePriority(messageCount)

    def updatePriority(self, count):
        """
        Updates the priority based on the number of messages

        Priority Levels:
            0 - No Messages
            1 - 1-5 messages
            2 - 6-20 messages
            3 - 21-50 messages
            4 - 51-75 messages
            5 - 76+ messages

        :arg count:  the number of unread messages
        :return: None
        :updates:  self.priority
        """
        if count > 75:
            self.priority = 5
        elif 50 < count <= 75:
            self.priority = 4
        elif 20 < count <= 50:
            self.priority = 3
        elif 5 < count <= 20:
            self.priority = 2
        elif 1 < count <= 5:
            self.priority = 1
        else:
            self.priority = 0

    def doCleanUp(self):
        if os.path.isfile('gmail.storage'):
            os.remove('gmail.storage')


class GmailException(Exception):
    pass


def main():
    """
    Main method for testing
    Polls gmail class every 60 seconds.  With current settings, every 5 minutes the class
    will update and print out the new value
    """
    gmail = GmailService()
    try:
        while True:
            if gmail.doUpdate():
                gmail.getPriority()
            else:
                time.sleep(60)
    except KeyboardInterrupt:
        pass

    return 0


if __name__ == '__main__':
    main()
