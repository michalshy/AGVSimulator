from pygame import *
import pygame
from Simulation.Managers.ParamManager import ParamManager
from Globals import *
from OpcHandler.OpcHandler import OpcHandler
from Simulation.AGV.AGV import AGV

class WindowManager:
    def __init__(self, canvas: Surface, pm: ParamManager, agv: AGV) -> None:
        self._canvas = canvas
        self._pm = pm
        self._agv = agv
        self._backgroundColor = (0,0,0)
        self._roomImage = pygame.image.load(self._pm.GetRoomPath())
        self._rectRoom = self._roomImage.get_rect()
        self._startPos: tuple = self.DetermineRoomPosition()

    def PrepWindow(self):
        self._canvas.fill(self._backgroundColor)
        self._canvas.blit(self._roomImage, (self._startPos))

    def CheckEvents(self, opcHandler: OpcHandler) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                opcHandler.CloseConnection()
                return False      
        return True
    
    def Draw(self):
        self._agv.Draw()

    def Update(self):
        pygame.display.update()

    def DetermineRoomPosition(self) -> tuple:
        return ((SCREEN_WIDTH - self._roomImage.get_width())/2, (SCREEN_HEIGHT - self._roomImage.get_height())/2)
    
    def GetImage(self):
        return self._roomImage