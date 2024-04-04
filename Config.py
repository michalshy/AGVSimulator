# Class to handle all global parameters

class Config:
    def __init__(self):
        self._host = "moj branch"

    def getHost(self):
        return self._host