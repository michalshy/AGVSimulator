from tkinter import BooleanVar

from opcua import Client


class OPCDataGrabber:
    def __init__(self):
        self._url = "opc.tcp://157.158.57.71:48050"
        self._dataFromServer = 0
        self._serverStatus = "i=2259"
        self.dataReceived = "X-coordinate,Y-coordinate,Heading,Going to ID,Current segment\n"  #brakuje battery cell voltage
        self.frame6000 = self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()
        self.frame6100 = self.client.get_root_node().get_children()[0].get_children()[1].get_children()[2].get_children()
        self.NNS = self.frame6000[-4].get_children()
        self.ENS = self.frame6100[-6].get_children()
        self.client = None
        self.timeInterval = None
        self.ConnectToServer()

    def ConnectToServer(self):
        try:
            self.client = Client('opc.tcp://157.158.57.71:48050')
            self.client.connect()
            print("Connected to OPC UA server.")
        except Exception as e:
            print("Failed to connect to OPC UA server:", e)

        print(self.client.get_root_node().get_children()[0].get_children()[1].get_children()[2].get_children())  # wejscie do ramki 6100
        print(self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children())  # wejscie do ramki 6000
        print(self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()[-4].get_children())  # wejscie do NNS
        print(self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()[-4].get_children()[5].get_value())  # wartosc x-coor
        print(self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()[-4].get_children()[6].get_value())  # wartosc y-coor
        print(self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()[-4].get_children()[7].get_value())  # wartosc heading
        print(self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()[-4].get_children()[11].get_value())  # wartosc going to id
        print(self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()[-4].get_children()[13].get_value())  # wartosc current segment
        print(self.client.get_root_node().get_children()[0].get_children()[1].get_children()[2].get_children()[-6].get_children()) # wejscie do energy signals (battery cell value)







        print(self.client.get_objects_node())

    def StartReception(self, it):
        try:
            node = self.client.get_node(self.NNS[it].get_value())
            value = node.get_value()
            self.dataReceived += f"{value}"
            if(it == 13):
                 self.dataReceived += "\n"
            else:
                 self.dataReceived += ","
        except Exception as e:
            print("Error during StartReception:", e)
            self.ConnectToServer()
            # self.client = None
        # finally:
        #     self._nodeId = "FN.6000.[NNS] - Natural Navigation Signals"

    def CloseConnection(self):
        self.client.disconnect()

    def ReceiveDataFromServer(self):
        if self.client is None:
            self.ConnectToServer()

        if self.client is not None:
            tab = [5,6,7,11,13]
            try:
                for i in tab:
                    self.StartReception(i)
            except ConnectionResetError:
                print("Connection was reset. Attempting to reconnect...")
                self.ConnectToServer()
                # self.client = None

    def SetTimeInterval(self):
        file = open("../../Config/config.txt")

        self.timeInterval = float(file.read())
