header = "B2 R U F' R' L' B B2 L F D D' R' F2 D' R R D2 B' L R"
info = "L' L B F2 R2 F2 R' L F' B' R D' D' F U2 B' U U D' U2 F'"
msg = "L F' F2 R B R R F2 F' R2 D F' U L U' U' U F D F2 U R U' F U B2 B U2 D B F2 D2 L2 L2 B' F' D' L2 D U2 U2 D2 U B' F D R2 U2 R' B' F2 D' D B' U B' D B' F' U' R U U' L' L' U2 F2 R R F L2 B2 L2 B B' D R R' U L"

default_table = {
    "F": 0, "B": 1, "L2": 2, "R2": 3, "U2": 4, "D2": 5,
    "F'": 6, "U'": 7, "D'": 8, "L": 0, "R": 1, "U": 2,
    "D": 3, "F2": 4, "B2": 5, "L'": 6, "R'": 7, "B'": 8
}

# sample
#header = "L2 F' B2 U D2 B U D' F2 L' F U2 R U' L' R' U' B F D U'"
#info = "B U2 D2 R' F U2 B R L' B L' B L' D F' L U' B2 R F2 L' F2"

# extract P
str_h1 = ""
for c in header.split():
    str_h1 += str(default_table[c])
h1 = int(str_h1, 9)
str_h1 = str(h1)
len_sub = int(str_h1[0])
sub1 = int(str_h1[1:1+len_sub])
sub2 = int(str_h1[10+len_sub:])
P = int(str_h1[1+len_sub:10+len_sub])
print("sub1 = " + str(sub1))
print("sub2 = " + str(sub2))
print("P    = " + str(P))

# extract length info
str_leninfo = ""
for c in info.split():
    str_leninfo += str(str(P).index(str(default_table[c])))
print(str_leninfo)
leninfo = int(str_leninfo, 9)
str_leninfo = str(leninfo)
j = int(str_leninfo[0])
k = int(str_leninfo[1])
sub3 = int(str_leninfo[2:2+j])
len_msg = int(str_leninfo[2+j:2+j+k])
sub4 = int(str_leninfo[2+j+k:])
print("sub3 = " + str(sub3))
print("sub4 = " + str(sub4))
print("len  = " + str(len_msg))

# extract msg
msglist = msg.split()[:len_msg]
str_msginfo = ""
for c in msglist:
    str_msginfo += str(str(P).index(str(default_table[c])))
msginfo = int(str_msginfo, 9)
#bin_msg = bin(msginfo)[2:]
#bin_msg = "0" * (8 - (len(bin_msg) % 8) ) + bin_msg
print(hex(msginfo)[2:].rstrip("L").decode("hex"))
