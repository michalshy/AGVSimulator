class Battery:
    def __init__(self) -> None:
        self._batteryAvailable = False
        self._boundryBattery = 0

    def Init(self, val):
        self._batteryAvailable = True
        self._boundryBattery = val * 0.3

    def DetermineFlags(self, val):
        # Battery
        if val > self._boundryBattery:
            self._batteryAvailable = True
        else:
            self._batteryAvailable = False

    def GetBatterAvailable(self):
        return self._batteryAvailable