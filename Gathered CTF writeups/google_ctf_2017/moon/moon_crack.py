#!/usr/bin/env python2
# --------------------------------------------------------------------------------------------------
# Google CTF 2017 - Moon (RE 500)
# --------------------------------------------------------------------------------------------------
import math

hash_str =  '30c7ead97107775969be4ba00cf5578f1048ab1375113631dbb6871dbe35162b' +\
            '1c62e982eb6a7512f3274743fb2e55c818912779ef7a34169a838666ff3994bb' +\
            '4d3c6e14ba2d732f14414f2c1cb5d3844935aebbbe3fb206343a004e18a092da' +\
            'ba02e3c0969871548ed2c372eb68d1af41152cb3b61f300e3c1a8246108010d2' +\
            '82e16df8ae7bff6cb6314d4ad38b5f9779ef23208efe3e1b699700429eae1fa9' +\
            '3c036e5dcbe87d32be1ecfac2452ddfdc704a00ea24fbc2161b7824a968e9da1' +\
            'db756712be3e7b3d3420c8f33c37dba42072a941d799ba2eebbf86191cb59aa4' +\
            '9a80ebe0b61a79741888cb62341259f62848aad44df2b809383e09437928980f'

# --------------------------------------------------------------------------------------------------
def alpha_crack( h ):
    # because some loses from from rounding, we brute for the character instead applying acos()
    for p in range(128):
        if int(1024*math.cos(math.radians(p)) + 2048) == h:
            return p

    return 0

# --------------------------------------------------------------------------------------------------
def beta_crack( h ):
    for p in range(128):
        if int(1024*math.sin(math.radians(p)) + 2048) == h:
            return p

    return 0

# --------------------------------------------------------------------------------------------------
def calc_h( password ):
    h = 0x5a

    for i in range(0,32):
        r = (i*3) & 7
        p = ((password[i] << r) | (password[i] >> (8 - r))) & 0xff
        h ^= p

    return h

# --------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # fragment h to 4 byte chunks
    hash = []
    for i in range(0,512,8):
        hash.append( int(hash_str[i:i+8], 16) )

    # do it for each possible h
    for h in range(256):
        pw = []

        for idx in range(64):
            final = hash[idx] ^ (h | (h << 8) | (h << 16) | (h << 24))
            final = final ^ idx ^ (idx << 6) ^ (idx << 12) ^ (idx << 18) ^ (idx << 24) ^ (idx << 30)
            final = (final ^ 0x5f208c26) & 0x7fff

            if idx & 1 == 0:
                pw.append( alpha_crack(final) )
            else:
                pw.append( beta_crack(final) )

    #    print hex(h), pw

        # does cracked password matches?
        if calc_h( pw[::2] ) == h:
            flag = ""
            for i in range(0, 64, 2):
                flag += chr(pw[i])

            print 'Flag found!', flag

# --------------------------------------------------------------------------------------------------
'''
C:\Python27\python.exe C:/Users/ispo/PycharmProjects/moon_crack/moon_crack.py
Flag found!                                 
Flag found! CTF{OpenGLMoonMoonG0esT0TheMoon}
'''
# --------------------------------------------------------------------------------------------------
