import Physics
import os, time
import simpy
import Reception
import Simulation
import Transmission
import threading
from Transmission import Transmission
from Reception import Reception
from Simulation import Simulation
from Simulation.ParamManager import ParamManager
from Simulation.AGV.AGV import AGV
from Physics.Physics import Physics


# AppEngine - class used to control whole flow, declare variables that are unique
class AppEngine:

    def __init__(self):
        # Declare simpy environment as real-time and it's factor as 100ms
        self.env = simpy.rt.RealtimeEnvironment(factor=1)
        self._agv = AGV()
        self._phyEng = Physics(self._agv)
        self._paramManager = ParamManager()
        self._reception = Reception.Reception(self._paramManager)
        self._transmission = Transmission.Transmission()
        self._simulation = Simulation.AGVSim(self.env, self._phyEng, self._agv)

    def LoopProgram(self):
        # threading.Thread(target=self._reception.startReception()).start()
        # threading.Thread(target=self._transmission.transmit).start()
        self._reception.StartReceptionLocal()
        # Start simulation
        self._simulation.Run()
        self.env.run()
        # End simulation
