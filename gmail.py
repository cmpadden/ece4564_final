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
        return self.name

    def doUpdate(self):
        if self.updateCount == self.updatePeriod:
            self.updateCount = 0
            return True
        else:
            self.updateCount += 1
            return False

    def getPriority(self):
        print(str(self))
        return self.priority

    def getMessageCount(self):
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


def main():
    """
    Main method for testing
    """
    return 0


if __name__ == '__main__':
    main()
