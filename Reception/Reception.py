import socket  # Import socket module


class Reception:
    def __init__(self):
        self._port = 50000  # placeholder
        self._sock = socket.socket()
        self._host = 'localhost'  # placeholder
        self._sock.bind((self._host, self._port))
        self._data = ''

    def startConnection(self):
        self._sock.listen(5)  # Now wait for client connection.
        print('Server listening....')
        x = 0
        while True:
            conn, address = self._sock.accept()  # Establish connection with client.
            while True:
                try:
                    print('Got connection from', address)
                    self._data = conn.recv(1024)
                    print('Server received', self._data)
                    st = 'Thank you for connecting'
                    byt = st.encode()
                    conn.send(byt)
                    x += 1
                except Exception as e:
                    print(e)
                    break
            self.closeConnection(conn)

    def closeConnection(self, conn):
        conn.close()
