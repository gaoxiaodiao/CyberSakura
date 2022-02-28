from scapy.all import *
from datetime import datetime

def analyse(pkt):
    if pkt[TCP].dport == 4445 and pkt[TCP].payload:
        print(pkt[TCP].payload)

sniff(offline="log2.pcapng", filter="tcp", store=0, prn=analyse)
