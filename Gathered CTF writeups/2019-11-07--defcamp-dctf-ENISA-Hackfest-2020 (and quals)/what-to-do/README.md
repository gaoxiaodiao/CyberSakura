# what-to-do (50pts, 46 solved) Forensics [Medium]

## First look
We're given a huge zip file, after extracting this, we expect it to be a memory dump.

## Solving
We first try to identify what profile it is: `py -2 .\vol.py -f whatodobun.bin`. We find it's `Win7SP1x64`.  
Now we just look for files with `flag`: `py -2 .\vol.py -f whatodobun.bin --profile=Win7SP1x64 filescan | findstr "flag"` which finds:
```
0x000000007e1f3330     16      0 RW---d \Device\HarddiskVolume2\Users\volf\Downloads\flag.eml
0x000000007e3e5dc0     16      0 R--r-d \Device\HarddiskVolume2\Users\volf\Downloads\flag.eml
0x000000007fac6070     16      0 RW-rwd \Device\HarddiskVolume2\Users\volf\Downloads\flag.eml
```
Let's dump this flag.eml:
```
py -2 .\vol.py -f whatodobun.bin --profile=Win7SP1x64 dumpfiles -Q 0x000000007e3e5dc0 -n -D ./
```
And in the extracted file is our flag, we just need to wrap it in `{}`: `CTF{6b858a61b8074e6a8b0f5ee45bb63c88210922a5ca4c9176d4b7ea2d884ba149}`