from scapy.all import *

def modify(pkt):
    if pkt[IP].dst == '172.30.0.2' and pkt[TCP].dport == 5005:
        pkt

sniff(filter='tcp', prn=modify)
