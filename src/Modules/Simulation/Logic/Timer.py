import pygame
from pygame import *
# -*- coding: utf-8 -*-
"""Timer module

Global Timer module provided for updating of main loop with delta time
(for simulator to work properly on different platforms), and updating of
transmission, reception and logging cycles accordingly to variables set in Globals
"""
class Timer:
    def __init__(self) -> None:
        self._fps = 60
        self._timer = pygame.time.Clock()
        self._dt = 0.0

    def StartTimer(self):
        self._timer.tick(self._fps)

    def UpdateDelta(self):
        self._dt = (self._timer.tick(self._fps)/1000.0)

    def GetDt(self):
        return self._dt
    
    def GetTicks(self):
        return pygame.time.get_ticks()
    
timer = Timer()
timer.StartTimer()