from machine import Pin

log('Opening the tags file: ' + tagsFile)

# Functions Declaration

# Function IOConfiguration for the tags


def IOConfig():
    log('Tags IO Config...')

    for tag in tags:
        pinAddress = tags[tag]['PinAddress']
        pinType = tags[tag]['PinType']
        pin = Pin(pinAddress, pinType)
        tags[tag]['pin'] = pin
        log('')
        log(tags[tag]['Name'] + ' configured as:')
        print(pin)
        log(tags[tag]['Name'] + ' schedule is:')
        for s in tags[tag]['Schedule']:
            sched = s.split()
            if sched != []:
                print('Start: ' + sched[0])
                print('Stop: ' + sched[1])

    log('IO Config completed...')

    # DO NOT TRY TO SAVE THE TAGS FILE WITH THE CLASS PIN IT WON'T WORK!!!
    log('Reset all the outputs on startup')
    for tag in tags:
        tags[tag]['pin'].value(1)

# Function scheduler for the lights and sprinklers


def scheduler():
    min = (utime.localtime()[4])
    hour = int((utime.localtime()[3]) + 7)

    # Adjust hours between 24-30
    if hour > 23 and hour < 31:
        hour = hour - 24

    currTime = str(hour) + ':' + str(min)
    log(currTime)
    ClientWrite('time-' + currTime)

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

    for tag in tags:
        start = (tags[tag]['Schedule'][0])
        if currTime in start:
            log('Starting: ' + tags[tag]['Name'])
            tags[tag][pin].value(0)
            #ClientWrite(x + '/0')
        stop = (tags[tag]['Schedule'][1])
        if currTime in stop:
            log('Stopping: ' + tags[tag]['Name'])
            tags[tag][pin].value(1)
            #ClientWrite(x + '/1')


# Main program starts here
try:
    f = open(tagsFile, "r")
    t = f.read()
    tags = json.loads(t)
    f.close
# Program normal flow
    IOConfig()

# Tags file not found, get tags info from DB
except:
    log('Cannot find the tags file: ' + tagsFile)
    log('Getting tags from DB...')
    try:
        r = requests.get(serverURL + 'getNodeTags?node=' + ID)
        t = r.json()
        tags = {}
        f = open(tagsFile, "w")
        print('Tags from DB:')
        for x in t:
            for h in list(x):
                if h != 'Name' and h != 'PinAddress' and h != 'PinType' and h != 'Schedule':
                    x.pop(h)
            print(x)
            tags[x['Name']] = x
        f.write(json.dumps(tags))
        f.close()
        IOConfig()

    except:
        log('Tags not found in DB...Please configure tags for this controller')
