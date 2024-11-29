from NeuralNetwork.AIManager import AI_Manager
import pandas as pd

# -*- coding: utf-8 -*-
"""Dec module

Deep learning class module, contains method which makes prediction of path possible.
Navigator module within AGV uses it to checks next points on route based on order.
"""

def AiApiGetRoute(initial_data, segments_to_traverse):
    return AI_Manager(20).predict_route(initial_data, segments_to_traverse)

class Dec:
    def __init__(self) -> None:
        self._path = []

    def PredictPath(self, initial_data, segments_to_traverse):
        self._path = AiApiGetRoute(initial_data, segments_to_traverse)
        if(len(self._path) != 0):
            return True
        return False

    def ReturnPredictedPath(self):
        return self._path
    