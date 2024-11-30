import threading

_PATH = []
_PATH_MUTEX = threading.Lock()

class PathMetaclass(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class PathSingleton(metaclass=PathMetaclass):
    def Append(self, el):
        global _PATH_MUTEX
        _PATH_MUTEX.acquire()
        try:
            _PATH.append(el)
        finally:
            _PATH_MUTEX.release()

    def Return(self):
        path = []
        global _PATH_MUTEX
        _PATH_MUTEX.acquire()
        try:
            path = _PATH.copy()
        finally:
            _PATH_MUTEX.release()
        return path
    
    def PopBack(self):
        global _PATH_MUTEX
        _PATH_MUTEX.acquire()
        try:
            _PATH.pop()
        finally:
            _PATH_MUTEX.release()

    def PopFront(self):
        global _PATH_MUTEX
        _PATH_MUTEX.acquire()
        try:
            _PATH.pop(0)
        finally:
            _PATH_MUTEX.release()