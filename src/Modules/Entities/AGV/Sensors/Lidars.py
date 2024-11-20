# -*- coding: utf-8 -*-
"""Lidar module

Module which simulates Lidar system of AGV, based on provided image of room,
checks for approaching walls to potentialy stop AGV before collision.
"""
class Lidars:
    def __init__(self) -> None:
        self._emergencyStop = False
        self._stop = False

    def Init(self):
        self._emergencyStop = False
        self._stop = False

    def DetermineFlags(self):
        #provide lidar logic, probably based on canva and close pixels
        pass

    def EmergencyStop(self):
        self._emergencyStop = True

    def Stop(self):
        self._stop = True

    def GetEmergencyStop(self):
        return self._emergencyStop

    def GetStop(self):
        return self._stop