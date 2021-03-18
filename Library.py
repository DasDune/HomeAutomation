import json
import requests
# init logs
logs = ''


def log(msg):
    global logs
    print(msg)
    try:
        logs = logs + msg + '\n'
        # log(len(logs))
    except:
        print('logging failed! exceeding logs var size...')
        print('save logs to logs.txt and reset logs variable')
        logs
        f = open("logs.txt", "a")
        f.write(logs)
        f.close
        logs = ''


def readConfig():
    try:
        log('Reading config file...')
        f = open('config.json', "r")
        cfg = f.read()
        config = json.loads(cfg)
        # log(config)
        f.close
        # log('Config ver. : ' + config['ver'])
        return config
    except:
        log('config file not found...')


def updateConfig(mac):
    config = readConfig()
    log('DB server location : ' + config['dbURL'])
    log('Get the latest config online...')

    try:
        r = requests.get(config['dbURL'] +
                         'getNode?MAC=' + mac)
        cfg = r.json()
        log('Controller ID is: ' + cfg['ID'])
        log('Controller IP is: ' + cfg['IP'])

    except:
        log('Cannot get the latest config online...')

    log('Get the system info online...')
    log('...')
    try:
        r = requests.get(config['dbURL'] +
                         'sysInfo')
        sys = r.json()
        log('*System version: ' + sys['ver'])
        log('*DB server location: ' + sys['dbURL'])
        log('*Files server location: ' + sys['filesURL'])
        log('*Config File: ' + sys['configFile'])
        log('*Tags File: ' + sys['tagsFile'])
        log('*SubNet: ' + sys['subnet'])

        log('*G/W: ' + sys['gw'])
        log('*DNS: ' + sys['dns'])
        log('...')

        log('Updating the config file...')
        sys.update(cfg)
        f = open('config.json', "w")
        json.dump(sys, f)
        f.close()

    except:
        log('Cannot get the system info online...')


def popTags():
    config = readConfig()
    ID = config['ID']
    dbURL = config['dbURL']
    tagsFile = config['tagsFile']
    log('Getting the tags from DB for controller: ' + ID + ' ...')
    r = requests.get(dbURL + 'getNodeTags?node=' + ID)
    if len(r.text) > 2:
        log('tags are: ')
        t = r.json()
        tags = {}
        for x in t:
            tags.update(
                {x['Name']: {'name': x['Name'], 'pin': x['PinNo'], 'type': x['PinType'], 'schedule': x['Schedule']}})
        log(tags)
        log('Saving tags to: ' + tagsFile)
        f = open(tagsFile, "w")
        json.dump(tags, f)
        f.close()
    else:
        log('tags not found in DB...')


def loadFile(fileName):
    config = readConfig()
    filesURL = config['filesURL']

    if fileName == 'boot.py':
        token = config['btoken']
    if fileName == 'main.py':
        token = config['mtoken']
    URL = filesURL + fileName + '?alt=media&token=' + token
    r = requests.get(URL)
    f = open(fileName, "w")
    f.write(r.text)
    f.close()
    log(fileName + ' downloaded!')


def checkUpdate():
    log('checking for update...')
    config = readConfig()
    dbURL = config['dbURL']
    ver = config['ver']
    log('Current version: ' + ver)
    updateFlag = False

    try:
        r = requests.get(config['dbURL'] +
                         'sysInfo')
        sys = r.json()
        onlineVer = sys['ver']
        log('Online version: ' + onlineVer)
        if (ver != onlineVer):
            log('Updating controller...')
            updateFlag = True
            update = sys['update']
            if 'config' in update:
                log('update config...')
                updateConfig()
            if 'boot' in update:
                log('update boot.py...')
                loadFile('boot.py')
            if 'main' in update:
                log('update main.py...')
                loadFile('main.py')
            if config['ID'] in update:
                log('update tags...')
                popTags()
        else:
            log('The controller is up to date')
    except:
        log('Cannot get the system info online...')
    return updateFlag


mac = '84:f3:eb:53:23:37'

# updateConfig(mac)

checkUpdate()


# f = open('config.json', "r")
# cfg = f.read()

# y = json.loads(cfg)

# print(y)
