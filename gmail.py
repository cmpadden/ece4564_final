#!/usr/bin/env pytho
"""
Gmail Service client
"""
import google


class gmailService:
    def __init__(self):
        self.name = 'Gmail Service'
        self.priority = 0
        self.updatePeriod = 5
        self.updateCount = 0

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


def main():
    """
    Main method for testing
    """
    return 0


if __name__ == '__main__':
    main()
