#!/usr/bin/env python3


import socket
import sys
import random

defaultPort = 7989
clientList = {}
IP = None
Port = None
WAITING = 0
SENDING = 1
ACCEPTED = 2
RESENDING = 3
ENDED = 4

if len(sys.argv) == 2:
    IP = sys.argv[1]
    Port = defaultPort
elif len(sys.argv) == 3:
    IP = sys.argv[1]
    Port = sys.argv[2]
else:
    exit(1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((IP, Port))
while True:
    response, addr = s.recvfrom(1024)
    response = response.decode('utf-8').split('\n')
    if response[0] == 'request':
        if response[1] in clientList:
            clientList[response[-1]] = [addr[0], addr[1], response[1], ACCEPTED, str(random.randint(1, 10000))]
            data = 'wait\n' + clientList[response[-1]][4]
            s.sendto(data.encode('utf-8'), addr)
            clientList[response[1]][3] = SENDING
            data = 'send\n' + addr[0] + '\n' + str(addr[1]) + '\n' + clientList[response[1]][4]
            s.sendto(data.encode('utf-8'), (clientList[response[1]][0], clientList[response[1]][1]))
        else:
            clientList[response[-1]] = [addr[0], addr[1], response[1], WAITING, str(random.randint(1, 10000))]
            data = 'wait\n' + clientList[response[-1]][4]
            s.sendto(data.encode('utf-8'), addr)
    elif response[0] == 'done':
        if clientList[response[-1]][3] == SENDING:
            clientList[response[-1]][3] = ENDED
            temp = clientList[response[-1]][2]
            clientList[temp][3] = RESENDING
            data = 'send\n' + addr[0] + '\n' + str(addr[1]) + '\n' + clientList[temp][4]
            s.sendto(data.encode('utf-8'), (clientList[temp][0], clientList[temp][1]))
        elif clientList[response[-1]][3] == RESENDING:
            clientList[response[-1]][3] = ENDED
    elif response[0] == 'success':
        clientList.pop(clientList.pop(response[-1])[2])
