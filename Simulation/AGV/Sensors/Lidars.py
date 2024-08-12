class Lidars:
    def __init__(self) -> None:
        self._emergencyStop = False
        self._stop = False

    def Init(self):
        self._emergencyStop = False
        self._stop = False

    def DetermineFlags(self):
        #provide lidar logic, probably based on canva and close pixels
        pass

    def EmergencyStop(self):
        self._emergencyStop = True

    def Stop(self):
        self._stop = True

    def GetEmergencyStop(self):
        return self._emergencyStop

    def GetStop(self):
        return self._stop