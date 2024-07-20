import Physics
import simpy
import Simulation
from Simulation import Simulation
from OpcHandler.OpcHandler import OpcHandler
from Simulation.ParamManager import ParamManager
from Simulation.AGV.AGV import AGV
from Physics.Physics import Physics

# AppEngine - class used to control whole flow, declare variables that are unique
class AppEngine:

    def __init__(self):
        # Declare simpy environment as real-time and it's factor as 100ms
        self.env = simpy.rt.RealtimeEnvironment(factor=1, strict=False)
        self._agv = AGV()
        self._phyEng = Physics(self._agv)
        self._paramManager = ParamManager()
        self._opcHandler = OpcHandler(self._paramManager, self._agv)
        self._simulation = Simulation.AGVSim(self.env, self._phyEng, self._agv, self._opcHandler)

    def LoopProgram(self):
        # Start simulation
        self._simulation.Run()
        # End simulation
