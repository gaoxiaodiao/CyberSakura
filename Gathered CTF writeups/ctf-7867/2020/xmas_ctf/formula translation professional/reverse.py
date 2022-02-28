import numpy as np

def entrypoint(MAT):
	for I in range(0, 16, 4):
		flag(- MAT[(I >> 1) - 3]) ^ 45 == PORTION[(I >> 2) + 1][0]
		flag(- MAT[((I + 2) >> 1) - 3]) ^ 45 == PORTION[(I >> 2) + 1][1]

def entry_rev(MAT, flag):
	# MAT = MAT[0] + MAT[1] + MAT[2]
	# for I in range(0, 17, 4):
	# 	flag[-MAT[(I >> 1) - 3] + 52] = chr(PORTION[(I >> 2)][0] ^ 45)
	# 	flag[-MAT[((I + 2) >> 1) - 3] + 52] = chr(PORTION[(I >> 2)][1] ^ 45)
	MAT = [i * 5 for i in range(1, 10)]
	arr = [53, 51, 95, 51, 100, 100, 49, 78, 95]
	# arr = [53, 51, 95, 51, 100, 49, 78, 95, 125]

	# print(np.asarray(MAT).reshape(3, 3))
	# print(np.asarray([chr(ch)for ch in arr]).reshape(3, 3))

	MAT = np.asarray(MAT).reshape(3, 3).T.reshape(9, )
	# print(MAT)

	for i in range(9):
		# print(MAT[i], chr(arr[i]))
		flag[-MAT[i]+52] = chr(arr[i])

	return flag


def main(POSITRONS):
	COERCION = r"'"
	ARITHMETIC = 2 * ord(COERCION) + 17
	MAIN = 1
	for i in range(8, 1, -1):
		if (str(POSITRONS[i] + 1)) != ARITHMETIC:
			MAIN = 0

def main_rev(POSITRONS, flag):
	COERCION = r"'"
	ARITHMETIC = 2 * ord(COERCION) + 17
	for i in range(8):
		j = 7 - i
		flag[POSITRONS[j] + 1 + 52] = chr(ARITHMETIC)
	return flag

def swapper(POLYMER, COPOLYMER):
	OP = POLYMER
	POLYMER = COPOLYMER
	COPOLYMER = OP

PORTION = [(24,30),(114,30),(73,73),(28,99),(114,80)]
PU = 3
PV = 1.0 / (10) 
PW = -52

X = 0
AF = 'HD'
BF = 'DS'
flag = [' '] * 53

AMINO = [51, 49, 50, 49, 49, 49, 50, 49, 51, 50]
A = [88, 45, 77, 65, 83]

flag[0] = chr(A[0])
flag[1] = chr(A[1])
flag[2] = chr(A[2])
flag[3] = chr(A[3])
flag[4] = chr(A[4])
flag[-2+52] = '0'
flag[-3+52] = '1'

POSITRONS = [-46,-40,-36,-32,-25,-20,-10,-5]

flag = main_rev(POSITRONS, flag)
flag[52] = chr(125)
flag[5] = chr(123)
flag[-1+52] = chr(115)
fixed = flag[:]

X = X + 1

print('Start:\t\t\t', ''.join(flag))

# skipped
arr = [0x94, 0xcc, 0xcc, 0xa0, 0xb1, 0xcc, 0xcb]
for I in range(7):
	flag[-6 * X + 52] = chr(arr[I] ^ 255)
	X += 1

print('After first read:\t', ''.join(flag))


# for J in range(5, 2, -1):
# 	flag[-7 * X + 52] = chr(contents[file_ind] ^ 45)
# 	file_ind += 1
# 	flag[-3 * X + 52] = chr(contents[file_ind])
# 	file_ind += 1

M = [['', '', ''], ['', '', ''], ['', '', '']]
for F in range(9):
	X = F + 1
	X = 5 * X
	M[F//3][F%3] = X

print()
flag = entry_rev(M, flag)

print('After entrypoint:\t', ''.join(flag))

arr1 = [46.0000000, 33.0000000, 34.0000000, 28.0000000, 18.0000000, 22.0000000, 23.0000000, 9.00000000, 12.0000000, 15.0000000, 4.00000000, 6.00000000]
arr2 = [91.0000000, 82.0000000, 77.0000000, 127.000000, 120.000000, 127.000000, 119.000000, 96.0000000, 121.000000, 100.000000, 122.000000, 116.000000]

for ind in range(len(arr1)):
	key = int(arr1[ind])
	I = -(key ^ 7)
	ch = int(arr2[ind]) ^ -I
	flag[I+52] = chr(ch)

print('After 2nd read:\t\t', ''.join(flag))

flag[-44 + 52] = 'H'
flag[-34 + 52] = 'D'
flag[-32 + 52] = 'D'
flag[-23 + 52] = 'S'

print('After strings:\t\t', ''.join(flag))

X = "1303330310" + ''.join(list(map(lambda x: chr(x), [num ^ 2 for num in AMINO])))
X = int(X)
X = X // 10

arr = [0x5d, 0x58, 0x4e, 0x4a, 0x48, 0x47, 0x43, 0x40, 0x36]
for c in arr:
	ind = c - 100
	flag[ind+52] = chr(48 + (X % 10))
	X = X //10

print('Final:\t\t\t', ''.join(flag))
print()
print('Original:\t\t', ''.join(fixed))
print('Current Guess:\t\t', r'X-MAS{1_H34rd_th3_D0D_N33d3d_S0m3_3ng1n33r3_l1k5_y0u}')


