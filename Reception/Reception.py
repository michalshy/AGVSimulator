import socket  # Import socket module
from Simulation.ParamManager import ParamManager
from opcua import Client


class Reception:
    def __init__(self, paramManager: ParamManager):
        self._port = 50000  # placeholder
        self._sock = socket.socket()
        self._host = '127.0.0.1'  # placeholder
        self._data = ''
        self._param_manager = paramManager
        self._url = "opc.tcp://localhost:4841/freeopcua/server/"
        self._nodeId = "ns=2;i="
        self._dataFromServer = []
        self.value = ""

    def StartReceptionLocal(self):
        self._param_manager.fabricateFrames()

    def StartReception(self,it):
        self._nodeId += str(it)
        client = Client(self._url)
        client.connect()
        node = client.get_node(self._nodeId)
        value = node.get_value()
        self._dataFromServer.append(value)

        self._nodeId = "ns=2;i=" 

    def CloseConnection(self, conn):
        client.disconnect()
