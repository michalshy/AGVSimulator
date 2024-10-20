class Wheels:
    def __init__(self) -> None:
        self._maxSpeed = 0 
        self._atMaxSpeed = False

        # flags
        self._driveMode = False

    def Init(self):
        self._maxSpeed = 50 #TODO: figure out when agv can move faster to 150

    def DetermineFlags(self, speed):
        # Max speed
        if speed >= self._maxSpeed:
            self._atMaxSpeed = True
        else:
            self._atMaxSpeed = False

    def SetDriveMode(self, state: bool):
        self._driveMode = state

    def GetAtMaxSpeed(self):
        return self._atMaxSpeed
    
    def GetDriveMode(self):
        return self._driveMode