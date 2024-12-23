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
        segments = [240.0,236.0,336.0,332.0,118.0,122.0,262.0,266.0,30.0,34.0,64.0,60.0,254.0,258.0,102.0,106.0,150.0,154.0,206.0,210.0,208.0,204.0]
        self._orderReady = False
        return segments
    
    def Run(self):
        if timer.GetTicks() > (self._simulatedOrder + SIMULATED_ORDER_CYCLE) and self._notInvoked: #TEMPORARY
            self._orderReady = True
            self._notInvoked = False
            self._simulatedOrder += SIMULATED_ORDER_CYCLE

    

