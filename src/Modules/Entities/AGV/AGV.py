from Modules.Entities.Frame6000.ENS import ENS
from Modules.Entities.Frame6000.SS import SS
from Modules.Entities.Frame6000.NNS import NNS
from Modules.Entities.Frame6100.NNC import NNC 
from Modules.Entities.AGV.Sensors.Lidars import Lidars
from Modules.Entities.AGV.Sensors.Wheels import Wheels
from Modules.Entities.AGV.Sensors.Navigator import Navigator
from Modules.Entities.AGV.Sensors.Battery import Battery
from Modules.Simulation.Logic.Timer import *
from Modules.Entities.Physics import Physics
import pygame
from Logger import *
import math
from Config import *
import pandas as pd
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
        self._setFirst = False
        self._order = []
        self._toHeading = 0

        self._shouldSlow = False

        self._data = None

        # For frames
        self._ens = ENS()
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

        #logging
        self._logCycle = 0

    def Init(self, x, y):
        self._ens.batteryCellVolt = 50000

        #TODO: ADD PROPER HANDLER FOR START POSITION
        self._nns.xCoor = x
        self._nns.yCoor = y

        self._battery.Init(self._ens.batteryCellVolt)
        self._navi.Init()
        self._wheels.Init()
        self._lidars.Init()

    def SetPosition(self, x, y):
        self._nns.xCoor = x
        self._nns.yCoor = y

    def SetOrder(self, state: bool, segments: list):
        self._isOrder = state
        self._order = segments

    def SetData(self, data: pd.DataFrame):
        self._data = data

    def DetermineFlags(self):
        self._battery.DetermineFlags(self._ens.batteryCellVolt)
        self._navi.DetermineFlags()
        self._wheels.DetermineFlags(self._nns.speed)
        self._lidars.DetermineFlags()

    def GetIsOrder(self):
        return self._isOrder

    def GetOrder(self):
        return self._order

    def GetENS(self):
        return self._ens

    def GetSS(self):
        return self._ss

    def GetNNS(self):
        return self._nns

    def GetBatteryAvailable(self):
        return self._battery.GetBatterAvailable()

    def GetAtMaxSpeed(self):
        return self._wheels.GetAtMaxSpeed()

    def CheckDrive(self):
        if self._nns.speed > self._wheels.GetMaxSpeed():
            self._shouldSlow = True
        else:
            self._shouldSlow = False

        if(self._navi.TaskInProgress()):
            self._stopFlag = False
            self._wheels.SetDriveMode(True)
        else:
            self._stopFlag = True
            self._wheels.SetDriveMode(False)
        
        return self._wheels.GetDriveMode()
    
    def GetStopFlag(self):
        return self._stopFlag

    def Navigate(self, physics: Physics):
        self._CheckPaths()
        self._ControlNavigation(physics)

    def ShouldSlow(self):
        return self._shouldSlow

    def Draw(self, canvas):
       
        pygame.draw.circle(canvas, GREEN, \
                           (PointsInterpolationWidth(self._nns.xCoor) + Additional.ROOM_W_OFFSET, \
                            PointsInterpolationHeight(self._nns.yCoor) + Additional.ROOM_H_OFFSET), \
                            config['agv']['agv_size'])
        pygame.draw.circle(canvas,RED, \
                        (PointsInterpolationWidth(self._nns.xCoor) + Additional.ROOM_W_OFFSET + \
                         5 * math.cos(math.radians(self._nns.heading))
                        ,PointsInterpolationHeight(self._nns.yCoor) + Additional.ROOM_H_OFFSET + \
                        5 * math.sin(math.radians(self._nns.heading)) ) , 2)
        self._navi.DrawPath(canvas)        
    
    def _ConstructLine(self):
        return str(self._nns.heading) + "," + str(self._nns.speed * 100) + "," + str(self._nns.xCoor) + "," \
                            + str(self._nns.yCoor) + "," + str(self._ens.batteryCellVolt) + "\n"
    
    def _CheckPaths(self):
        if self._isOrder:
            logger.Info("Order detected")
            self._navi.FindPath(self._order, self._data) #self._enc.batteryValue, (self._nns.xCoor, self._nns.yCoor), self._nns.heading, self._nns.goingToID
            self._isOrder = False

    def _ControlNavigation(self, physics: Physics):
        if len(self._navi.GetPath()) != 0:
            tempPos = self._navi.GetPath()[0]
            heading, dist = physics.CalculatePath(self._nns, tempPos)
            self._ens.batteryCellVolt = tempPos[3]
            if not self._setFirst:
                self._nns.xCoor = tempPos[0]
                self._nns.yCoor = tempPos[1]
                self._nns.heading = Degrees(tempPos[2])
            if self._nns.xCoor > tempPos[0] - 0.1 and self._nns.xCoor < tempPos[0] + 0.1:
                if self._nns.yCoor > tempPos[1] - 0.1 and self._nns.yCoor < tempPos[1] + 0.1:
                    self._navi.PopFrontPath()
                    _txt = "Dist is " + str(dist)
                    logger.Debug(_txt)
                    if self._setFirst:
                        self._wheels.SetMaxSpeed(dist/config['agv']['amplifier'])
                    self._setFirst = True
            if heading > 0 and heading < 180:
                self._nns.heading -= 1
            else:
                self._nns.heading += 1

    def LogToFile(self):
        if timer.GetTicks() > (self._logCycle + STATE_CYCLE):
            f = open(logger.GetFileName(), "a")
            f.write(self._ConstructLine())
            f.close()
            self._logCycle = timer.GetTicks()