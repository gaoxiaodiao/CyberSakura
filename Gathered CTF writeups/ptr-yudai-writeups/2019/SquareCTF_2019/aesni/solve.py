from ptrlib import xor

key = b'\x55'
encoded = b"\001=\034&x<\006x3\034;\020Uc7cfcde9b27cb5904a273dbe81679dde\026JV\\]k\200\002S\352\023\325^\017\274\020n\223\300\363@\n]\207_Z\330a\353\206\003\016>\243M|P\a\222\225\260d38;`*e\033u _5?8gldech4>\fP,*\023`d0d8b3b?d4d\202nLpP\006\271TRSQ"[:13]

print(xor(encoded, key))
