import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, address = sock.accept()

while True:
    data = conn.recv(1024).decode()
    if data == 'CLOSE':
        print("CLOSE")
        break



    print(data.encode().upper())
    conn.send(data.encode().upper())

conn.close()
