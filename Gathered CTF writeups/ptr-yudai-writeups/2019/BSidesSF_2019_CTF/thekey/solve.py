from scapy.all import *

result = b' '
last = 0
interval = True

def keyid2chr(keyid, shift):
    table = {}
    for i in range(26):
        table[0x04 + i] = (bytes([ord("a") + i]), bytes([ord("A") + i]))
    syms = [b"!", b"@", b"#", b"$", b"%", b"^", b"&", b"*", b"("]
    for i in range(9):
        table[0x1e + i] = (bytes([ord("1") + i]), syms[i])
    table[0x27] = (b'0', b')')
    table[0x28] = (b'\n', b'\n')
    table[0x29] = (b'[ESC]', b'[ESC]')
    syms1 = b"\t -=[]\\#;' ,./"
    syms2 = b"\t _+{}|~:\" <>?"
    for i, (a, b) in enumerate(zip(syms1, syms2)):
        table[0x2b + i] = (bytes([a]), bytes([b]))
    if keyid in table:
        return table[keyid][shift]
    else:
        print(keyid)
        return b'?'

def analyse(pkt):
    global result, interval, last
    payload = bytes(pkt[Raw].load)
    leftover = payload[0x40:]
    if payload[8] == ord('S') and payload[9] == 1:
        # submit
        pass
    elif payload[8] == ord('C') and payload[9] == 1 and len(leftover) == 8:
        # complete
        shift = leftover[0]
        keyid = leftover[2]
        if keyid == 0:
            interval = True
        else:
            # an event captured
            c = keyid2chr(keyid, shift==0x20)
            if last == keyid and not interval:
                return
            result += c
            last = keyid
            interval = False

sniff(offline="thekey.pcapng", filter="", store=0, prn=analyse)
print(result)
