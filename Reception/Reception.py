import socket  # Import socket module

port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()  # Create a socket object
host = ""  # Get local machine name
s.bind(('localhost', port))  # Bind to the port
s.listen(5)  # Now wait for client connection.

print('Server listening....')

x = 0

while True:
    conn, address = s.accept()  # Establish connection with client.

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

conn.close()
