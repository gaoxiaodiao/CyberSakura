# Memory (forensics 100)

###ENG
[PL](#pl-version)

In the task we get a memdump (quite large so we won't add it here).
We proceed with the analysis using volatility.

If we check connections we can see that there is only one:

```
$ ./volatility-2.5.standalone.exe connections -f forensic_100.raw
Volatility Foundation Volatility Framework 2.5
Offset(V)  Local Address             Remote Address            Pid
---------- ------------------------- ------------------------- ---
0x8213bbe8 192.168.88.131:1034       153.127.200.178:80        1080
```

No we can still play with volatility or we can just check this IP directly in the memdump strings and we can find:

```
# Copyright (c) 1993-1999 Microsoft Corp.
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
# For example:
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host
127.0.0.1       localhost
153.127.200.178    crattack.tistory.com 
```

So it seems someone added this IP manually for host `crattack.tistory.com`.

If we now look for the host `crattack.tistory.com` we can find:


```
C:\Program Files\Internet Explorer\iexplore.exe http://crattack.tistory.com/entry/Data-Science-import-pandas-as-pd
```

This matches what we've seen - someone was accessing this IP on port 80, so it was IE.
But this IP does not match the actual IP of this host.
So we check what did the user see under `http://crattack.tistory.com/entry/Data-Science-import-pandas-as-pd` -> `http://153.127.200.178/entry/Data-Science-import-pandas-as-pd` and it turnes out to be the flag:

`SECCON{_h3110_w3_h4ve_fun_w4rg4m3_}`

###PL version

W zadaniu dostajemy memdump (du??y wi??c go nie wrzucamy).
Rozpoczynamy analiz?? z volatility.

Je??li sprawdzimy po????czenia to widzimy tylko jedno:

```
$ ./volatility-2.5.standalone.exe connections -f forensic_100.raw
Volatility Foundation Volatility Framework 2.5
Offset(V)  Local Address             Remote Address            Pid
---------- ------------------------- ------------------------- ---
0x8213bbe8 192.168.88.131:1034       153.127.200.178:80        1080
```

Mogliby??my dalej bawi?? si?? z volatility ale szybciej b??dzie poszuka?? tego IP w stringach z memdumpa:

```
# Copyright (c) 1993-1999 Microsoft Corp.
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
# For example:
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host
127.0.0.1       localhost
153.127.200.178    crattack.tistory.com 
```

Jak wida?? kto?? r??cznie doda?? ten IP dla hosta `crattack.tistory.com`.

Je??li teraz poszukamy hosta `crattack.tistory.com` znajdziemy:

```
C:\Program Files\Internet Explorer\iexplore.exe http://crattack.tistory.com/entry/Data-Science-import-pandas-as-pd
```

Co pasuje do tego co obserwowali??my - kto?? ????czy?? si?? z tym adresem na porcie 80, wi??c by??o to IE.
Ale ten IP nie pasuje do faktycznego adresu tego hosta.
Sprawwd??my wi??c co u??ytkownik widzia?? pod `http://crattack.tistory.com/entry/Data-Science-import-pandas-as-pd` -> `http://153.127.200.178/entry/Data-Science-import-pandas-as-pd` a okazuje si?? to by?? flag??:

`SECCON{_h3110_w3_h4ve_fun_w4rg4m3_}`
