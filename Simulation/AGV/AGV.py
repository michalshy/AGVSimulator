from Simulation.Frame6000.ENC import ENC
from Simulation.Frame6000.SS import SS
from Simulation.Frame6000.NNS import NNS
from Simulation.Frame6100.NNC import NNC
import pygame
import math
from Simulation.AGV.Navigator.Navigator import Navigator
from Globals import *

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(a[1]-b[1], a[0]-b[0]) - math.atan2(c[1]-b[1], c[0]-b[0]))
    return ang + 360 if ang < 0 else ang

# Class that holds state of AGV
class AGV:
    def __init__(self, canvas):
        #pygame
        self._canvas = canvas
        self._color = (0,255,0)

        # For frames
        self._enc = ENC()
        self._ss = SS()
        self._nns = NNS()
        self._maxSpeed = 50 #TODO: figure out when agv can move faster to 150
        self._enc.batteryValue = 120000
        self._boundryBattery = self._enc.batteryValue * 0.3
        self._nns.heading = -90

        #TODO: ADD PROPER HANDLER FOR START POSITION
        self._nns.xCoor = 400
        self._nns.yCoor = 400

        # flags
        self.atMaxSpeed = False
        self.batteryAvailable = True
        self.driveMode = False

        #navi
        self._navi = Navigator()
        self._path = []

    def InitNavi(self, img: pygame.image):
        self._navi.Init(img)

    def SetDestId(self, nnc: NNC):
        self._nns.goingToID = nnc.destID

    def SetDestTrig(self, nnc: NNC):
        self.driveMode = nnc.goDestTrig

    def DetermineFlags(self):
        if self._nns.speed >= self._maxSpeed:
            self.atMaxSpeed = True
            self._nns.speed = self._maxSpeed
        else:
            self.atMaxSpeed = False

        if self._enc.batteryValue > self._boundryBattery:
            self.batteryAvailable = True
        else:
            self.batteryAvailable = False
            self.driveMode = False


    def GetENC(self):
        return self._enc

    def GetSS(self):
        return self._ss

    def GetNNS(self):
        return self._nns

    def GetMaxSpeed(self):
        return self._maxSpeed

    def GetBatteryAvailable(self):
        return self.batteryAvailable

    def GetAtMaxSpeed(self):
        return self.atMaxSpeed

    def GetDriveMode(self):
        return self.driveMode

    def PrintState(self):
        print("Heading: " + str(round(self._nns.heading,2)) + "degree")
        print("Speed: " + str(round(self._nns.speed / 100,2)) + "m/s")
        print("X position: " + str(round(self._nns.xCoor / 100, 2)) + "m")
        print("Y position: " + str(round(self._nns.yCoor / 100, 2)) + "m")
        print("Battery value: " + str(self._enc.batteryValue) + "mAh")
        print("Destination ID:" + str(self._nns.goingToID))
        print("Destination Triger:" + str(self.driveMode))

        self.Draw()

    def SetDriveMode(self, state: bool):
        self.driveMode = state

    #TODO: PROVIDE DESTINATION FROM PARAMMANAGER
    def CheckPaths(self):
        self._navi.FindPath((self._nns.xCoor, self._nns.yCoor), (900,400))
        self.SetPathToFollow()

    def Navigate(self):
        self.CheckPaths()

    def Draw(self):
        for i in self._path:
            pygame.draw.rect(self._canvas, (255,0,0), pygame.Rect(i[0], i[1], GRID_DENSITY, GRID_DENSITY))
        pygame.draw.circle(self._canvas, self._color,(self._nns.xCoor, self._nns.yCoor),AGV_SIZE)
        pygame.draw.circle(self._canvas,(255,0,0),
                           (self._nns.xCoor + 25 * math.cos(math.radians(self._nns.heading))
                             ,self._nns.yCoor + 25 * math.sin(math.radians(self._nns.heading)) ) , 7)
        
    def SetPathToFollow(self):
        self._path.clear()
        for i in self._navi.GetPathToFollow():
            self._path.append((i[1] * GRID_DENSITY + ROOM_W_OFFSET, i[0] * GRID_DENSITY + ROOM_H_OFFSET))

    #[0] IS FOR X, [1] IS FOR Y
    def GetPath(self):
        return self._path

    def CalculateTurn(self):
        pointBeginning = (self._nns.xCoor, self._nns.yCoor)
        pointHeading = (self._nns.xCoor + 25 * math.cos(math.radians(self._nns.heading)), self._nns.yCoor + 25 * math.sin(math.radians(self._nns.heading)))
        return getAngle(self._path[0], pointBeginning, pointHeading)
        

