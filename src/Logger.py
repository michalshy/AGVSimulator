from datetime import datetime
from enum import Enum
from Modules.Simulation.Logic.Timer import *
# -*- coding: utf-8 -*-
"""Logger module
Wrapper around python logging module with additional functionality or providing
state of AGV to different file. On its cycle, when simulation calls desired
method, logger appends AGV state into specified file.
Logger produces as well file with logs, which contains informations printed on the
output stream during simulation execution
"""


STATE_CYCLE = 1000

Levels = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

class Logger:

    def __init__(self) -> None:
        self._nameOfFile = ""
        self._InitAGVFile()
        self._cycle = STATE_CYCLE
        self._lvl = 0

    def GetFileName(self):
        return self._nameOfFile

    def Debug(self, msg):
        if self._lvl >= 4:
            self._Log(msg, 4)

    def Info(self, msg):
        if self._lvl >= 3:
            self._Log(msg, 3)

    def Warning(self, msg):
        if self._lvl >= 2:
            self._Log(msg, 2)

    def Error(self, msg):
        if self._lvl >= 1:
            self._Log(msg, 1)

    def Critical(self, msg):
        if self._lvl >= 0:
            self._Log(msg, 0)

    def SetLevel(self, level):
        self._lvl = level
    
    def _Log(self, msg, lvl):
        print(f'{Levels[lvl]:10} {datetime.now()}  {msg:100}')

    def _InitAGVFile(self):
        self._nameOfFile = datetime.now().strftime("./Logs/%d%m%Y%H%M%S") + ".csv"
        f = open(self._nameOfFile, "w")
        f.close()

logger = Logger()