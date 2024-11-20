from Modules.Entities.Frame6000.ENC import ENC
from Modules.Entities.Frame6000.SS import SS
from Modules.Entities.Frame6000.NNS import NNS
from Modules.Entities.Frame6100.NNC import NNC 
from Modules.Entities.AGV.Sensors.Lidars import Lidars
from Modules.Entities.AGV.Sensors.Wheels import Wheels
from Modules.Entities.AGV.Sensors.Navigator import Navigator
from Modules.Entities.AGV.Sensors.Battery import Battery
from Modules.Simulation.Logic.Timer import *
import pygame
import math
from Globals import *
# -*- coding: utf-8 -*-
"""AGV module

Module responsible for single AGV behaviour. Does not take any action on its own,
provides API functions for Simulation module to use.
The manipulation it provides on its own is flags it controls.
By this flags Physics module can know if some action is possible.
Simulation also uses flags to control flow.
"""
class AGV:
    def __init__(self):
        self._isOrder = False

        # For frames
        self._enc = ENC()
        self._ss = SS()
        self._nns = NNS()
        
        # base params
        self._boundryBattery = 0

        #sensors
        self._battery = Battery()
        self._navi = Navigator()
        self._wheels = Wheels()
        self._lidars = Lidars()

        #flags
        self._stopFlag = False

    def Init(self, x, y):
        self._enc.batteryValue = 120000

        #TODO: ADD PROPER HANDLER FOR START POSITION
        self._nns.xCoor = x * 10
        self._nns.yCoor = y * 10

        self._battery.Init(self._enc.batteryValue)
        self._navi.Init()
        self._wheels.Init()
        self._lidars.Init()

    def SetRouteParams(self, nnc: NNC):
        self.SetDestId(nnc)
        self.SetDestTrig(nnc)

    def SetOrder(self, state: bool):
        self._isOrder = state

    def DetermineFlags(self):
        self._battery.DetermineFlags(self._enc.batteryValue)
        self._navi.DetermineFlags()
        self._wheels.DetermineFlags(self._nns.speed)
        self._lidars.DetermineFlags()

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

    def CheckDrive(self):
        if(self._isOrder):
            self._wheels.SetDriveMode(True)
        else:
            self._wheels.SetDriveMode(False)
        
        return self._wheels.GetDriveMode()
    
    def GetStopFlag(self):
        return self._stopFlag

    def PrintState(self):
        print("Heading: " + str(round(self._nns.heading,2)) + "degree")
        print("Speed: " + str(round(self._nns.speed / 100,2)) + "m/s")
        print("Battery value: " + str(self._enc.batteryValue) + "mAh")
        print("Destination ID:" + str(self._nns.goingToID))
        print("Destination Triger:" + str(self._wheels.GetDriveMode()))

    #TODO: PROVIDE DESTINATION FROM PARAMMANAGER
    def CheckPaths(self):
        self._navi.FindPath() #self._enc.batteryValue, (self._nns.xCoor, self._nns.yCoor), self._nns.heading, self._nns.goingToID

    def Navigate(self):
        self.CheckPaths()

    def Draw(self, canvas):
       
        pygame.draw.circle(canvas, GREEN,(self._nns.xCoor + ROOM_W_OFFSET, self._nns.yCoor + ROOM_H_OFFSET), AGV_SIZE)
        pygame.draw.circle(canvas,RED,
                        (self._nns.xCoor + ROOM_W_OFFSET + 5 * math.cos(math.radians(self._nns.heading))
                            ,self._nns.yCoor + ROOM_H_OFFSET + 5 * math.sin(math.radians(self._nns.heading)) ) , 2)
        self._navi.DrawPath(canvas)        
        
    def CalculateTurn(self):
        return self._navi.CalculateTurn(self._nns)
    
    def GetDistance(self):
        return self._navi.GetDistance()