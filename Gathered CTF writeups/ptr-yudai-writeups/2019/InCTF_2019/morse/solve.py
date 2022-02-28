from scapy.all import *

flag = ''
def analyse(pkt):
    global flag
    payload = bytes(pkt)[4:]
    if payload[0] != 0x01: return
    if payload[1] != 0x0e: return
    try:
        if payload[8] == 0x52: # Write Command
            flag += '.' if payload[-1] == 1 else '-'
        elif payload[8] == 0x12: # Write Request
            flag += ' '
    except:
        return

sniff(offline="Challenge.pcap", store=0, prn=analyse)
print(flag)
