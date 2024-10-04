from datetime import datetime
from Simulation.AGV.AGV import AGV

INIT_CYCLES = 32

class LogManager:
    def __init__(self) -> None:
        self._nameOfFile = datetime.now().strftime("./Logs/%d%m%Y%H%M%S") + ".txt"
        f = open(self._nameOfFile, "w")
        f.close()
        self._infoToWrite = ""
        self._cycle = INIT_CYCLES

    def ConstructLine(self, agv: AGV):
        self._infoToWrite = str(agv.GetNNS().heading) + ":" + str(agv.GetNNS().speed) + ":" + str(agv.GetNNS().xCoor) + ":" \
                            + str(agv.GetNNS().yCoor) + ":" + str(agv.GetENC().batteryValue) + ":" + str(agv.GetNNS().goingToID) + ":" + str(agv.GetDriveMode()) + "\n"

    def WriteToFile(self, agv: AGV):
        self._cycle -= 1
        if self._cycle == 0:
            self.ConstructLine(agv)
            f = open(self._nameOfFile, "a")
            f.write(self._infoToWrite)
            f.close()
            self._cycle = INIT_CYCLES