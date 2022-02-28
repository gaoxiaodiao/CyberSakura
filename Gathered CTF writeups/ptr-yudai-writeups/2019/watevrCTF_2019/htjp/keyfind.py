from ptrlib import *
import urllib.parse

def send_request(content):
    sock.send("HTTP/1.1 200 OK\r\n")
    sock.send("Content-Length: {}\r\n".format(len(content)))
    sock.send("Content-Type: text/plain\r\n\r\n")
    sock.send(content)
    r = re.findall(b"/(.+) HTTP", sock.recvline())
    return str2bytes(urllib.parse.unquote(bytes2str(r[0])))

target = b"i_store_my_flag_inside_this_file.txt"
c = "1"

sock = Socket("13.53.150.215", 50000)
key = send_request(c * len(target) + "\r\n")
key = xor(key, c)
print(key)
sock.close()

cipher = target
delta = key

for i in range(50):
    sock = Socket("13.53.150.215", 50000)
    cipher = xor(cipher, delta)
    delta = send_request(cipher)
    print(delta)
    if delta == target: break
    delta = xor(delta, target)
    sock.close()

print(xor(cipher, target))
sock.interactive()
