#!/usr/bin/env pytho
"""
Gmail Service client
"""
import httplib2

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run


class GmailService:
    def __init__(self):
        self.name = 'Gmail Service'

        # Priority Levels:
        #   0 - No Messages
        #   1 - 1-5 messages
        #   2 - 6-20 messages
        #   3 - 21-50 messages
        #   4 - 51-99 messages
        #   5 - 100+ messages
        self.priority = 0
        self.updatePeriod = 5
        self.updateCount = 0

        # The actual location of the file.  Removed for commits
        self.CLIENT_SECRET_FILE = 'CLENT_SECRET_FILE.json'
        self.OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
        self.STORAGE = Storage('gmail.storage')
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
            messages = self.getMessageCount()
            self.updatePriority(messages)
            return True
        else:
            self.updateCount += 1
            return False

    def getPriority(self):
        """
        Gets the current priority
        :return: The services priority
        """
        print(str(self))
        return self.priority

    def getMessageCount(self):
        """
        Makes the request to the Gmail API for the number of unread messages within the past day
        Initial usage requires the user to go to a website and authorize the application
        :return: Number of unread messages in the past day
        """
        messageCount = 0

        http = httplib2.Http()

        credentials = self.STORAGE.get()
        if credentials is None or credentials.invalid:
            credentials = run(self.flow, self.STORAGE, http=http)

        http = credentials.authorize(http)

        gmail_service = build('gmail', 'v1', http=http)

        messages = gmail_service.users().messages().list(userId='me',
                                                         q='is:unread AND newer:1d').execute()

        more = True
        while more:
            try:
                if messages['message']:
                    messageCount += len(messages['message'])
            except KeyError:
                pass
            try:
                if messages['nextPageToken']:
                    messages = gmail_service.users().messages().list(
                        userId='me',
                        q='is:unread AND newer_than:1d',
                        pageToken=messages[
                            'nextPageToken']).execute()
                else:
                    more = False
            except KeyError:
                more = False
        return messageCount

    def updatePriority(self, count):
        """
        Updates the priority based on the number of messages
        :arg count:  the number of unread messages
        :return: None
        :updates:  self.priority
        """
        if count >= 100:
            self.priority = 5
        elif 50 < count < 100:
            self.priority = 4
        elif 20 < count <= 50:
            self.priority = 3
        elif 5 < count <= 20:
            self.priority = 2
        elif 1 < count <= 5:
            self.priority = 1
        else:
            self.priority = 0


def main():
    """
    Main method for testing
    """
    return 0


if __name__ == '__main__':
    main()
