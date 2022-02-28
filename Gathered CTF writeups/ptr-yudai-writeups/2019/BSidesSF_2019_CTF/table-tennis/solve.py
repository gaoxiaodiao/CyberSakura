from scapy.all import *

result = b''

def analyse(pkt):
    global result
    if pkt[IP].src == "192.168.10.212":
        data = bytes(pkt[ICMP].payload)
        result += data[16:24]

sniff(offline="out.pcapng", filter="icmp", store=0, prn=analyse)
print(result)
