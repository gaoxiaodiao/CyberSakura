# investigator (370pts, 14 solved) Forensics, Misc & Mobile [Easy]

## First look
When we open the given `PCAP`, we can see a lot of traffic. When we look through it a bit and search for some strings, we see some recognisable words such as `WRTE`, `OKAY` and `CLSE`. This is android `ADB` traffic. We also find some `APK` file based on our string search. Our goal is clear, extract the `APK` file.

## Solving
Wireshark is able to decode `ADB` traffic so let's enable that by right clicking on an `ADB` packet -> `Decode as` -> and select `ADB` under `Current`. We can also extract the whole `TCP` stream and save it as raw data under `data.dat`. Now we have to parse the `ADB` protocol, because in this `TCP` stream, is our `APK` file which we want, but it also has these `ADB` data strings. We can simply implement this in python with the help of Wireshark to understand the protocol:
```python
import struct

with open("data.dat", "rb") as f:
    data = f.read()

idx = 0
result = b""
while idx < len(data):
    if data[idx:idx+4]==b"WRTE" and data[idx+20: idx+24] == b"\xa8\xad\xab\xba":
        length = struct.unpack("<I", data[idx+12:idx+16])[0]
        arg0 = struct.unpack("<I", data[idx+4:idx+8])[0]
        arg1 = struct.unpack("<I", data[idx+8:idx+12])[0]

        #arg0 and arg1 kind of specify the stream, there are 2 APK's being send.
        if (arg0 == 5 or arg1 == 0x41) and length > 20: #skip small packets
            result += data[idx+24:idx+24+length]
            idx += length + 24
    idx += 1

result = result.replace(b"\x44\x41\x54\x41\x00\x00\x01\x00", b"") #DATA00000100

with open("data_extracted.zip", "wb") as f:
    f.write(result)
```
Now we need to extract the `classes.dex` file and open it up in a decompiler such as `JADX`.  
In the `MainActivity` we find the following:
```
this.t = 64524587;
this.t = -1944971157;
this.t = 344623675;
this.t = 1581367861;
this.t = 1760960267;
this.t = 118873725;
this.t = -1122776688;
this.t = 415595399;
this.t = 641466125;
this.t = 1293651411;
this.t = 1200513448;
this.t = 1396114426;
this.t = -215204352;
this.t = 2031384093;
this.t = 1287151886;
this.t = 28223930;
this.t = -1716313687;
this.t = -567086190;
this.t = -1684197569;
this.t = -310036409;
this.t = 238086082;
this.t = 210160122;
this.t = 1886362847;
this.t = 1489026485;
this.t = -238661515;
this.t = -255017515;
this.t = 856637508;
this.t = 615302507;
this.t = 120912101;
this.t = -1681563310;
this.t = 1094395449;
this.t = 1726311212;
this.t = 145339813;
this.t = -2008579287;
this.t = 828431677;
this.t = 917791728;
this.t = -1003250922;
this.t = -971565278;
this.t = -770806142;
this.t = -560309836;
this.t = -149703106;
this.t = -835322980;
this.t = 1490909382;
this.t = 210601382;
this.t = 137534656;
this.t = -2028860249;
this.t = -966032419;
this.t = -326066318;
this.t = -265220027;
this.t = -1497681174;
this.t = 1444480349;
this.t = -714729064;
this.t = -698107094;
this.t = 426954206;
this.t = -1693479248;
this.t = 1512113707;
this.t = -1695715744;
this.t = 2055250696;
this.t = 1530345934;
this.t = 1904972563;
this.t = 1908303526;
this.t = -1919964477;
this.t = 2016652512;
this.t = 1914244748;
this.t = -1930350542;
this.t = 883221276;
this.t = -860164922;
this.t = 861974181;
this.t = 1427484873;
this.t = -97567084;
return new String(new byte[] {
    (byte)(this.t >>> 6), (byte)(this.t >>> 11), (byte)(this.t >>> 13), (byte)(this.t >>> 3), (byte)(this.t >>> 17), (byte)(this.t >>> 21), (byte)(this.t >>> 3), (byte)(this.t >>> 22), (byte)(this.t >>> 21), (byte)(this.t >>> 22), (byte)(this.t >>> 14), (byte)(this.t >>> 19), (byte)(this.t >>> 20), (byte)(this.t >>> 4), (byte)(this.t >>> 8), (byte)(this.t >>> 3), (byte)(this.t >>> 19), (byte)(this.t >>> 4), (byte)(this.t >>> 23), (byte)(this.t >>> 18), (byte)(this.t >>> 16), (byte)(this.t >>> 9), (byte)(this.t >>> 17), (byte)(this.t >>> 22), (byte)(this.t >>> 19), (byte)(this.t >>> 18), (byte)(this.t >>> 23), (byte)(this.t >>> 13), (byte)(this.t >>> 21), (byte)(this.t >>> 8), (byte)(this.t >>> 5), (byte)(this.t >>> 3), (byte)(this.t >>> 11), (byte)(this.t >>> 4), (byte)(this.t >>> 24), (byte)(this.t >>> 9), (byte)(this.t >>> 3), (byte)(this.t >>> 21), (byte)(this.t >>> 14), (byte)(this.t >>> 6), (byte)(this.t >>> 4), (byte)(this.t >>> 16), (byte)(this.t >>> 1), (byte)(this.t >>> 10), (byte)(this.t >>> 2), (byte)(this.t >>> 5), (byte)(this.t >>> 20), (byte)(this.t >>> 21), (byte)(this.t >>> 16), (byte)(this.t >>> 8), (byte)(this.t >>> 20), (byte)(this.t >>> 12), (byte)(this.t >>> 20), (byte)(this.t >>> 22), (byte)(this.t >>> 23), (byte)(this.t >>> 4), (byte)(this.t >>> 23), (byte)(this.t >>> 3), (byte)(this.t >>> 16), (byte)(this.t >>> 4), (byte)(this.t >>> 9), (byte)(this.t >>> 18), (byte)(this.t >>> 16), (byte)(this.t >>> 15), (byte)(this.t >>> 8), (byte)(this.t >>> 4), (byte)(this.t >>> 22), (byte)(this.t >>> 23), (byte)(this.t >>> 2), (byte)(this.t >>> 7)
});
```
This is probably our flag, so let's contruct it, it's clear what to do:
```python
import re

input = """
this.t = 64524587;
this.t = -1944971157;
...
return new String(new byte[] {
    (byte)(this.t >>> 6), (byte)(this.t >>> 11), (byte)(this.t >>> 13), (byte)(this.t >>> 3), (byte)(this.t >>> 17), (byte)(this.t >>> 21), (byte)(this.t >>> 3), (byte)(this.t >>> 22), (byte)(this.t >>> 21), (byte)(this.t >>> 22), (byte)(this.t >>> 14), (byte)(this.t >>> 19), (byte)(this.t >>> 20), (byte)(this.t >>> 4), (byte)(this.t >>> 8), (byte)(this.t >>> 3), (byte)(this.t >>> 19), (byte)(this.t >>> 4), (byte)(this.t >>> 23), (byte)(this.t >>> 18), (byte)(this.t >>> 16), (byte)(this.t >>> 9), (byte)(this.t >>> 17), (byte)(this.t >>> 22), (byte)(this.t >>> 19), (byte)(this.t >>> 18), (byte)(this.t >>> 23), (byte)(this.t >>> 13), (byte)(this.t >>> 21), (byte)(this.t >>> 8), (byte)(this.t >>> 5), (byte)(this.t >>> 3), (byte)(this.t >>> 11), (byte)(this.t >>> 4), (byte)(this.t >>> 24), (byte)(this.t >>> 9), (byte)(this.t >>> 3), (byte)(this.t >>> 21), (byte)(this.t >>> 14), (byte)(this.t >>> 6), (byte)(this.t >>> 4), (byte)(this.t >>> 16), (byte)(this.t >>> 1), (byte)(this.t >>> 10), (byte)(this.t >>> 2), (byte)(this.t >>> 5), (byte)(this.t >>> 20), (byte)(this.t >>> 21), (byte)(this.t >>> 16), (byte)(this.t >>> 8), (byte)(this.t >>> 20), (byte)(this.t >>> 12), (byte)(this.t >>> 20), (byte)(this.t >>> 22), (byte)(this.t >>> 23), (byte)(this.t >>> 4), (byte)(this.t >>> 23), (byte)(this.t >>> 3), (byte)(this.t >>> 16), (byte)(this.t >>> 4), (byte)(this.t >>> 9), (byte)(this.t >>> 18), (byte)(this.t >>> 16), (byte)(this.t >>> 15), (byte)(this.t >>> 8), (byte)(this.t >>> 4), (byte)(this.t >>> 22), (byte)(this.t >>> 23), (byte)(this.t >>> 2), (byte)(this.t >>> 7)
});
"""
res = ""
matches = re.findall(r"\(byte\) \(this\.t >>> (\d+)\)", input)
for idx, match in enumerate(re.findall(r"this\.t = ((?:-)?\d+)", input)):
    t = int(match)
    res += chr((t >> int(matches[idx])) & 0xff)
print(res)
```
Which gets us the flag: `DCTF{82c149f2aa7697a0d7c83ff9a1e6211b09fc5ca0efd12aafe6b5a713c32012f2}`