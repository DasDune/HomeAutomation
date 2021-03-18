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


checkUpdate()
