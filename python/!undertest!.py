import ubinascii as binascii
import uhashlib as hashlib
import uasyncio as asyncio
import urandom as random
import usocket as socket
import network
from machine import Timer

ssid = 'Jarinya'
password = '19771977'
IP = '192.168.1.99'
PORT = 80
subnet = '255.255.255.0'
gateway = '192.168.1.1'
dns = '8.8.8.8'
ssid = 'Jarinya'
password = '19771977'

# Configure as a station
# Try to connect to primary AP if failed try to connect to secondary AP


def connect(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    print('Try to connect to ' + ssid + '...')

    time.sleep(5)
    if station.isconnected() == False:
        print('Cannot connect to ' + ssid + '...')
        connected = False
        station.active(False)
    else:
        print('Connected to to ' + ssid + '!')
        print(station.ifconfig())
        connected = True
    return connected


connected = connect('DasNet', 'Benoit666')

if connected == False:
    connected = connect('Jarinya', '19771977')

print(connected)

#station = network.WLAN(network.STA_IF)
# station.active(True)
#station.ifconfig((IP, subnet, gateway, dns))
#station.connect(ssid, password)

randomNumber = 0

while station.isconnected() == False:
    pass

# Configure as an access point
print('Connection successful')
print(station.ifconfig())

ssid = 'C9'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while ap.active() == False:
    pass

print('AP Config done')
print(ap.ifconfig())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
conn = None
ws = False


def ClientWrite(msg):
    print('Try to send message: ' + str(msg))
    frame = [129]
    frame += [len(msg)]
    frame_to_send = bytearray(frame) + msg
    if ws:
        conn.send(frame_to_send)


def randomizer():
    global randomNumber
    randomNumber = random.getrandbits(8)
    ClientWrite(str(randomNumber))


tim = Timer(-1)
tim.init(period=60000, mode=Timer.PERIODIC, callback=lambda t: randomizer())


def ClientHandshake(conn, data):
    data = data.decode().split('\r')
    for items in data:
        if 'Sec-WebSocket-Key' in items:
            print('Socket handshaking...')
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
            print('Client is connected!!!')


# The communication loop accept either HTTP or WS
while(1):
    conn, addr = s.accept()
    ws = False
    print('Got a connection from %s' % str(addr))
    while(1):
        data = conn.recv(1024)
        try:
            msg = data.decode()
            print(msg)
        except:
            print('Cannot decode')

        if (len(data) <= 8):
            print('Client left...')
            ws = False
            conn.close()
            break

        if 'Sec-WebSocket-Key' in msg:
            ClientHandshake(conn, data)
            ws = True

        if ws == False:
            conn.send(str(randomNumber))
            conn.close()
            break

# Abnormal : Out of communication loop, restart
machine.reset()
