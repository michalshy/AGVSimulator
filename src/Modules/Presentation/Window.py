import pygame
from pygame.locals import *
from Modules.Presentation.Parameters import Parameters
from Globals import *
from Modules.Presentation.OpcClient import OpcClient
from Modules.Entities.AGV.AGV import AGV

class Window:
    def __init__(self, pm: Parameters) -> None:
        self._canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._backgroundColor = (0,0,0)
        self._roomImage = pygame.image.load(pm.GetRoomPath())
        self._rectRoom = self._roomImage.get_rect()
        self._startPos: tuple = self._DetermineRoomPosition()

    def PrepWindow(self):
        self._canvas.fill(self._backgroundColor)
        self._canvas.blit(self._roomImage, (self._startPos))

    def CheckEvents(self, opcClient: OpcClient) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                opcClient.CloseConnection()
                return False      
        return True
    
    def Draw(self, agv: AGV):
        agv.Draw(self._canvas)
        self._Update()

    def GetImage(self):
        return self._roomImage
    
    def GetCanvas(self):
        return self._canvas

    def _Update(self):
        pygame.display.update()
  
    def _DetermineRoomPosition(self) -> tuple:
        return ((SCREEN_WIDTH - self._roomImage.get_width())/2, (SCREEN_HEIGHT - self._roomImage.get_height())/2)