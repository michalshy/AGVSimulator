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

class L(Enum):
    OFF = -1,
    DEBUG = 0,
    INFO = 1,
    WARNING = 2,
    ERROR = 3,
    CRITICAL = 4

class Logger:

    def __init__(self) -> None:
        self._nameOfFile = ""
        self._InitAGVFile()
        self._cycle = STATE_CYCLE
        self._lvl = L.OFF.value

    def GetFileName(self):
        return self._nameOfFile

    def Debug(self, msg):
        if self._lvl >= L.DEBUG.value:
            self._Log(msg)

    def Info(self, msg):
        if self._lvl >= L.INFO.value:
            self._Log(msg)

    def Warning(self, msg):
        if self._lvl >= L.WARNING.value:
            self._Log(msg)

    def Error(self, msg):
        if self._lvl >= L.ERROR.value:
            self._Log(msg)

    def Critical(self, msg):
        if self._lvl >= L.CRITICAL.value:
            self._Log(msg)

    def _SetLevel(self, level):
        self._lvl = level
    
    def _Log(self, msg):
        print(f'{self._lvl.name:10} {datetime.now()}  {msg:100}')

    def _InitAGVFile(self):
        self._nameOfFile = datetime.now().strftime("./Logs/%d%m%Y%H%M%S") + ".csv"
        f = open(self._nameOfFile, "w")
        f.close()

logger = Logger()