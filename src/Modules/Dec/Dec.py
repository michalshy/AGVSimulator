from NeuralNetwork.AIManager import AI_Manager
from NeuralNetwork.DataManager import DataManager

# -*- coding: utf-8 -*-
"""Dec module

Deep learning class module, contains method which makes prediction of path possible.
Navigator module within AGV uses it to checks next points on route based on order.
"""

def AiApiGetRoute(initial_data ,segments_to_traverse):
    return AI_Manager(20).predict_route(initial_data,segments_to_traverse)

class Dec:
    def __init__(self) -> None:
        self._path = []

    def PredictPath(self,initial_data ,segments_to_traverse):
        dataManager = DataManager('Config/agv.pkl')
        df = dataManager._fullData[233:254]
        self._path = AiApiGetRoute(df ,segments_to_traverse)

    def ReturnPredictedPath(self):
        return self._path
    