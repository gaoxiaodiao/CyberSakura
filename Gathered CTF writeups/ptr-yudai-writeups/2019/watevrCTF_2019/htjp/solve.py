from ptrlib import *
import urllib.parse

def send_request(content):
    sock.send("HTTP/1.1 200 OK\r\n")
    sock.send("Content-Length: {}\r\n".format(len(content)))
    sock.send("Content-Type: text/plain\r\n\r\n")
    sock.send(content)
    #r = re.findall(b"/(.+) HTTP", sock.recvline())
    #return str2bytes(urllib.parse.unquote(bytes2str(r[0])))

target = b"i_store_my_flag_inside_this_file.txt"
c = "1"

key = b'\x1e>\x07\x11\x19\x00\x1eo\x0f\x13l\x05[P\x11l\x05\x17,\x1a\x11\x15:\x06\x01\x06\x01\x00QY3\r\x19C\x08\t'

sock = Socket("13.53.150.215", 50000)
cipher = xor(target, key)
print(send_request(cipher))
print(sock.recv())
sock.interactive()

print(xor(target, key))
