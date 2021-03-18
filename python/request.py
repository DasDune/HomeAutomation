import requests
import json

node = {'MAC': 'dc:4f:22:7e:38:de', 'IP': '192.168.1.10'}
data = {'name': 'Tag99', 'description': 'This is Tag99'}

# print(type(node))

# r = requests.post('http://us-central1-homeautomation-654d6.cloudfunctions.net/setNode', data=node)

r = requests.get(
    'http://us-central1-homeautomation-654d6.cloudfunctions.net/getNodeTags?node=C115')

# r = requests.post('https://httpbin.org/post', data=payload)

# print(r.text)
# print(r.text)
# y = r.text
# print(type(tagss))
tags = r.json()
# print(t)
#tags = {}
# Nice code to filter a dictionnary!
for x in tags:
    # y = json.dumps(x)
    # print(list(x)[0])
    for h in list(x):
        if h != 'Pin' and h != 'name' and h != 'Schedule':
            x.pop(h)
    # print(x)
    # print(x['Pin'])
    # print(x['name'])

for tag in tags:
    print('Schedule for: ' + tag['name'])
    for s in tag['Schedule']:
        sched = s.split()
        # print(sched)
        if sched != []:
            print('Start: ' + sched[0])
            print('Stop: ' + sched[1])
# print(type(tags))


# tags = []
# for x in t:
#   tags.append(['tag:' + x['name'], 'Pin:' + x['Pin']])
# tags.append(x['Pin'])
# print(tags)
# print(tags)
# tags = json.dumps(tags)
# print(tags)
