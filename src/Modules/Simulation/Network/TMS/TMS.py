from Modules.Entities.AGV.AGV import AGV
from Modules.Entities.Frame6100.NNC import NNC

class TMS:
    def __init__(self) -> None:
        pass

    def CheckForOrders(self, agv: AGV): #TEMPORARY FUNCTION TO TRIGGER DRIVE
        if True: #recept new order
            agv.SetOrder(True)
        else:
            agv.SetOrder(False)       
