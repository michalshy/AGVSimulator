# Class to handle all global parameters

class Config:
    def __init__(self):
        self._host = "kto wie"

    def getHost(self):
        return self._host