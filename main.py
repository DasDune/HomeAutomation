

#import os
#from ntptime import settime
#from machine import Timer
from machine import Pin
import usocket as socket
import ubinascii as binascii
import uhashlib as hashlib
import ujson

mainVer = '1.3'
# Change the scheduler to look for a time window to start/stop the load
log('loading main.py ver ' + mainVer + '...')

# Get time when the program starts
min = (utime.localtime()[4])
hour = int((utime.localtime()[3]) + 7)
currTime = str(hour) + ':' + str(min)

# Reading the sprinklers/lights schedule for the outputs tags
try:
    f = open(Schedule, "r")
    t = f.read()
    tags = ujson.loads(t)
    f.close
    log('sprinklers/lights schedule loaded from ' + Schedule + ' file...')
    # Scheduler runs every min.
    log('scheduler started...')
    tim = Timer(-1)
    tim.init(period=60000, mode=Timer.PERIODIC, callback=lambda t: scheduler())

except:
    log('sprinklers/lights schedule loading failed!')

# IO Config
#I0 = Pin(14, Pin.IN)
#I1 = Pin(12, Pin.IN)
#I2 = Pin(13, Pin.IN)
#I3 = Pin(15, Pin.IN)

#O0 = Pin(5, Pin.OUT)
#O1 = Pin(4, Pin.OUT)
#O2 = Pin(0, Pin.OUT)
#O3 = Pin(2, Pin.OUT)

O0 = Pin(16, Pin.OUT)
O1 = Pin(5, Pin.OUT)
O2 = Pin(4, Pin.OUT)
O3 = Pin(14, Pin.OUT)
O4 = Pin(0, Pin.OUT)
O5 = Pin(2, Pin.OUT)

# Use as Outputs indexing with the scheduler
#Outputs = [['O0',O0],['O1',O1],['O2',O2],['O3',O3]]
Outputs = [O0, O1, O2, O3, O4, O5]

# Reset all the outputs on startup
O0.value(1)
O1.value(1)
O2.value(1)
O3.value(1)
O4.value(1)
O5.value(1)
# scheduler routine

# Socket write message encoder


def ClientWrite(msg):
    print('Socket sending message: ' + str(msg))
    frame = [129]
    frame += [len(msg)]
    frame_to_send = bytearray(frame) + msg
    if conn is not None:
        conn.send(frame_to_send)


def scheduler():
    min = (utime.localtime()[4])
    hour = int((utime.localtime()[3]) + 7)

    # Adjust hours between 24-30
    if hour > 23 and hour < 31:
        hour = hour - 24

    currTime = str(hour) + ':' + str(min)
    print(currTime)
    ClientWrite('time-' + currTime)

    if hour == 23 and min == 45:
        try:
            os.remove('logs.txt')
            log('logs cleared...\n')
        except:
            print('logs file purge error!')

    if min == 58:
        try:
            log('syncing ...\n')
            settime()
        except:
            log('syncing error!')

    for tag in tags:
      for start in tags[tag]['Start']:
          # startTime = y
          index = tags[tag]['Start'].index(start)
          stop = tags[tag]['Stop'][index]
          startH = int(start.split(':')[0])
          startM = int(start.split(':')[1])
          stopH = int(stop.split(':')[0])
          stopM = int(stop.split(':')[1])
          
          if (hour == startH) and (min >= startM) and ((min < stopM) or (startH < stopH)):
              if Outputs[tags[tag]['index']].value() == 1:
                  log('start tag: ' + tag)
                  Outputs[tags[tag]['index']].value(0)
                  ClientWrite(tag + '/0')
                  
          if (hour == stopH) and (min >= stopM):
              if Outputs[tags[tag]['index']].value() == 0:
                  log('stop tag: ' + tag)
                  Outputs[tags[tag]['index']].value(1)
                  ClientWrite(tag + '/1')
   
   
# Socket Init.
conn = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP, PORT))
sock.listen(5)
log('socket server listening...')


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


# Inputs handler
def handleInput(p):
    log('Input change detected: ' + str(p) + str(p.value()))
    msg = str(p) + str(p.value())
    ClientWrite(msg)


# Inputs interrupts
# I0.irq(trigger=Pin.IRQ_RISING, handler=handleInput)
# I1.irq(trigger=Pin.IRQ_RISING, handler=handleInput)
# I2.irq(trigger=Pin.IRQ_RISING, handler=handleInput)
# I3.irq(trigger=Pin.IRQ_RISING, handler=handleInput)

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
    msg = 'O4/' + str(O3.value())
    ClientWrite(msg)
    msg = 'O5/' + str(O3.value())
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


scheduler()

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




