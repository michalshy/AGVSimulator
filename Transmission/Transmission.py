import socket  # Import socket module
from Simulation.AGV.AGV import AGV
from opcua import Client


class Transmission(object):
    def __init__(self, agv: AGV):
        self._sock = socket.socket()
        self._port = 50000  # placeholder
        self._host = '127.0.0.1'  # placeholder
        self._data = ''
        self._agv = agv
        self._url = "opc.tcp://localhost:4841/freeopcua/server/"
        self._nodeId = "ns=2;i="

    def Transmit(self,input,it):
        self._nodeId += str(it)
        client = Client(self._url)
        client.connect()
        node = client.get_node(self._nodeId)
        node.set_data_value(input)
        self._nodeId = "ns=2;i="   

    def CloseConnection(self):
        print('closing')
        client.disconnect()
