import socket  # Import socket module
import os
import re

from opcua import Client
import time


class Transmission(object):
    def __init__(self):
        self._sock = socket.socket()
        self._port = 48060  # placeholder
        self._host = 'opc.tcp://localhost'  # placeholder
        self._data = ''
        self._server_adress = "opc.tcp://localhost:48060"
        self._nodeId = "ns=2;s=Tag7"
        self._client = Client("opc.tcp://localhost:48060")

    def Transmit(self):
        self._sock.connect((self._host, self._port))
        x = 0
        st = str(x)
        byt = st.encode()
        self._sock.send(byt)
        while x < 100:
            st = str(x)
            byt = st.encode()
            self._sock.send(byt)

            print(x)

            while True:
                data = self._sock.recv(1024)
                if data:
                    print(data)
                    x += 1
                    break

                else:
                    print('no data received')
        self.CloseConnection()

    def CloseConnection(self):
        print('closing')
        self._sock.close()
