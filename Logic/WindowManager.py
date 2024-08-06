from pygame import *

class WindowManager:
    def __init__(self, canvas: Surface) -> None:
        self._canvas = canvas
        self._backgroundColor = (0,0,0)

    def PrepWindow(self):
        self._canvas.fill(self._backgroundColor)
