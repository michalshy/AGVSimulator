# Class to handle all global parameters
# This class is redundant by now, later will be filled by Reception class

# Big shoutout to my friend Jacob Zajunc


class Config:
    def __init__(self):
        self._host = "moj branch"

    def getHost(self):
        return self._host