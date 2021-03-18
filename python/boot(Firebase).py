from machine import reset
import ujson as json
from ntptime import settime
import machine
import ubinascii as binascii
import urequests as requests
import utime
import gc
import network
import webrepl
import esp
import os

# Variables declaration

logs = '\n'
configFile = "config.json"
tagsFile = "tags.json"
serverURL = 'http://us-central1-homeautomation-654d6.cloudfunctions.net/'
IP = ''
PORT = 55
subnet = '255.255.255.0'
gateway = '192.168.1.1'
dns = '8.8.8.8'
ssid = 'Jarinya'
password = '19771977'

# Functions Declaration

# Function Logger


def log(msg):
    global logs
    print(msg)
    logs = logs + msg + '\n'


# Program Start
log('booting...')

gc.collect()
log('Garbage collector activated')

mac = binascii.hexlify(network.WLAN().config('mac'), ':').decode()
log('Controller MAC is: ' + mac)

log('Opening the config file: ' + configFile)

# Check if the config file exist
try:
    # Config file exist proceed with booting
    f = open(configFile, "r")
    t = f.read()
    config = json.loads(t)
    f.close
    IP = config['IP']
    ID = config['ID']
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.ifconfig((IP, subnet, gateway, dns))
    station.connect(ssid, password)
    while station.isconnected() == False:
        pass
    log('Controller connected to the network!')
    webrepl.start()

    try:
        settime()
        log('set time successful!')
    except:
        log('set time failed!!!')

    log('Controller IP: ' + str(station.ifconfig()[0]))
    log('Controller ID: ' + config['ID'])
    log('Allocated Heap: ' + str(gc.mem_alloc()))
    log('Free Heap: ' + str(gc.mem_free()))
    log('Flash ID: ' + str(esp.flash_id()))
    log('Flash Size: ' + str(esp.flash_size()))
    log('Current hour: ' + str(utime.localtime()[3] + 7))
    log('UTC DateTime: ' + str(utime.localtime()))

    print('')
    log('-->Boot complete')

# Config file not found, boot with a dynamic IP
except:
    log('Cannot find the config file: ' + configFile)
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while station.isconnected() == False:
        pass
    IP = station.ifconfig()[0]
    log('The controller is connected! dynamic IP is: ' + IP)
    log('Get the configuration for MAC: [' + mac + '] from DB...')
    r = requests.get(serverURL + 'getNode?MAC=' + mac)
    if r.text != '':
        # The config exist in DB, check IP type
        if r.json()["Type"] == 'Dynamic':
            log('Found MAC in DB, please update the DB with a static IP and a valid controller name to complete the configuration, then reboot...')
        else:
            log('Ok!, configuration completed, ready to create the config file')
            f = open(configFile, "w")
            json.dump(r.json(), f)
            f.close()
            log('Configuration file: ' + configFile +
                ' created for MAC:[' + mac + ']')
            log('Rebooting...')
            reset()
    else:
        # The config info not exist in DB, populate basic info for DB
        log('node info not found for MAC: [' + mac + ']')
        log('populate basic info: MAC: [' +
            mac + '] and IP: [' + IP + '] for DB...')
        payload = {'MAC': mac, 'IP': IP, 'Type': 'Dynamic', 'ID': 'C' + IP[-2]}
        log(payload)
        log(json.dumps(payload))
        headers = {"Content-Type": "application/json"}
        r = requests.post(serverURL + 'setNode',
                          data=json.dumps(payload), headers=headers)
        log('Please update the DB with a static IP and a valid controller name to complete the configuration, then reboot...')
