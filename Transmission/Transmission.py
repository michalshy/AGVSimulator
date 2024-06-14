import socket  # Import socket module
from Simulation.AGV.AGV import AGV

class Transmission(object):
    def __init__(self, agv: AGV):
        self._sock = socket.socket()
        self._port = 50000  # placeholder
        self._host = '127.0.0.1'  # placeholder
        self._data = ''
        self._agv = agv

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
