import AppEngine
import Reception
from Simulation.ParamManager import ParamManager

# Main of the whole AGV Simulator, calls loop declared deeper into Simulation
def __main__():
    app = AppEngine.AppEngine()
    app.LoopProgram()


__main__()
