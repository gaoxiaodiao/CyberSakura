def analyzer(M, I, B):
	B *= 2
	OP = B ^ 35
	if OP == M[I]:
		return 1.0
	else:
		return 0.0

def rev_analyzer(M, I):
	OP = M[I]
	B = (OP ^ 35) // 2
	return chr(B)

def compute(A, I, B):
	B *= 2
	I = I - 48
	return A == B

def rev_compute(I, B):
	B *= 2
	I = I - 48
	return B >> 1

# CONVOLUTIONMATRIX = [[7, 13, 15], [17, 19, 24], [30, 31, 34], [37 , 39, 41]]
CONVOLUTIONMATRIX = [7, 13, 15, 17, 19, 24, 30, 31, 34, 37 , 39, 41]
PROGRESSIONMATRIX = [241, 209, 201, 243, 207, 249, 231, 251 , 235, 255, 209, 201]
# POSITIONMATRIX = [[[134, 36, 175, 63, 112], [163, 111, 37, 140, 73]], [[172, 83, 61, 65, 135], [53, 146, 43, 157, 58]]]

# POSITIONMATRIX = [118, 53, 43, 51, 117, 51, 41, 53, 116, 51, 40, 48, 113, 48, 38, 51, 109, 52, 36, 55]
POSITIONMATRIX = [
	[[118, 117, 116, 113, 109], [53, 51, 51, 48, 52]],
	[[43, 41, 40, 38, 36], [51, 53, 48, 51, 55]]
]

flag = [''] * 42
TT = [85, 32, 64, 76, 94]
ANTIMONY = [0, 4, 5, 8, 12]
# POSITIONMATRIX = [[[118, 53, 43, 51, 117], [51, 41, 53, 116, 51]], [[40, 48, 113, 48, 38], [51, 109, 52, 36, 55]]]

AX = 28
AY = 48

for j in range(5):
	flag[j] = chr(13 ^ TT[j])

flag[5] = chr(123)
flag[41] = chr(125)

TT2 = [8, 12, 16, 21, 26]

for J in range(5):
    flag[TT2[J] - 1] = chr(95)

for j in range(12):
	flag[CONVOLUTIONMATRIX[j] - 1] = rev_analyzer(PROGRESSIONMATRIX, j)

flag[28] = chr(95)
flag[34] = chr(95)
flag[37] = chr(95)

INSTRUCTION = 5570010
ind = 0
for J in range(5):
	flag[AX + ANTIMONY[4 - ind] - 1] = chr(rev_compute(J, int(AY + INSTRUCTION % 10)))
	INSTRUCTION = INSTRUCTION // 10
	ind += 1
	# optimize must be 1


for J in range(5):
	flag[(POSITIONMATRIX[0][0][J] ^ 127) - 1] = chr(POSITIONMATRIX[0][1][J])
	flag[(POSITIONMATRIX[1][0][J] ^ 63) - 1] = chr(POSITIONMATRIX[1][1][J])

# print(flag)
print(''.join(flag))
print(len(''.join(flag)))