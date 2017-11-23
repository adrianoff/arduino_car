from base64 import b64encode
from hashlib import sha1

headers = {}
headers["Sec-WebSocket-Key"] = "aaa"

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
sha1code = sha1(headers["Sec-WebSocket-Key"].encode() + GUID.encode())
response_key = b64encode(sha1code.digest()).decode()

a = 1