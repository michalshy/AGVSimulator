import socket  # Import socket module
from Simulation.ParamManager import ParamManager


class Reception:
    def __init__(self, paramManager: ParamManager):
        self._port = 50000  # placeholder
        self._sock = socket.socket()
        self._host = '127.0.0.1'  # placeholder
        self._data = ''
        self._param_manager = paramManager

    def StartReceptionLocal(self):
        self._param_manager.fabricateFrames()

    def StartReception(self):
        self._sock.bind((self._host, self._port))
        self._sock.listen(5)  # Now wait for client connection.
        print('Server listening....')
        x = 0
        while True:
            conn, address = self._sock.accept()  # Establish connection with client.

            while True:
                try:
                    print('Got connection from', address)
                    data = conn.recv(1024)
                    print('Server received', data)

                    st = 'Thank you for connecting'
                    byt = st.encode()
                    conn.send(byt)

                    x += 1

                except Exception as e:
                    print(e)
                    break
        self.CloseConnection(conn)

    def CloseConnection(self, conn):
        conn.close()
