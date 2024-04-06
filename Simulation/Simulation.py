import simpy
from Frame6000.NNS import NNS
from Frame6000.ENC import ENC
from Frame6000.SS import SS

from Frame6100.MC import MC
from Frame6100.NNC import NNC

class AGVSim(object):
    def __init__(self, env):
        self.env = env

        # Start the run process everytime an instance is created.
        #self.action = env.process(self.run())


    nns = NNS()
    enc = ENC()
    nns = NNS()
    ss = SS()
    mc = MC()
    nnc = NNC()

