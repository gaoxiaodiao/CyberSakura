# posts (110pts, 40 solved) Misc & OSINT [Medium]

## First look
When we open the pdf, we get some meaningless messages. I tried to select everything and check it in a text editor, but nothing special.

## Solving
When we Google one of those places, such as `Kruglyy Prud`, we see that it represents a `D`. We can do this for all the remaining ones and construct the flag:
```
Kruglyy Prud																D
Communs																		C
3015 E Evergreen Blvd, Vancouver, WA 98661, USA								T
1299-1261 N Kelham Ave Oklahoma City, OK 73117								F
Pintor Solana																U
Kruglyy Prud																D
700 W Overland Rd, Meridian, ID, USA Towers at Kuhio Park Apartments		I
Towers at Kuhio Park Apartments												Y
Pintor Solana																U
2524 Humboldt Ave S Minneapolis, MN 55405									3
1399-1301 25th 1/2 St W, Minneapolis, MN 55405, USA							7
China CITIC Bank 24-hour Self-service Bank at Cross Region Plaza			O
Libration Systems Managemen													G
M74X+H7 Taastrup, Høje-Taastrup Municipality, Denmark						8
2524 Humboldt Ave S Minneapolis,MN 55405									3
1399-1301 25th 1/2 St W, Minneapolis, MN 55405, USA							7
สาํ นักงานอัยการสูงสุด อาคารหลักเมือง / Wat Buranasiri Mattayaram                  A
Kruglyy Prud																D
Communs																		C
3015 E Evergreen Blvd, Vancouver, WA 98661, USA								T
1299-1261 N Kelham Ave Oklahoma City, OK 73117								F
```
_Note for `Pintor Solana` I used OpenStreetMap, since Google maps didn't have it_
Concatinating everything: `DCTFUDIYU37OG837ADCTF`.