from ntptime import settime
from machine import Timer
import utime
import gc
import network
import webrepl
import esp
import os

# Only update the two lines below
bootVer = '1.1'
ID = '103'

# init logs
logs = '\n'


def log(msg):
    global logs
    print(msg)
    try:
        logs = logs + msg + '\n'
        # print(len(logs))
    except:
        print('logging failed! exceeding logs var size...')
        clearLogs()


log('booting with boot.py ver ' + bootVer + '...')

Controller = "C" + ID
IP = '192.168.1.' + ID
Schedule = Controller + "Sched" + ".json"
PORT = 8080
##


# Clear the logs when the variable each its lenght limit and save to a file.

def clearLogs():
    print('save logs to logs.txt and reset logs variable')
    global logs
    f = open("logs.txt", "a")
    f.write(logs)
    f.close
    logs = ''


log('Welcome to controller: ' + Controller)
log('Scheduler file is: ' + Schedule)
log('Configured IP is: ' + IP)
log('Configured socket Port is: ' + str(PORT))

gc.collect()
log('Garbage collector activated')

ssid = 'Jarinya'
password = '19771977'

station = network.WLAN(network.STA_IF)

station.active(True)

station.connect(ssid, password)

while station.isconnected() == False:
    pass

webrepl.start()

try:
    settime()
    log('set time successful!')
except:
    log('set time failed!!!')

log('Connection successful')
log('Controller IP: ' + str(station.ifconfig()[0]))
log('Allocated Heap: ' + str(gc.mem_alloc()))
log('Free Heap: ' + str(gc.mem_free()))
log('Flash ID: ' + str(esp.flash_id()))
log('Flash Size: ' + str(esp.flash_size()))
log('Current hour: ' + str(utime.localtime()[3] + 7))
log('UTC DateTime: ' + str(utime.localtime()))

day = str((utime.localtime()[2]))
hour = str(int((utime.localtime()[3]) + 7))
min = str((utime.localtime()[4]))

log('-->Boot completed at day:' + day + ' hour:' + hour + ' min:' + min)
