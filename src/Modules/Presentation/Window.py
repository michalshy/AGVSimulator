import pygame
from pygame.locals import *
from Config import *
from Modules.Entities.AGV.AGV import AGV
from Modules.Presentation.Network.Network import Network
# -*- coding: utf-8 -*-
"""Window module

Window is mostly wrapper around pygame functions, provided for eliminating
redundance over project 
"""
class Window:
    def __init__(self) -> None:
        self._canvas = pygame.display.set_mode((config['screen']['screen_width'], 
                                                config['screen']['screen_height']))
        self._backgroundColor = (0,0,0)
        self._roomImage = pygame.image.load(config['room']['room_image'])
        self._rectRoom = self._roomImage.get_rect()
        self._startPos: tuple = self._DetermineRoomPosition()
        self._infoColor = (64,64,64)
        self._borderColor = (255,255,255)
        self._font = pygame.font.Font('freesansbold.ttf', 20)
        self._infoRectBorder = pygame.Rect(Additional.INFO_WINDOW_POSX - config['info_window']['info_border']/2, 
                                           Additional.INFO_WINDOW_POSY - config['info_window']['info_border']/2, 
                                           config['info_window']['info_window_sizex'] + config['info_window']['info_border'], 
                                           config['info_window']['info_window_sizey'] + config['info_window']['info_border'])
        self._infoRect = pygame.Rect(Additional.INFO_WINDOW_POSX, 
                                     Additional.INFO_WINDOW_POSY, 
                                     config['info_window']['info_window_sizex'], 
                                     config['info_window']['info_window_sizey'])

    def PrepWindow(self):
        self._canvas.fill(self._backgroundColor)
        self._canvas.blit(self._roomImage, (self._startPos))

    def CheckEvents(self, network: Network) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                network.CloseConns()
                return False      
        return True
    
    def DrawInformations(self, agv: AGV):
        TITLE = "AGV INFO:"
        heading = "Heading:" + str(round(agv.GetNNS().heading,6))
        corX = "X:" + str(round(agv.GetNNS().xCoor,2))
        corY = "Y:" + str(round(agv.GetNNS().yCoor,2))
        speed = "Speed:" + str(round(agv.GetNNS().speed / 100,2))
        battery = "Battery:" + str(agv.GetENC().batteryValue)
        pygame.draw.rect(self._canvas, self._borderColor, self._infoRectBorder)
        pygame.draw.rect(self._canvas, self._infoColor, self._infoRect)
        self._canvas.blit(self._font.render(TITLE, True, WHITE), 
                          (self._infoRect.x + config['info_window']['info_padding'], 
                           self._infoRect.centery - 50))
        self._canvas.blit(self._font.render(heading, True, WHITE), 
                          (self._infoRect.x + config['info_window']['info_padding'], 
                           self._infoRect.centery - 30))
        self._canvas.blit(self._font.render(corX, True, WHITE), 
                          (self._infoRect.x + config['info_window']['info_padding'], 
                           self._infoRect.centery - 10))
        self._canvas.blit(self._font.render(corY, True, WHITE), 
                          (self._infoRect.x + config['info_window']['info_padding'], 
                           self._infoRect.centery + 10))
        self._canvas.blit(self._font.render(speed, True, WHITE), 
                          (self._infoRect.x + config['info_window']['info_padding'], 
                           self._infoRect.centery + 30))
        self._canvas.blit(self._font.render(battery, True, WHITE), 
                          (self._infoRect.x + config['info_window']['info_padding'], 
                           self._infoRect.centery + 50))
    
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
        return ((config['screen']['screen_width'] - self._roomImage.get_width())/2, 
                (config['screen']['screen_height'] - self._roomImage.get_height())/2)