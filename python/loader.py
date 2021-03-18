import json
import requests
import os


def readConfig():
    try:
        print('Reading the minimum config file...')
        f = open('config.json', "r")
        cfg = f.read()
        config = json.loads(cfg)
        f.close
        # print('Config ver. : ' + config['ver'])
        return config
    except:
        print('Minimum config file not found...')


def connect():
    try:
        config = readConfig()
        print('Connecting to SSID: ' +
              config['ssid'] + ' with password: ' + config['password'] + ' ...')
        print('Connected with a dynamic IP.')
    except:
        print('Cannot connect to the network...')


def loadFile(fileName):
    f = open('config.json', "r")
    cfg = f.read()
    config = json.loads(cfg)
    f.close
    filesURL = config['filesURL']
    token = config['token']
    URL = filesURL + fileName + '?alt=media&token=' + token
    r = requests.get(URL)
    f = open(fileName, "w")
    f.write(r.text)
    f.close()
    print(fileName + ' downloaded!')


def popTags():
    f = open('config.json', "r")
    cfg = f.read()
    config = json.loads(cfg)
    f.close
    ID = config['ID']
    dbURL = config['dbURL']
    tagsFile = config['tagsFile']
    print('Getting the tags from DB for controller: ' + ID + ' ...')
    r = requests.get(dbURL + 'getNodeTags?node=' + ID)
    if len(r.text) > 2:
        print('tags are: ')
        t = r.json()
        tags = {}
        for x in t:
            tags.update(
                {x['Name']: {'name': x['Name'], 'pin': x['PinNo'], 'type': x['PinType']}})
        print(tags)
        print('Saving tags to: ' + tagsFile)
        f = open(tagsFile, "w")
        json.dump(tags, f)
        f.close()
    else:
        print('tags not found in DB...')


def updateConfig():
    config = readConfig()
    print('DB server location : ' + config['dbURL'])
    print('Get the latest config online...')

    try:
        r = requests.get(config['dbURL'] +
                         'getNode?MAC=' + 'ec:fa:bc:63:12:d0')
        cfg = r.json()
        print('Controller ID is: ' + cfg['ID'])
        print('Controller IP is: ' + cfg['IP'])

    except:
        print('Cannot get the latest config online...')

    print('Get the system info online...')
    print('...')
    try:
        r = requests.get(config['dbURL'] +
                         'sysInfo')
        sys = r.json()
        print('*System version: ' + sys['ver'])
        print('*DB server location: ' + sys['dbURL'])
        print('*Files server location: ' + sys['filesURL'])
        print('*Config File: ' + sys['configFile'])
        print('*Tags File: ' + sys['tagsFile'])
        print('*SubNet: ' + sys['subnet'])
        print('*G/W: ' + sys['gw'])
        print('*DNS: ' + sys['dns'])
        print('...')

        print('Updating the config file...')
        sys.update(cfg)
        f = open('config.json', "w")
        json.dump(sys, f)
        f.close()
        # print('Rebooting with IP: ' + cfg['IP'] + '...')

    except:
        print('Cannot get the system info online...')


def checkUpdate():
    config = readConfig()
    dbURL = config['dbURL']
    ver = config['ver']
    print('Current version: ' + ver)

    try:
        r = requests.get(config['dbURL'] +
                         'sysInfo')
        sys = r.json()
        onlineVer = sys['ver']
        print('Online version: ' + onlineVer)
        if (ver != onlineVer):
            print('Updating controller...')
            update = sys['update']
            if 'config' in update:
                print('update config...')
            if 'boot' in update:
                print('update boot.py...')
            if 'main' in update:
                print('update main.py...')
            if config['ID'] in update:
                print('update tags...')
    except:
        print('Cannot get the system info online...')
