from Simulation.Frames.Frame6000.ENC import ENC
from Simulation.Frames.Frame6000.SS import SS
from Simulation.Frames.Frame6000.NNS import NNS
from Simulation.Frames.Frame6100.NNC import NNC
from Simulation.AGV.Sensors.Lidars import Lidars
from Simulation.AGV.Sensors.Wheels import Wheels
from Simulation.AGV.Sensors.Navigators.Navigator import Navigator
from Simulation.AGV.Sensors.Navigators.NavigatorML import NavigatorML, ENGINE, ENGINES
from Simulation.AGV.Sensors.Navigators.NavigatorA import NavigatorA
from Simulation.AGV.Sensors.Battery import Battery
from Simulation.Logic.Timer import *
import pygame
import math
from Globals import *

# Class that holds state of AGV
class AGV:
    def __init__(self, canvas):
        #pygame
        self._canvas = canvas

        # For frames
        self._enc = ENC()
        self._ss = SS()
        self._nns = NNS()
        
        # base params
        self._boundryBattery = 0

        #sensors
        self._battery = Battery()
        self._navi: Navigator
        if NAV_TYPE == 1:
            self._navi = NavigatorA()
        if NAV_TYPE == 0:
            self._navi = NavigatorML()
        self._wheels = Wheels()
        self._lidars = Lidars()

        #flags
        self._stopFlag = False

    def Init(self, img: pygame.Surface):
        self._enc.batteryValue = 120000
        self._nns.heading = self._navi.GetHeading()

        #TODO: ADD PROPER HANDLER FOR START POSITION
        self._nns.xCoor = STARTING_POS_X * 10
        self._nns.yCoor = STARTING_POS_Y * 10

        self._battery.Init(self._enc.batteryValue)
        self._navi.Init(img)
        self._wheels.Init()
        self._lidars.Init()

    def SetRouteParams(self, nnc: NNC):
        self.SetDestId(nnc)
        self.SetDestTrig(nnc)

    def SetDestId(self, nnc: NNC):
        self._nns.goingToID = nnc.destID

    def SetDestTrig(self, nnc: NNC):
        self._wheels.SetDriveMode(nnc.goDestTrig)

    def DetermineFlags(self):
        self._battery.DetermineFlags(self._enc.batteryValue)
        self._navi.DetermineFlags()
        self._wheels.DetermineFlags(self._nns.speed)
        self._lidars.DetermineFlags()

        self._stopFlag = self._navi.GetStop()


    def GetENC(self):
        return self._enc

    def GetSS(self):
        return self._ss

    def GetNNS(self):
        return self._nns

    def GetBatteryAvailable(self):
        return self._battery.GetBatterAvailable()

    def GetAtMaxSpeed(self):
        return self._wheels.GetAtMaxSpeed()

    def GetDriveMode(self):
        return self._wheels.GetDriveMode()
    
    def GetStopFlag(self):
        return self._stopFlag

    def PrintState(self):
        print("Heading: " + str(round(self._nns.heading,2)) + "degree")
        print("Speed: " + str(round(self._nns.speed / 100,2)) + "m/s")
        
        if self._navi.GetPath() is not None and ENGINE == ENGINES.OLEK:
            for i in self._navi.GetPath():
                print("X position: " + str(round(self._nns.xCoor, 10)) + "cm")
                print("X position predict: " + str(round(i[0], 10)) + "cm")
                print("Y position: " + str(round(self._nns.yCoor, 10)) + "cm")
                print("Y position predict: " + str(round(i[1], 10)) + "cm")

        elif self._navi.GetPath() is not None and ENGINE == ENGINES.JAKUB:
            for i in self._navi.GetPath():
                print("X position: " + str(round(self._nns.xCoor, 10)) + "cm")
                print("X position predict: " + str(round(i[0], 10)) + "cm")
                print("Y position: " + str(round(self._nns.yCoor, 10)) + "cm")
                print("Y position predict: " + str(round(i[1], 10)) + "cm")

        else:
            print("X position: " + str(round(self._nns.xCoor, 10)) + "cm")
            print("Y position: " + str(round(self._nns.yCoor, 10)) + "cm")
        print("Battery value: " + str(self._enc.batteryValue) + "mAh")
        print("Destination ID:" + str(self._nns.goingToID))
        print("Destination Triger:" + str(self._wheels.GetDriveMode()))

    #TODO: PROVIDE DESTINATION FROM PARAMMANAGER
    def CheckPaths(self):
        self._navi.FindPath(self._enc.batteryValue, (self._nns.xCoor, self._nns.yCoor), self._nns.heading, self._nns.goingToID)

    def Navigate(self):
        self.CheckPaths()

        # NEW ROTATION
        self._nns.heading = self._navi.GetHeading()

        #TEST POSITION FLICK JAKUB
        # if self._navi.GetPath() and timer.GetTicks() > 10000:
        #     self._nns.xCoor = self._navi.GetPath()[0][0]
        #     self._nns.yCoor = self._navi.GetPath()[0][1]

    def Draw(self):
       
        pygame.draw.circle(self._canvas, GREEN,(self._nns.xCoor + ROOM_W_OFFSET, self._nns.yCoor + ROOM_H_OFFSET),AGV_SIZE)
        pygame.draw.circle(self._canvas,RED,
                        (self._nns.xCoor + ROOM_W_OFFSET + 5 * math.cos(math.radians(self._nns.heading))
                            ,self._nns.yCoor + ROOM_H_OFFSET + 5 * math.sin(math.radians(self._nns.heading)) ) , 2)
        if self._navi.GetPath() is not None:
            for i in self._navi.GetPath():
                if ENGINE == ENGINES.OLEK:  
                    pygame.draw.rect(self._canvas, RED, pygame.Rect(i[0] + ROOM_W_OFFSET, i[1] + ROOM_H_OFFSET, GRID_DENSITY, GRID_DENSITY))
                if ENGINE == ENGINES.JAKUB:   
                    pygame.draw.rect(self._canvas, RED, pygame.Rect(i[0] + ROOM_W_OFFSET, i[1], GRID_DENSITY, GRID_DENSITY))
        
    def CalculateTurn(self):
        return self._navi.CalculateTurn(self._nns)
    
    def GetDistance(self):
        return self._navi.GetDistance()