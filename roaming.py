#Roaming : chosen the nearest SSID base on its gain

from ntptime import settime
from machine import Timer
import utime
import gc
import network
import webrepl
import esp
import os

station = network.WLAN(network.STA_IF)
#sta_if = network.WLAN(network.STA_IF)
station.active(True)
nets = station.scan()

ssid = ""
Gain = -99
passw = ""
Jpassw = "19771977"
Dpassw = "Benoit666"

print("SSID Scan...")
for net in nets:
    print("find AP: " + net[0].decode())
    if net[0].decode().find("DasNet") != -1:
      print("found SSID DasNet, gain : " + str(net[3]))
      if net[3] > Gain:
        Gain = net[3]
        ssid = net[0].decode()
        passw = Dpassw
    
    if net[0].decode().find("Jarinya") != -1:
      print("SSID Jarinya, gain : " + str(net[3]))
      if net[3] > Gain:
        Gain = net[3] 
        ssid = net[0].decode()
        passw = Jpassw

print("connecting to " + ssid + "..." )

station.connect(ssid, passw)

while station.isconnected() == False:
    pass
print('Controller connected to the network!')
print('Controller IP: ' + str(station.ifconfig()[0]))

