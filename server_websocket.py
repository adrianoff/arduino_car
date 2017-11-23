    #!/usr/bin/env python

import socket, struct, hashlib, threading, cgi
from base64 import b64encode
from hashlib import sha1


def parse_headers(data):
    headers = {}
    lines = data.splitlines()
    if len(lines) > 0:
        for l in lines:
            parts = l.decode().split(": ", 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]
        headers['code'] = lines[len(lines) - 1]

    return headers


def create_sec_key(key):
    guid = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    sha1code = sha1(key.encode() + guid.encode())
    response_key = b64encode(sha1code.digest()).decode()
    return response_key


def handshake(client):
    print('Handshaking...')
    data = client.recv(1024)
    headers = parse_headers(data)
    print('Got headers:')
    return_data = ""
    for k in headers:
        print(k, ':', headers[k])

    if "Sec-WebSocket-Key" in headers:
        client_type = "WEB"
        response_key = create_sec_key(headers["Sec-WebSocket-Key"])
        shake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
        shake += "Upgrade: WebSocket\r\n"
        shake += "Connection: Upgrade\r\n"
        shake += "Sec-WebSocket-Origin: %s\r\n" % (headers['Origin'])
        shake += "Sec-WebSocket-Location: ws://%s\r\n" % (headers['Host'])
        shake += "Sec-WebSocket-Accept: %s\r\n\r\n" % response_key

        response = shake.encode()
        print('Send handshake:')
        print(response)
        client.send(response)
    else:
        if "User-Agent" in headers:
            client_type = "AJAX"
            return_data = headers['code'].decode()
            client.send('OK'.encode())
            client.close()
        else:
            client_type = "CAR"
            response = "HELLO".encode()
            client.send(response)

    return {"client_type": client_type, "data": return_data}


def decode_response(data):
    byte_array = []
    for character in data:
        byte_array.append(character)

    data_length = byte_array[1] & 127
    index_first_mask = 2

    if data_length == 126:
        index_first_mask = 4
    elif data_length == 127:
        index_first_mask = 10

    masks = [m for m in byte_array[index_first_mask: index_first_mask+4]]
    index_first_data_byte = index_first_mask + 4
    decoded_chars = []
    i = index_first_data_byte
    j = 0

    while i < len(byte_array):
        decoded_chars.append(chr(byte_array[i] ^ masks[j % 4]))
        i += 1
        j += 1

    return decoded_chars


def encode_request(data):
    bytes_formatted = [129]

    bytes_raw = data.encode()
    bytes_length = len(bytes_raw)
    if bytes_length <= 125:
        bytes_formatted.append(bytes_length)
    elif 126 <= bytes_length <= 65535:
        bytes_formatted.append(126)
        bytes_formatted.append((bytes_length >> 8) & 255)
        bytes_formatted.append(bytes_length & 255)
    else:
        bytes_formatted.append(127)
        bytes_formatted.append((bytes_length >> 56) & 255)
        bytes_formatted.append((bytes_length >> 48) & 255)
        bytes_formatted.append((bytes_length >> 40) & 255)
        bytes_formatted.append((bytes_length >> 32) & 255)
        bytes_formatted.append((bytes_length >> 24) & 255)
        bytes_formatted.append((bytes_length >> 16) & 255)
        bytes_formatted.append((bytes_length >> 8) & 255)
        bytes_formatted.append(bytes_length & 255)

    bytes_formatted = bytes(bytes_formatted)
    bytes_formatted = bytes_formatted + bytes_raw

    return bytes_formatted


def handle(client, address):
    try:
        handshake_result = handshake(client)
        client_type = handshake_result['client_type']
        handshake_data = handshake_result['data']
    except Exception as e:
        print(str(e))
        if client in clients:
            clients.remove(client)
            client.close()

        return

    if client_type == "WEB":
        clients.append(client)
    else:
        if client_type == "AJAX":
            for c in car_clients:
                try:
                    ajax_data = handshake_data.encode()
                    c.send(ajax_data)
                except Exception:
                    if c in car_clients:
                        car_clients.remove(c)
                        c.close()
            return 0
        else:
            car_clients.append(client)
    lock = threading.Lock()
    while 1:
        if client_type == "WEB":
            try:
                t = client.recv(1024, socket.MSG_PEEK)
                if len(t) == 0:
                    client.close()
                    break

                decoded_chars = ''.join(decode_response(client.recv(1024)))
            except Exception:
                if client in clients:
                    clients.remove(client)
                    client.close()
            lock.acquire()
            print(decoded_chars[0])
            send_string = encode_request(decoded_chars[0])
            for c in clients:
                try:
                    c.send(send_string)
                except Exception:
                    if c in clients:
                        clients.remove(c)
                        c.close()

            send_string = decoded_chars[0]
            for c in car_clients:
                try:
                    c.send(send_string.encode())
                except Exception:
                    if c in car_clients:
                        car_clients.remove(c)
                        c.close()
            lock.release()

    print('Client closed:', address)
    lock.acquire()
    clients.remove(client)
    lock.release()
    client.close()


def get_client_type(data):
    headers = parse_headers(data)
    pass


def start_server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 9999))
    s.listen(1000)

    while 1:
        connection, address = s.accept()
        print('Connection from:', address)
        threading.Thread(target=handle, args=(connection, address)).start()


clients = []
car_clients = []
start_server()
