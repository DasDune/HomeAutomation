
import usocket as socket
import ubinascii as binascii
import uhashlib as hashlib

from loader import connect
from loader import readConfig
from loader import log

connect('static')

config = readConfig()
IP = config['IP']
PORT = config['wsPort']

# Socket Init.
conn = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP, 55))
sock.listen(5)
print('socket server listening at IP: ' + IP + ' PORT: ' + '55')


# Socket read message decoder
def ClientRead(data):
    opcode_and_fin = data[0]
    msg_len = data[1] - 128
    mask = data[2:6]
    encrypted_msg = data[6: 6+msg_len]
    msg = bytearray([encrypted_msg[i] ^ mask[i % 4]
                     for i in range(msg_len)])
    clientMsg = str(msg, "utf-8")
    log('Socket receiving message: ' + str(clientMsg))
    return clientMsg

# Socket write message encoder


def ClientWrite(msg):
    log('Socket sending message: ' + str(msg))
    frame = [129]
    frame += [len(msg)]
    frame_to_send = bytearray(frame) + msg
    if conn is not None:
        conn.send(frame_to_send)


# Handle the received decoded socket message
def HandleData(msg):
    print(msg)

# Socket handshake process from tcp to ws


def ClientHandshake(data):
    data = data.decode().split('\r')
    for items in data:
        if 'Sec-WebSocket-Key' in items:
            log('Socket handshaking...')
            key = items.split(': ')[1]
            resp = key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
            resp = hashlib.sha1(resp).digest()
            resp = binascii.b2a_base64(resp)[:-1]
            response = "HTTP/1.1 101 Switching Protocols\r\n" + \
                "Upgrade: websocket\r\n" + \
                "Connection: Upgrade\r\n" + \
                "Sec-WebSocket-Accept: %s\r\n\r\n" % (
                    resp.decode("utf-8"))
            conn.send(response.encode())
            log('Client is connected!!!')


# Socket process loop
while True:
    conn, addr = sock.accept()
    log('Socket client connection request from: ' + str(addr))
    handshake = True
    while True:
        data = conn.recv(1024)
        log('Socket data received...')
        if (len(data) <= 8):
            print('Socket client left...')
            conn = None
            break
        if handshake:
            ClientHandshake(data)
            handshake = False
        else:
            msg = ClientRead(data)
            ClientWrite(msg)
            HandleData(msg)
