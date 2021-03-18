#import os
#from ntptime import settime
#from machine import Timer
from machine import Pin
import usocket as socket
import ubinascii as binascii
import uhashlib as hashlib
import ujson as json
import urequests as requests

mainVer = '1.3'
# add messaging feature
log('loading main.py ver ' + mainVer + '...')

# Get time when the program starts
min = (utime.localtime()[4])
hour = int((utime.localtime()[3]) + 7)
currTime = str(hour) + ':' + str(min)

# Reading the sprinklers/lights schedule for the outputs tags
try:
    f = open(Schedule, "r")
    t = f.read()
    tags = json.loads(t)
    f.close
    log('sprinklers/lights schedule loaded from ' + Schedule + ' file...')
    # Scheduler runs every min.
    log('scheduler started...')
    tim = Timer(-1)
    tim.init(period=60000, mode=Timer.PERIODIC, callback=lambda t: scheduler())
except:
    log('sprinklers/lights schedule loading failed!')

# IO Config
I0 = Pin(14, Pin.IN)
I1 = Pin(12, Pin.IN)
I2 = Pin(13, Pin.IN)
I3 = Pin(15, Pin.IN)

O0 = Pin(5, Pin.OUT)
O1 = Pin(4, Pin.OUT)
O2 = Pin(0, Pin.OUT)
O3 = Pin(2, Pin.OUT)

# Use as Outputs indexing with the scheduler
#Outputs = [['O0',O0],['O1',O1],['O2',O2],['O3',O3]]
Outputs = [O0, O1, O2, O3]

# Reset all the outputs on startup
O0.value(1)
O1.value(1)
O2.value(1)
O3.value(1)


# Messaging routine
def messaging(title, message):
    payload = {"notification": {
        "body": "Message",
        "title": "Title"
    },
        "priority": "high",
        "data": {
        "click_action": "FLUTTER_NOTIFICATION_CLICK",
        "id": "1",
        "status": "done"
    },
        "to": "/topics/all"
    }
    payload["notification"]["title"] = title
    payload["notification"]["body"] = message

    headers = {"Content-Type": "application/json",
               "Authorization":
               "key=AAAAf4vX-dY:APA91bHTmNY2TpIbryOBMOtZcbiOxvhg6LRdX9clVd85Du2Vb05jgQK2rUf1X1lbf8VPSKSTLgpReRkIxVn7WDz1jJjrfJ55i4cuIaQn4sz1H-2LXrT-6msNZig7eXPEQ_g19S96hmOK"
               }

    r = requests.post("https://fcm.googleapis.com/fcm/send",
                      data=json.dumps(payload), headers=headers)

# scheduler routine


def scheduler():
    min = (utime.localtime()[4])
    hour = int((utime.localtime()[3]) + 7)

    # Adjust hours between 24-30
    if hour > 23 and hour < 31:
        hour = hour - 24

    currTime = str(hour) + ':' + str(min)
    messaging('Message from C99', currTime)
    ClientWrite('time-' + currTime)
    # messaging()

    if hour == 17 and min == 0:
        try:
            os.remove('logs.txt')
            log('logs cleared...\n')
        except:
            print('logs file purge error!')

    if min == 59:
        try:
            log('syncing ...\n')
            settime()
        except:
            log('syncing error!')

    for x in tags:
        start = (tags[x]['Start'])
        if currTime in start:
            log('Start: ' + x)
            Outputs[tags[x]['index']].value(0)
            ClientWrite(x + '/0')
        stop = (tags[x]['Stop'])
        if currTime in stop:
            log('Stop: ' + x)
            Outputs[tags[x]['index']].value(1)
            ClientWrite(x + '/1')


# Socket Init.
conn = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP, PORT))
sock.listen(5)
#log('socket server listening...')
messaging('Message from C99', 'I just started !!')


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


# Inputs handler
def handleInput(p):
    log('Input change detected: ' + str(p) + str(p.value()))
    msg = str(p) + str(p.value())
    ClientWrite(msg)


# Inputs interrupts
I0.irq(trigger=Pin.IRQ_RISING, handler=handleInput)
I1.irq(trigger=Pin.IRQ_RISING, handler=handleInput)
I2.irq(trigger=Pin.IRQ_RISING, handler=handleInput)
I3.irq(trigger=Pin.IRQ_RISING, handler=handleInput)

# Init the web page IO targets


def initWebTargets():
    log('Sending all IO values to client on new connection...')
    msg = 'O0/' + str(O0.value())
    ClientWrite(msg)
    msg = 'O1/' + str(O1.value())
    ClientWrite(msg)
    msg = 'O2/' + str(O2.value())
    ClientWrite(msg)
    msg = 'O3/' + str(O3.value())
    ClientWrite(msg)
    msg = 'I0/' + str(I0.value())
    ClientWrite(msg)
    msg = 'I1/' + str(I1.value())
    ClientWrite(msg)
    msg = 'I2/' + str(I2.value())
    ClientWrite(msg)
    msg = 'I3/' + str(I3.value())
    ClientWrite(msg)
    ClientWrite('time-' + currTime)

# Handle the received decoded socket message


def HandleData(msg):
    if msg == 'Reset':
        log('Reset request...bye bye...')
        machine.reset()
    else:
        x = msg.split('/')
        # print(x[0])
        # print(type(x[0]))
        # for i in Outputs:
        # if i[0] == x[0]:
        #    out = i[1]
        # print(str(out))

        # print(tags['O0'])
        out = (Outputs[tags[x[0]]['index']])
        #tag = tags[x[0]]
        #out = tag.get('var')
        cmd = int(x[1])
        out.value(cmd)
        log('output: ' + str(x[0]) + ' value: ' + str(x[1]) + ' to controller')
        ClientWrite(msg)

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
            initWebTargets()


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
