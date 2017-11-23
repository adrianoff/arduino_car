import socket

sock = socket.socket()
sock.connect(('localhost', 9999))
sock.send("HELLO".encode())

while 1:
    data = sock.recv(1)
    print(data.decode())

sock.send("CLOSE".encode())

sock.close()

print(data.decode())
