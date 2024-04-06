import simpy
from Frame6000 import ENC, NNS, SS
from Frame6100 import MC, NNC
class AGVSim(object):
    def __init__(self, env):
        self.env = env

        # Start the run process everytime an instance is created.
        #self.action = env.process(self.run())

    enc = ENC()
    nns = NNS()
    ss = SS()
    mc = MC()
    nnc = NNC()
