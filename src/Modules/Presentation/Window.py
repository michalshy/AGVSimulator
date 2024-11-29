import pygame
from pygame.locals import *
from Modules.Presentation.Parameters import Parameters
from Globals import *
from Modules.Presentation.OpcClient import OpcClient
from Modules.Entities.AGV.AGV import AGV
# -*- coding: utf-8 -*-
"""Window module

Window is mostly wrapper around pygame functions, provided for eliminating
redundance over project 
"""
class Window:
    def __init__(self, pm: Parameters) -> None:
        self._canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._backgroundColor = (0,0,0)
        self._roomImage = pygame.image.load(pm.GetRoomPath())
        self._rectRoom = self._roomImage.get_rect()
        self._startPos: tuple = self._DetermineRoomPosition()
        self._infoColor = (64,64,64)
        self._borderColor = (255,255,255)
        self._font = pygame.font.Font('freesansbold.ttf', 20)
        self._infoRectBorder = pygame.Rect(INFO_WINDOW_POSX - INFO_BORDER/2, 
                                           INFO_WINDOW_POSY - INFO_BORDER/2, 
                                           INFO_WINDOW_SIZEX + INFO_BORDER, 
                                           INFO_WINDOW_SIZEY + INFO_BORDER)
        self._infoRect = pygame.Rect(INFO_WINDOW_POSX, INFO_WINDOW_POSY, INFO_WINDOW_SIZEX, INFO_WINDOW_SIZEY)

    def PrepWindow(self):
        self._canvas.fill(self._backgroundColor)
        self._canvas.blit(self._roomImage, (self._startPos))

    def CheckEvents(self, opcClient: OpcClient) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                opcClient.CloseConnection()
                return False      
        return True
    
    def DrawInformations(self, agv: AGV):
        TITLE = "AGV INFO:"
        heading = "Heading:" + str(round(agv.GetNNS().heading,2))
        corX = "X:" + str(round(agv.GetNNS().xCoor,2))
        corY = "Y:" + str(round(agv.GetNNS().yCoor,2))
        speed = "Speed:" + str(round(agv.GetNNS().speed / 100,2))
        battery = "Battery:" + str(agv.GetENC().batteryValue)
        pygame.draw.rect(self._canvas, self._borderColor, self._infoRectBorder)
        pygame.draw.rect(self._canvas, self._infoColor, self._infoRect)
        self._canvas.blit(self._font.render(TITLE, True, WHITE), 
                          (self._infoRect.x + INFO_PADDING, self._infoRect.centery - 50))
        self._canvas.blit(self._font.render(heading, True, WHITE), 
                          (self._infoRect.x + INFO_PADDING, self._infoRect.centery - 30))
        self._canvas.blit(self._font.render(corX, True, WHITE), 
                          (self._infoRect.x + INFO_PADDING, self._infoRect.centery - 10))
        self._canvas.blit(self._font.render(corY, True, WHITE), 
                          (self._infoRect.x + INFO_PADDING, self._infoRect.centery + 10))
        self._canvas.blit(self._font.render(speed, True, WHITE), 
                          (self._infoRect.x + INFO_PADDING, self._infoRect.centery + 30))
        self._canvas.blit(self._font.render(battery, True, WHITE), 
                          (self._infoRect.x + INFO_PADDING, self._infoRect.centery + 50))
    
    def Draw(self, agv: AGV):
        self.DrawInformations(agv)
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