from tkinter import BooleanVar

from opcua import Client


class OPCDataGrabber:
    def __init__(self):
        self._url = "opc.tcp://localhost:4841/freeopcua/server/"
        self._dataFromServer = 0
        self._nodeId = "ns=2;i="
        self._serverStatus = "i=2259"
        self.dataReceived = "X-coordinate,Y-coordinate,Heading,Battery cell voltage,Speed\n"
        self.client = None
        self.timeInterval = None
        self.ConnectToServer()

    def ConnectToServer(self):
        try:
            self.client = Client(self._url)
            self.client.connect()
            print("Connected to OPC UA server.")
        except Exception as e:
            print("Failed to connect to OPC UA server:", e)

    def StartReception(self,it):
        try:
            self._nodeId += str(it)
            node = self.client.get_node(self._nodeId)
            value = node.get_value()
            self.dataReceived += f"{value}"
            if(it == 6):
                self.dataReceived += "\n"
            else:
                self.dataReceived += ","
        except Exception as e:
            print("Error during StartReception:", e)
            self.ConnectToServer()
            # self.client = None
        finally:
            self._nodeId = "ns=2;i="

    def CloseConnection(self):
        self.client.disconnect()

    def ReceiveDataFromServer(self):
        if self.client is None:
            self.ConnectToServer()

        if self.client is not None:
            tab = [7, 8, 5, 10, 6]
            try:
                for i in tab:
                    self.StartReception(i)
            except ConnectionResetError:
                print("Connection was reset. Attempting to reconnect...")
                self.ConnectToServer()
    def SetTimeInterval(self):
        file = open("../../Config/config.txt")

        self.timeInterval = float(file.read())
