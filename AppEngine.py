# import Physics
import Reception
# import Simulation
import Transmission
import threading
from Transmission import Transmission
from Reception import Reception
from Simulation import Simulation
from Simulation.ParamManager import ParamManager


# from Simulation import Simulation

class AppEngine:

    def __init__(self):
        self._paramManager = ParamManager()
        self._reception = Reception.Reception(self._paramManager)
        self._transmission = Transmission.Transmission()
        self._simulation = Simulation.AGVSim(0)

    def loopProgram(self):
        self._reception.startReceptionLocal()
        while True:
            # threading.Thread(target=self._reception.startReception()).start()
            # threading.Thread(target=self._transmission.transmit).start()
            self._simulation.Simulate()
