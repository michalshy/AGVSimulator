# import Physics
import Reception
# import Simulation
import Transmission
import threading
from Transmission import Transmission
from Reception import Reception


# from Simulation import Simulation

class AppEngine:

    def __init__(self):
        self._reception = Reception.Reception()
        # self._transmission = Transmission.Transmission()
        # self._simulation = Simulation.AGVSim(0)

    def loopProgram(self):
        while True:
            threading.Thread(target=self._reception.startReception()).start()
            # threading.Thread(target=self._transmission.transmit).start()
