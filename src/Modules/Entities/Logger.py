from datetime import datetime
from Modules.Entities.AGV.AGV import AGV
from Modules.Simulation.Logic.Timer import *

INIT_CYCLE = 1000

class Logger:
    def __init__(self) -> None:
        self._nameOfFile = datetime.now().strftime("./Logs/%d%m%Y%H%M%S") + ".txt"
        f = open(self._nameOfFile, "w")
        f.close()
        self._infoToWrite = ""
        self._cycle = INIT_CYCLE

    def ConstructLine(self, agv: AGV):
        self._infoToWrite = str(agv.GetNNS().heading) + ":" + str(agv.GetNNS().speed) + ":" + str(agv.GetNNS().xCoor) + ":" \
                            + str(agv.GetNNS().yCoor) + ":" + str(agv.GetENC().batteryValue) + ":" + str(agv.GetNNS().goingToID) + ":" + str(agv.GetDriveMode()) + "\n"

    def WriteToFile(self, agv: AGV):
        if timer.GetTicks() > (self._cycle + INIT_CYCLE):
            self.ConstructLine(agv)
            f = open(self._nameOfFile, "a")
            f.write(self._infoToWrite)
            f.close()
            self._cycle = timer.GetTicks()