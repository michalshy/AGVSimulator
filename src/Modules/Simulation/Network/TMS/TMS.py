from Modules.Entities.AGV.AGV import AGV
from Modules.Entities.Frame6100.NNC import NNC
from Modules.Simulation.Logic.Timer import *

SIMULATED_ORDER_CYCLE = 5000

class TMS:
    def __init__(self) -> None:
        self._triggeredOnce = False #temporary
        self._orderReady = False
        self._simulatedOrder = 0
        self._eot = False

    def CheckForOrders(self): #TEMPORARY FUNCTION TO TRIGGER DRIVE
        return self._orderReady

    def GetOrder(self):
        segments = (0,1,2,3,4,5,6)
        self._orderReady = False
        return segments
    
    def Run(self):
        while not self._eot:
            if timer.GetTicks() > (self._simulatedOrder + SIMULATED_ORDER_CYCLE):
                self._orderReady = True
                self._simulatedOrder += SIMULATED_ORDER_CYCLE

    def EndTransmission(self):
        self._eot = True
    

