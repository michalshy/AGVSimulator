from Modules.Entities.AGV.AGV import AGV
from Modules.Entities.Frame6100.NNC import NNC

class TMS:
    def __init__(self) -> None:
        self._triggeredOnce = False #temporary

    def CheckForOrders(self, agv: AGV): #TEMPORARY FUNCTION TO TRIGGER DRIVE
        segments = (0,1,2,3,4,5,6)
        if not self._triggeredOnce:
            agv.SetOrder(True, segments)
            self._triggeredOnce = True
