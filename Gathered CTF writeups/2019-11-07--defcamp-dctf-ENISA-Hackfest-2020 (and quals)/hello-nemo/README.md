# hello-nemo (50pts, 128 solved) Misc & Forensics [Easy]

## First look
When we open the pcap, we're a bit overwhelmed, by the size of the file and the amount of packets.

## Solving
I just searched for `flag` until I came to a zip file (recognized the magic bytes, `PK..`). We can simply extract this, by:  
`Right click -> Follow -> TCP Stream` or `Cntrl + Alt + Shift + T` and then select `Raw` under `Show and save data as` -> `Save as` -> `flag.zip`.  
When we now open the zip file, we see that it requires a password.  
When we just simply search for `password`, we find `dgyfogfoewyeowyefowouevftowyefg`, which is our password.  
Using the password, we can read the flag: `DCTF{3907879c7744872694209e3ea9d2697508b7a0a464afddb2660de7ed0052d7a7}`