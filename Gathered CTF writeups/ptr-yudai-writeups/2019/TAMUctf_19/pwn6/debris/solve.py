from ptrlib import *

def send_data(size, data, i):
    payload = p32(size)
    payload += p32(i)
    payload += data
    sock.send(payload)
    print(payload)
    return sock.recv()

def send_login(username, password):
    payload = bytes([len(username)])
    payload += bytes([len(password)])
    payload += username
    payload += password
    return send_data(len(payload), payload, 0)

def send_create_account(number):
    payload = p32(number)
    return send_data(4, payload, 2)
    #return send_data(6, payload, 2)

def send_create_user(username, password, priv, email, name, qnum, answer):
    payload = bytes([len(username)])
    payload += bytes([len(password)])
    payload += bytes([priv])
    payload += bytes([len(email)])
    payload += bytes([len(name)])
    payload += bytes([len(answer)])
    payload += bytes([qnum])
    payload += username
    payload += password
    payload += email
    payload += name
    payload += answer
    return send_data(len(payload), payload, 0x61)

def send_check_deposit(number):
    payload = p32(number)
    return send_data(4, payload, 1)

#sock = Socket("172.30.0.2", 6210)
sock = Socket("127.0.0.1", 6210)

result = send_create_account(1234)
result = send_create_user(b"1234", b"pass123", 1, b"taro@yopmail.com", b"Taro", 1, b"red")
result = send_login(b"1337", b"Secur1ty")
result = send_check_deposit(1337)
print(result)
