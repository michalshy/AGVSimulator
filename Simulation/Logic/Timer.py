import pygame
from pygame import *

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