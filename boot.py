import lib
import gc
import network

gc.collect()
lib.log('Garbage collector activated')

# Sync Clock
lib.syncClock()

# check for update
#config = lib.readConfig()
updateFlag = False
updateFlag = lib.checkUpdate()

# configure as a station
# connect to the nearest AP
if updateFlag:
    lib.roaming()
    lib.setAP()

# configure as an access point
# lib.setAP()
