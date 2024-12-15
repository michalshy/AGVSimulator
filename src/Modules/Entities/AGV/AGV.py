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
from enum import Enum
# -*- coding: utf-8 -*-
"""AGV module

Module responsible for single AGV behaviour. Does not take any action on its own,
provides API functions for Simulation module to use.
The manipulation it provides on its own is flags it controls.
By this flags Physics module can know if some action is possible.
Simulation also uses flags to control flow.
"""

class AGV_STATE(Enum):
    INIT = 0,
    SIM = 1,
    SIM_CHECK = 2,
    SIM_APPLY = 3,
    SIM_DRIVE = 4,
    NO_SIM = 5,
    ERR = 6

class AGV:
    def __init__(self):
        self._state = AGV_STATE.INIT
        self._isOrder = False
        self._setFirst = False
        self._setParams = False
        self._order = []
        self._traversed = []

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

    def _DetermineDriveAvailabilty(self):
        if not self._battery.GetBatterAvailable() or \
            not self._navi.TaskInProgress() or \
            not self._wheels.GetDriveMode() or \
            not self._lidars.GetEmergencyStop() or \
            not self._lidars.GetStop():
            self._canDrive = False

    def CheckDrive(self):
        if self._navi.TaskInProgress():
            self._stopFlag = False
            self._wheels.SetDriveMode(True)
        elif len(self._navi.GetPath()) == 0:
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

    def Run(self, physics: Physics):
        match self._state:
            case AGV_STATE.INIT:
                self._setFirst = False
                self._traversed.clear()
                self._CheckPaths()
            case AGV_STATE.SIM:
                self._CheckSimPoint()
            case AGV_STATE.SIM_CHECK:
                self.DetermineFlags()
                if self.CheckDrive():   
                    physics.SetSpeed(self._wheels.GetMaxSpeed())
                else:
                    physics.Stop()
                self._MoveState(AGV_STATE.SIM_DRIVE)
            case AGV_STATE.SIM_DRIVE:
                self._ControlNavigation(physics)
                self._MoveState(AGV_STATE.SIM_APPLY)
            case AGV_STATE.SIM_APPLY:
                physics.Update()                             # Update positions
                self._MoveState(AGV_STATE.SIM)
            case AGV_STATE.NO_SIM:
                self._MoveState(AGV_STATE.INIT)
            case AGV_STATE.ERR:
                logger.Critical("Error during simulation")

    ### LOGGER ###
    def _ConstructLine(self):
        return str(self._nns.heading) + "," + str(self._nns.speed * 100) + "," + str(self._nns.xCoor) + "," \
                            + str(self._nns.yCoor) + "," + str(self._enc.batteryValue) + "\n"               

    def LogToFile(self):
        if timer.GetTicks() > (self._logCycle + STATE_CYCLE):
            f = open(logger.GetFileName(), "a")
            f.write(self._ConstructLine())
            f.close()
            self._logCycle = timer.GetTicks()
    ### LOGGER END ###

    ### GETTERS ###
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
    ### GETTERS END ###
    
    ### PYGAME ###
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
        for coord in self._traversed:
            pygame.draw.rect(canvas, GREEN, pygame.Rect(
                PointsInterpolationWidth(coord[0]) + Additional.ROOM_W_OFFSET,
                PointsInterpolationHeight(coord[1]) + Additional.ROOM_H_OFFSET, 
                3, 
                3
            ))
    ### PYGAME END ###

    ### PRIVATES ###
    def _MoveState(self, state):
        logger.Debug("Move to state " + str(state))
        self._state = state

    def _CheckSimPoint(self):
        if len(self._navi.GetPath()) != 0:
            self._MoveState(AGV_STATE.SIM_CHECK)
        elif not self._navi.TaskInProgress():
            logger.Debug("Simulation end")
            self._MoveState(AGV_STATE.NO_SIM)
                
    def _CheckPaths(self):
        if self._isOrder:
            logger.Info("Order detected")
            self._navi.FindPath(self._order, self._data) #self._enc.batteryValue, (self._nns.xCoor, self._nns.yCoor), self._nns.heading, self._nns.goingToID
            self._MoveState(AGV_STATE.SIM)

    def _ControlNavigation(self, physics: Physics):
        # Check if is available to follow path
        if len(self._navi.GetPath()) != 0:
            # Determine target
            tempPos = self._navi.GetPath()[0]
            # Transform object onto simulation start point
            if not self._setFirst:
                self._nns.xCoor = tempPos[0]
                self._nns.yCoor = tempPos[1]
            # Check heading difference and distance
            heading, dist = physics.CalculatePath(self._nns, tempPos)
            # Set heading and battery on predicted one
            if self._setParams == False:
                self._nns.heading -= heading
                self._enc.batteryValue = tempPos[3]
                self._setParams = True
            # Check if target point is reached (always true for 1st point)            
            if self._nns.xCoor > tempPos[0] - 0.1 and self._nns.xCoor < tempPos[0] + 0.1:
                if self._nns.yCoor > tempPos[1] - 0.1 and self._nns.yCoor < tempPos[1] + 0.1:
                    # If reached, pop point
                    self._traversed.append(tempPos)
                    self._navi.PopFrontPath()
                    # Determine distance to next point and base speed on this,
                    # Ommit first transform, we do not know from where agv got transferred
                    if self._setFirst:
                        self._wheels.SetMaxSpeed(dist * config['agv']['amplifier'])
                    self._setFirst = True
                    self._setParams = False
            # Adjust heading, simulate odometry
    ### PRIVATES END ###
    