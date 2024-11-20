# -*- coding: utf-8 -*-
"""Dec module

Deep learning class module, contains method which makes prediction of path possible.
Navigator module within AGV uses it to checks next points on route based on order.
"""
class Dec:
    def __init__(self) -> None:
        self._path = []
        self._heading = 0

    def PredictPath(self, segments_to_traverse: list): #TODO: PREDICT
        self._path = ((100,100), (200,200), (300,300), (400,400), (500,500), (600,600))
        self._heading = 90 

    def ReturnPredictedPath(self):
        return self._path
    
    def ReturnPredictedHeading(self):
        return self._heading