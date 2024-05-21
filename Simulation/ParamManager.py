from Simulation.Frame6100.NNC import NNC
from Simulation.Frame6100.MC import MC



class ParamManager:
    def __init__(self):
        self.mc = MC()
        self.nnc = NNC()

    def fabricateFrames(self):
        self.nnc.goDestTrig = 0
        self.nnc.destID = 0

        self.mc.enable = 0
        self.mc.rotLeft = 0
        self.mc.rotRight = 0
        self.mc.turnLeft = 0
        self.mc.turnRight = 0
        self.mc.moveBack = 0
        self.mc.moveForw = 0
        self.mc.velocity = 0

    def setENC(self):
        pass

    def setNNS(self):
        pass

    def setSS(self):
        pass
