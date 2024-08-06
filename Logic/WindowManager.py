from pygame import *
import pygame
from Simulation.ParamManager import ParamManager
from Globals import *

class WindowManager:
    def __init__(self, canvas: Surface, pm: ParamManager) -> None:
        self._canvas = canvas
        self._pm = pm
        self._backgroundColor = (0,0,0)
        self._roomImage = pygame.image.load(self._pm.GetRoomPath())
        self._rectRoom = self._roomImage.get_rect()
        self._startPos: tuple = self.DetermineRoomPosition()

    def PrepWindow(self):
        self._canvas.fill(self._backgroundColor)
        self._canvas.blit(self._roomImage, (self._startPos))

    def DetermineRoomPosition(self) -> tuple:
        return ((SCREEN_WIDTH - self._roomImage.get_width())/2, (SCREEN_HEIGHT - self._roomImage.get_height())/2)