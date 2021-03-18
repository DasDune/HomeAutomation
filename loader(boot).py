
# First initialization
import webrepl_setup
from machine import reset
import ubinascii as binascii
import network
import lib
import webrepl

# Connect with a dynamic IP
lib.connect('dynamic', 'Jarinya', '19771977')

webrepl.start()

mac = binascii.hexlify(network.WLAN().config('mac'), ':').decode()
print('Controller MAC is: ' + mac)

# Cloud update config file for this MAC
lib.updateConfig(mac)

# Cloud populate tags
lib.popTags()

# Only need to set the networking once

# Station Config : Connect to the nearest AP
lib.roaming()

# AP Config
lib.setAP()

#import webrepl_setup

# Download the production boot.py and main.py files
print('Downloading boot.py...')
lib.loadFile('boot.py')
print('Downloading main.py...')
lib.loadFile('main.py')


reset()

# loadFile('main.py')
