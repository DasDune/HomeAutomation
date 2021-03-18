

import lib
from lib import log
from machine import Pin
from machine import reset
import ubinascii as binascii
import uhashlib as hashlib
import usocket as socket
import utime

from machine import Timer

log('Starting main.py...')

# configure the IO tags
print('Configuring the IO...')
tags = lib.readTags()

for tag in tags:
    pin = tags[tag]['pin']
    pType = tags[tag]['type']
    pin = Pin(pin, pType)
    tags[tag]['io'] = pin
    tags[tag]['io'].value(1)
    print('Tag name: ' + tags[tag]['name'] + ' pin: ' + str(tags[tag]['pin']))
log('Tags configured! ')

# Reading the sprinklers/lights schedule
# Scheduler runs every min.
log('scheduler started...')
tim = Timer(-1)
tim.init(period=60000, mode=Timer.PERIODIC, callback=lambda t: scheduler())

# configure for HTTP and WS ready
print('Configure HTTP and WS...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
conn = None
ws = False


def clientWrite(msg):
    print('Try to send message: ' + str(msg))
    frame = [129]
    frame += [len(msg)]
    frame_to_send = bytearray(frame) + msg
    if ws:
        conn.send(frame_to_send)

# scheduler routine


def scheduler():
    min = (utime.localtime()[4])
    hour = int((utime.localtime()[3]) + 7)

    # Adjust hours between 24-30
    if hour > 23 and hour < 31:
        hour = hour - 24

    currTime = str(hour) + ':' + str(min)
    print(currTime)
    clientWrite('time-' + currTime)

    if hour == 23 and min == 45:

        try:
            os.remove('logs.txt')
            log('logs cleared...\n')
        except:
            log('logs file purge error!')

    if min == 58:
        lib.syncClock()

    for tag in tags:
        schedule = tags[tag]['schedule']
        sched = schedule.split('/')
        for hm in sched:
            start = hm.split(' ')[0]
            startH = int(start.split(':')[0])
            startM = int(start.split(':')[1])
            stop = hm.split(' ')[1]
            stopH = int(stop.split(':')[0])
            stopM = int(stop.split(':')[1])
            if hour == startH and min >= startM and min < stopM:
                if tags[tag]['io'].value() == 1:
                    log('start tag: ' + tags[tag]['name'])
                    tags[tag]['io'].value(0)
                    clientWrite(tags[tag]['name'] + '/0')

            if ((hour == startH) and (min >= stopM)) or ((hour == startH + 1) and (min - stopM < 0)):
                # if hour == startH:
                if tags[tag]['io'].value() == 0:
                    log('stop tag: ' + tags[tag]['name'])
                    # print(type(tag))
                    tags[tag]['io'].value(1)
                    clientWrite(tags[tag]['name'] + '/1')


scheduler()


def clientHandshake(conn, data):
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
            print('client is connected!!!')


# Socket read message decoder
def ClientRead(data):
    opcode_and_fin = data[0]
    msg_len = data[1] - 128
    mask = data[2:6]
    encrypted_msg = data[6: 6+msg_len]
    msg = bytearray([encrypted_msg[i] ^ mask[i % 4]
                     for i in range(msg_len)])
    clientMsg = str(msg, "utf-8")
    log('Incoming message: ' + str(clientMsg))
    return clientMsg


def msgHandler(msg):
    msgTag = ''
    msgAtt = ''
    msgCmd = ''
    result = ''
    message = msg.split('/')
    log(message)
    if len(message) == 1:
        msgTag = message[0]
    if len(message) == 2:
        msgTag = message[0]
        msgAtt = message[1]
    if len(message) == 3:
        msgTag = message[0]
        msgAtt = message[1]
        msgCmd = message[2]

    log(msgTag + '/' + msgAtt + '/' + msgCmd)

    for tag in tags:
        if msgTag != '':
            if tags[tag]['name'] == msgTag:
                if msgCmd == '':
                    # Request received
                    if msgAtt == 'io':
                        result = str(tags[tag][msgAtt].value())
                    else:
                        if msgAtt != '':
                            try:
                                result = str(tags[tag][msgAtt])
                            except:
                                result = 'Invalid attribute...'
                        else:
                            result = 'attribute missing...'
                else:
                    # Command received
                    if type(tags[tag][msgAtt]) is str:
                        tags[tag][msgAtt] = msgCmd
                    else:
                        if msgAtt == 'io':
                            tags[tag][msgAtt].value(int(msgCmd))
                        else:
                            tags[tag][msgAtt] = int(msgCmd)
                    result = 'Command: ' + msgTag + '/' + msgAtt + '/' + msgCmd + ' received!'

    if len(msg) == 0:
        result = 'connected!'
    if result != '':
        log(result)
        clientWrite(result)
    if result == '':
        log('cannot process request or command...')
        clientWrite('cannot process request or command...')


# The communication loop accept either HTTP or WS
print('Starts the comm loop...')
while(1):
    conn, addr = s.accept()
    ws = False
    print('Got a connection from %s' % str(addr))
    while(1):
        data = conn.recv(1024)
        print(data)
        print(len(data))
        if ws == False:
            msg = data.decode()
            print(msg)

        if (len(data) <= 6):
            print('client left...')
            clientWrite('byebye')
            ws = False
            conn.close()
            break

        if 'Sec-WebSocket-Key' in msg:
            clientHandshake(conn, data)
            ws = True

        if ws == False:
            conn.send('Hi!')
            conn.close()
            break
        else:
            msg = ClientRead(data)
            msgHandler(msg)

# Abnormal : Out of communication loop, restart
reset()
