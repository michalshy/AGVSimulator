# import Physics
import os, time

import Reception
# import Simulation
import Transmission
import threading
from Transmission import Transmission
from Reception import Reception
from Simulation import Simulation
from Simulation.ParamManager import ParamManager
from Simulation.AGV.AGV import AGV
from Physics.Physics import Physics


# from Simulation import Simulation

class AppEngine:

    def __init__(self):
        self._phyEng = Physics()
        self._paramManager = ParamManager()
        self._reception = Reception.Reception(self._paramManager)
        self._transmission = Transmission.Transmission()
        self._simulation = Simulation.AGVSim(0, self._phyEng)
        self._agv = AGV()

    def loopProgram(self):
        # threading.Thread(target=self._reception.startReception()).start()
        # threading.Thread(target=self._transmission.transmit).start()
        self._reception.startReceptionLocal()
        self._simulation.Simulate(self._agv)
