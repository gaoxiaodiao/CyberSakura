with open("cipher.txt", "rb") as f:
    cipher = f.read()

words = cipher.split(b" ")
"""
wordlist = {}
for word in words:
    if word in wordlist:
        wordlist[word] += 1
    else:
        wordlist[word] = 1
print(wordlist)
"""

output = ""
for word in words:
    if word == b'\xe0\xb2\xb8\xe0\xb3\x81\xe0\xb2\xb8\xe0\xb3\x8d\xe0\xb2\xb5\xe0\xb2\xbe\xe0\xb2\x97\xe0\xb2\xa4\xe0\xb2\xb9\xe0\xb3\x8b\xe0\xb2\xaf\xe0\xb2\xbf':
        output += "0"
    elif word == b'\xe0\xb2\x86\xe0\xb2\xa8\xe0\xb3\x8d':
        output += "1"
    elif word == b'\xe0\xb2\xaa\xe0\xb3\x8d\xe0\xb2\xb0\xe0\xb2\xb5\xe0\xb2\xbe\xe0\xb2\xb8\xe0\xb2\xb9\xe0\xb3\x8b\xe0\xb2\xaf\xe0\xb2\xbf':
        output += "2"
    elif word == b'\xe0\xb2\xaa\xe0\xb3\x8d\xe0\xb2\xb0\xe0\xb2\xb5\xe0\xb2\xbe\xe0\xb2\xb8\xe0\xb2\xa6\xe0\xb2\xbe\xe0\xb2\xa8\xe0\xb2\x82\xe0\xb2\x97\xe0\xb3\x8d\xe2\x80\x8c\xe0\xb2\x97\xe0\xb3\x86':
        output += "3"
    elif word == b'\xe0\xb2\xb8\xe0\xb3\x81\xe0\xb2\xb8\xe0\xb3\x8d\xe0\xb2\xb5\xe0\xb2\xbe\xe0\xb2\x97\xe0\xb2\xa4\xe0\xb2\xa6\xe0\xb2\xbe\xe0\xb2\xa8\xe0\xb2\x82\xe0\xb2\x97\xe0\xb3\x8d\xe2\x80\x8c\xe0\xb2\x97\xe0\xb3\x86':
        output += "4"
print(output)
print(hex(int(output, 5)))

# ABCBDABDEEEABCBCBDABDEEABCBCBDABDEEABCBCBDEEEEABCBCBDEABCBDEABCBCBDABDEEABDABCBCBCBDEABDABCBCBCBDABCBDABCBDABDABCBDEABDABDABCBDEABCBCBDABCBDEEEABDEABDABCBCBDEABCBDABCBCBDEABCBCBCBDABDEEABDABCBCBCBDEABDEEABCBDABDEEABCBDEEABDEEEABDABCBCBDEEABDEABCBDEEEEABCBDABCBDEEABDABDEABDEABDABDABDABDABDEEEABCBDEABCBDABDEEABDEEEEABDEABDEEEABDABCBCBCBDEABDEABCBDEABDEABDABDEABDEABCBCBCBDABDEEABCBDEEABDABCBCBDEEABDABCBDEEABDEEABCBDABDABDABCBCBCBDEABDABDABCBDEABDABCBDEEEABDABCBDEABDEEABDEABCBCBCBDEABCBCBDEEEABDABDEEABDEABDABCBDABDABCBDEEABCBDABCBDEABDEEABDABCBDEEEEABDABCBDABDABDEABCBCBDEABCBDEABCBCB
