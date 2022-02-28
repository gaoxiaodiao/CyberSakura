#!/usr/bin/env python3

import socket

#Change it!
HOST = '34.89.213.64'
PORT = 30361

count = 0

#connect to host and port
sock = socket.socket()
sock.connect((HOST, PORT))

#There are a total of 3 challenges
while count < 3:
    # receive the response, do a flush out if 'input' string is not showing on the response
    response = sock.recv(4096)
    str_response = repr(response)
    if (str_response.find("Input") == -1):
        flush = sock.recv(4096)

    #Extract the data by finding << and >>
    special1 = str_response.find('<') + 2
    special2 = str_response.find('>')

    if (count == 0):
        # Challenge 1: Decimal to hex
        response_trim = str(hex(int(str_response[special1:special2])))

    elif (count == 1):
        #challenge 2: hex to ascii
        response_trim = bytes.fromhex(str_response[special1:special2]).decode("utf-8")

    elif (count == 2):
        ##challenge 3: octal to ascii
        response_trim = ""
        response_list = str_response[special1:special2].split(' ')
        for i in response_list:
            data = chr(int(i, 8))
            response_trim = response_trim + data

    response_process = response_trim + '\n'
    print(response)
    print(response_trim)
    sock.send(bytes(response_process, 'utf8'))
    count = count + 1

# Receive Flag
response = sock.recv(4096)
print(response)

sock.close()