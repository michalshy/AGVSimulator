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
        self._orders = [[56.0, 52.0, 22.0, 26.0, 318.0, 322.0, 8.0, 4.0, 158.0, 162.0, 256.0, 252.0, 62.0, 66.0, 222.0, 226.0, 230.0, 234.0, 328.0, 324.0, 246.0, 250.0],[250.0, 248.0, 244.0, 326.0, 330.0, 286.0, 290.0, 334.0, 338.0, 238.0, 242.0, 240.0],[240.0, 236.0, 336.0, 332.0, 118.0, 122.0, 262.0, 266.0, 30.0, 34.0, 64.0, 60.0, 254.0, 258.0, 102.0, 106.0, 150.0, 154.0, 206.0, 210.0, 208.0],[208.0, 204.0, 302.0, 306.0, 190.0, 194.0, 184.0, 180.0, 166.0, 170.0, 174.0, 178.0, 176.0],[178.0, 176.0, 172.0, 168.0, 164.0, 24.0, 20.0, 54.0, 58.0, 56.0]]
        self._ordersIdx = 0
        self._lines = []
        self._timeWait = 0

    def CheckForOrders(self): 
        return self._orderReady

    def GetOrder(self):
        with open('tms.txt', 'r') as file:
            i = 0
            for line in file:
                numbers = line.strip().split(', ')
                if(i == self._ordersIdx):
                    self._lines = [float(num) for num in numbers]
                    break
                else:
                    i+=1
        with open('tms_time.txt', 'r') as file:
            i = 0
            for line in file:
                if(i == self._ordersIdx):
                    self._timeWait = int(line)
                    break
                else:
                    i+=1

        segments = self._lines
        self._ordersIdx +=1
        self._ordersIdx%=5
        self._orderReady = False
        return segments
    
    def GetTimeWait(self):
        return self._timeWait
    
    def Run(self):
        if timer.GetTicks() > (self._simulatedOrder + SIMULATED_ORDER_CYCLE) and self._notInvoked: 
            self._orderReady = True
            self._notInvoked = False
            self._simulatedOrder += SIMULATED_ORDER_CYCLE

    

