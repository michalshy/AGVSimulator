from Modules.Entities.AGV.AGV import AGV
from Modules.Entities.Frame6100.NNC import NNC
from Modules.Simulation.Logic.Timer import *

SIMULATED_ORDER_CYCLE = 5000

class TMS:
    def __init__(self) -> None:
        self._triggeredOnce = False #temporary
        self._orderReady = False
        self._simulatedOrder = 0
        self._notInvoked = True

    def CheckForOrders(self): #TEMPORARY FUNCTION TO TRIGGER DRIVE
        return self._orderReady

    def GetOrder(self):
        segments = [56.0,20.0,48.0,52.0,16.0,44.0,12.0,36.0,4.0]
        self._orderReady = False
        return segments
    
    def Run(self):
        if timer.GetTicks() > (self._simulatedOrder + SIMULATED_ORDER_CYCLE) and self._notInvoked: #TEMPORARY
            self._orderReady = True
            self._notInvoked = False
            self._simulatedOrder += SIMULATED_ORDER_CYCLE

    

