## Neo (Crypto, 200p)

###ENG
[PL](#pl-version)

The task shows a webpage with Neo going to Oracle.
There is a html form with some base64 encoded data.
Decoding gives some random 80 bytes blob.
Once every few seconds the data changes, most likely there is embedded timestamp.
If we provide our own base64 data in the form the page says that `AES decryption failed`.
This all points to `Padding Oracle Attack` - vulnerability which allows us to decode n-1 blocks of block cipher ciphertext in CBC mode.

In CBC mode the plaintext is XORed with previous block ciphertext.
This means that a change in a single byte of ciphertext will cause all bytes on corresponding positions in next blocks to be decrypted incorrectly, since they will be XORed with a wrong value.
What we want to achieve in the attack is to exploit how decryption handles padding.
In PKCS7 padding the last byte of decrypted data defines padding.
It's a number which says how many padding bytes there are and also what value each of them holds.
For example if there is 3 byte padding the 16 byte block would be `XXXXXXXXXXXXX0x30x030x3`.

If the padding is not formed correctly we will get decryption error, since it means the data were tamered with.
What we want to achieve with our attack is to try to guess the plaintext byte by attempting to "transform" it into padding.

Let's assume we have 2 blocks of ciphertext.
If we change the last byte of the first block this value will be XORed with decrypted last byte of the second block.
We changed it so it won't get the "proper" value anymore, so the padding will be broken for sure... unless the value will become `0x1`, which is a correct padding indicator!
If the value became `0x1` this means that `our_changed_byte XOR decrypted_byte = 0x1` and this means that `decrypted_byte = our_changed_byte XOR 0x1`!

So if for a certain value we won't get decryption error this means we successfully decoded the last byte of ciphertext.

Now we can extend this to more bytes - to recover the byte `k-1` we need to change the last byte to `0x2` and if we find the byte with no error in decryption it means that the xored value is also `0x2`.

This of course won't let us recover the first block, but this can't be helped, unless some special conditions are met.
In some cases the IV is placed as the first block of plaintext before encryption, and if this is the case, we could recover the IV as well.
In our case we had no knowledge of the way IV was handled, and if the IV is needed for us or not.
We assumed we don't need it and it turned out to be the right guess.

The attack implementation in python (we used https://github.com/mpgn/Padding-oracle-attack/blob/master/exploit.py as template)

```python
import base64
import re
import urllib
import urllib2
import sys
from binascii import hexlify, unhexlify
from itertools import cycle

# most of the code comes from https://github.com/mpgn/Padding-oracle-attack/blob/master/exploit.py
'''
    Padding Oracle Attack implementation of this article https://not.burntout.org/blog/Padding_Oracle_Attack/
    Check the readme for a full cryptographic explanation
    Author: mpgn <martial.puygrenier@gmail.com>
    Date: 2016
'''


def oracle(data):
    url = "http://crypto.chal.csaw.io:8001/"
    bytes_data = long_to_bytes(int(data, 16))
    values = {'matrix-id': base64.b64encode(bytes_data)}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    if "exception" in the_page:
        return False
    else:
        return True


def split_len(seq, length):
    return [seq[i:i + length] for i in range(0, len(seq), length)]


''' create custom block for the byte we search'''


def block_search_byte(size_block, i, pos, l):
    hex_char = hex(pos).split('0x')[1]
    return "00" * (size_block - (i + 1)) + ("0" if len(hex_char) % 2 != 0 else '') + hex_char + ''.join(l)


''' create custom block for the padding'''


def block_padding(size_block, i):
    l = []
    for t in range(0, i + 1):
        l.append(("0" if len(hex(i + 1).split('0x')[1]) % 2 != 0 else '') + (hex(i + 1).split('0x')[1]))
    return "00" * (size_block - (i + 1)) + ''.join(l)


def hex_xor(s1, s2):
    return hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(unhexlify(s1), cycle(unhexlify(s2)))))


def run(ciphertext, size_block):
    ciphertext = ciphertext.upper()
    found = False
    valid_value = []
    result = []
    len_block = size_block * 2
    cipher_block = split_len(ciphertext, len_block)
    if len(cipher_block) == 1:
        print "[-] Abort there is only one block"
        sys.exit()
    for block in reversed(range(1, len(cipher_block))):
        if len(cipher_block[block]) != len_block:
            print "[-] Abort length block doesn't match the size_block"
            break
        print "[+] Search value block : ", block, "\n"
        for i in range(0, size_block):
            for ct_pos in range(0, 256):
                if ct_pos != i + 1 or (
                                len(valid_value) > 0 and int(valid_value[len(valid_value) - 1], 16) == ct_pos):
                    bk = block_search_byte(size_block, i, ct_pos, valid_value)
                    bp = cipher_block[block - 1]
                    bc = block_padding(size_block, i)
                    tmp = hex_xor(bk, bp)
                    cb = hex_xor(tmp, bc).upper()
                    up_cipher = cb + cipher_block[block]
                    response = oracle(up_cipher)
                    exe = re.findall('..', cb)
                    discover = ''.join(exe[size_block - i:size_block])
                    current = ''.join(exe[size_block - i - 1:size_block - i])
                    find_me = ''.join(exe[:-i - 1])
                    sys.stdout.write(
                        "\r[+] Test [Byte %03i/256 - Block %d ]: \033[31m%s\033[33m%s\033[36m%s\033[0m" % (
                            ct_pos, block, find_me, current, discover))
                    sys.stdout.flush()
                    if response:
                        found = True
                        value = re.findall('..', bk)
                        valid_value.insert(0, value[size_block - (i + 1)])
                        print ''
                        print "[+] Block M_Byte : %s" % bk
                        print "[+] Block C_{i-1}: %s" % bp
                        print "[+] Block Padding: %s" % bc
                        print ''
                        bytes_found = ''.join(valid_value)
                        print '\033[36m' + '\033[1m' + "[+]" + '\033[0m' + " Found", i + 1, "bytes :", bytes_found
                        print ''
                        break
            if not found:
                print "\n[-] Error decryption failed"
                result.insert(0, ''.join(valid_value))
                hex_r = ''.join(result)
                print "[+] Partial Decrypted value (HEX):", hex_r.upper()
                padding = int(hex_r[len(hex_r) - 2:len(hex_r)], 16)
                print "[+] Partial Decrypted value (ASCII):", hex_r[0:-(padding * 2)].decode("hex")
                sys.exit()
            found = False
        result.insert(0, ''.join(valid_value))
        valid_value = []
    print ''
    hex_r = ''.join(result)
    print "[+] Decrypted value (HEX):", hex_r.upper()
    padding = int(hex_r[len(hex_r) - 2:len(hex_r)], 16)
    print "[+] Decrypted value (ASCII):", hex_r[0:-(padding * 2)].decode("hex")


def long_to_bytes(flag):
    flag = str(hex(flag))[2:-1]
    return "".join([chr(int(flag[i:i + 2], 16)) for i in range(0, len(flag), 2)])


def bytes_to_long(data):
    return int(data.encode('hex'), 16)


ct = base64.b64decode(
    "9aMTHPS1oP9VQA9Hxz5mGSIRuOVSspcQrGJlBYUoZIUhmur9X1B8hJJFeR48trScLtToNPCeWZiSz4Qit3KvsHlv0Xqy8rHREJUvYNbff1I=")
hexlified = bytes_to_long(ct)
run(hex(hexlified)[2:-1], 16)
```

Which gave us the flag in decrypted blocks: flag{what_if_i_told_you_you_solved_the_challenge}

###PL version

W zadaniu mamy stron?? internetow?? z Neo id??cym do Wyroczni.
Jest tam formularz html z ci??giem znak??w base64.
Dekodowanie daje nam 80 losowych bajt??w.
Co kilka sekund dane ulegaj?? zmianie, co sugeruje jaki?? timestamp.
Je??li podamy w??asny ci??g base64 strona odpowiada `AES decryption failed`.
Wszystko wskazuje na `Padding Oracle Attack` - podatno???? kt??ra pozwala odzyska?? n-1 blok??w szyfrogramu dla szyfru blokowego w trybie CBC.

W trybie CBC tekst przed szyfrowaniem jest XORowany z zaszyfrowanym blokiem poprzednim.
To oznacza ??e zmiana jednego bajtu szyfrogramu spowoduje ??e wszystkie bajty na odpowiadaj??cej pozycji w kolejnych blokach b??d?? ??le zdekodowane, poniewa?? zostan?? XORowane z inn?? warto??ci?? ni?? powinny.
W naszym ataku chcemy wykorzysta?? to w jaki spos??b deszyfrowanie wykorzystuje padding.
W paddingu PKCS7 ostatni bajt zawsze okre??la parametry wype??nienia.
To liczba kt??ra m??wi ile bajt??w paddingu mamy oraz jak?? warto???? powinien przyjmowa?? ka??dy z tych bajt??w.
Na przyk??ad je??li mamy 3 bajty paddingu w 16 bajtowym bloku to blok przyjmuje posta?? `XXXXXXXXXXXXX0x30x030x3`.

Je??li padding nie ma poprawnej formy dostaniemy b????d deszyfrowania, poniewa?? to oznacza ??e dane zosta??y uszkodzone/podmienione.
W naszym ataku chcemy zgadna?? bajt plaintextu poprzez zamienienie go w padding.

Za??????my ??e mamy 2 bloki szyfrogramu.
Je??li zmienimy ostatni bajt pierwszego bloku to ta warto???? zostanie XORowana z odszyfrowanym ostatnim bajtem drugiego bloku.
Poniewa?? zmienili??my warto???? na inn?? to ostatni bajt na pewno nie b??dzie mia?? ju?? warto??ci "poprawnej" wi??c padding b??dzie zepsutu... chyba ??e przypadkiem uzyskamy warto???? `0x1`, kt??ra jest poprawnym paddingiem!
Je??li warto???? sta??a si?? teraz `0x1` to znaczy ??e `nasz_zmieniony_bajt XOR odszyfrowany_bajt = 0x1` z czego wynika ??e `odszyfrowany_bajt = nasz_zmieniony_bajt XOR 0x1`!

Wi??c je??li dla jakiej?? warto??ci nie wyst??pi b????d deszyfrowania to znaczy ??e w??a??nie odkodowali??my ostatni bajt szyfrogramu.

Mo??emy to teraz rozszerzy?? na wi??cej bajt??w - aby odzyska?? teraz bajt `k-1` potrzebujemy aby ostatni bajt przyj???? warto???? `0x2` (mo??emy to zrobi?? bo znamy ju?? warto???? ostatniego bajtu) i je??li znajdziemy teraz bajt na pozycji k-1 dla kt??rego nie wyst??pi b????d deszyfrowania to znaczy ??e warto???? po XORowaniu wynosi teraz `0x2`.

To oczywi??cie nie pozwoli nam odzyska?? pierwszego bloku, ale z tym nic nie zrobimy, chyba ??e mamy do czynienia z pewn?? szczeg??ln?? sytuacj??, kiedy IV jest dodane jako pierwszy blok plaintextu.
W takiej sytuacji jeste??my w stanie odzyska?? tak??e IV.
W naszym przypadku nie wiedzieli??my nic na temat IV ani czy jest nam on do czego?? potrzebny, w zwi??zku z czym za??o??yli??my ??e nie i okaza??o si?? to by?? za??o??eniem poprawnym.

Atak zaimplementowali??my w pythonie (korzystaj??c z https://github.com/mpgn/Padding-oracle-attack/blob/master/exploit.py jako szablonu)

```python
import base64
import re
import urllib
import urllib2
import sys
from binascii import hexlify, unhexlify
from itertools import cycle

# most of the code comes from https://github.com/mpgn/Padding-oracle-attack/blob/master/exploit.py
'''
    Padding Oracle Attack implementation of this article https://not.burntout.org/blog/Padding_Oracle_Attack/
    Check the readme for a full cryptographic explanation
    Author: mpgn <martial.puygrenier@gmail.com>
    Date: 2016
'''


def oracle(data):
    url = "http://crypto.chal.csaw.io:8001/"
    bytes_data = long_to_bytes(int(data, 16))
    values = {'matrix-id': base64.b64encode(bytes_data)}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    if "exception" in the_page:
        return False
    else:
        return True


def split_len(seq, length):
    return [seq[i:i + length] for i in range(0, len(seq), length)]


''' create custom block for the byte we search'''


def block_search_byte(size_block, i, pos, l):
    hex_char = hex(pos).split('0x')[1]
    return "00" * (size_block - (i + 1)) + ("0" if len(hex_char) % 2 != 0 else '') + hex_char + ''.join(l)


''' create custom block for the padding'''


def block_padding(size_block, i):
    l = []
    for t in range(0, i + 1):
        l.append(("0" if len(hex(i + 1).split('0x')[1]) % 2 != 0 else '') + (hex(i + 1).split('0x')[1]))
    return "00" * (size_block - (i + 1)) + ''.join(l)


def hex_xor(s1, s2):
    return hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(unhexlify(s1), cycle(unhexlify(s2)))))


def run(ciphertext, size_block):
    ciphertext = ciphertext.upper()
    found = False
    valid_value = []
    result = []
    len_block = size_block * 2
    cipher_block = split_len(ciphertext, len_block)
    if len(cipher_block) == 1:
        print "[-] Abort there is only one block"
        sys.exit()
    for block in reversed(range(1, len(cipher_block))):
        if len(cipher_block[block]) != len_block:
            print "[-] Abort length block doesn't match the size_block"
            break
        print "[+] Search value block : ", block, "\n"
        for i in range(0, size_block):
            for ct_pos in range(0, 256):
                if ct_pos != i + 1 or (
                                len(valid_value) > 0 and int(valid_value[len(valid_value) - 1], 16) == ct_pos):
                    bk = block_search_byte(size_block, i, ct_pos, valid_value)
                    bp = cipher_block[block - 1]
                    bc = block_padding(size_block, i)
                    tmp = hex_xor(bk, bp)
                    cb = hex_xor(tmp, bc).upper()
                    up_cipher = cb + cipher_block[block]
                    response = oracle(up_cipher)
                    exe = re.findall('..', cb)
                    discover = ''.join(exe[size_block - i:size_block])
                    current = ''.join(exe[size_block - i - 1:size_block - i])
                    find_me = ''.join(exe[:-i - 1])
                    sys.stdout.write(
                        "\r[+] Test [Byte %03i/256 - Block %d ]: \033[31m%s\033[33m%s\033[36m%s\033[0m" % (
                            ct_pos, block, find_me, current, discover))
                    sys.stdout.flush()
                    if response:
                        found = True
                        value = re.findall('..', bk)
                        valid_value.insert(0, value[size_block - (i + 1)])
                        print ''
                        print "[+] Block M_Byte : %s" % bk
                        print "[+] Block C_{i-1}: %s" % bp
                        print "[+] Block Padding: %s" % bc
                        print ''
                        bytes_found = ''.join(valid_value)
                        print '\033[36m' + '\033[1m' + "[+]" + '\033[0m' + " Found", i + 1, "bytes :", bytes_found
                        print ''
                        break
            if not found:
                print "\n[-] Error decryption failed"
                result.insert(0, ''.join(valid_value))
                hex_r = ''.join(result)
                print "[+] Partial Decrypted value (HEX):", hex_r.upper()
                padding = int(hex_r[len(hex_r) - 2:len(hex_r)], 16)
                print "[+] Partial Decrypted value (ASCII):", hex_r[0:-(padding * 2)].decode("hex")
                sys.exit()
            found = False
        result.insert(0, ''.join(valid_value))
        valid_value = []
    print ''
    hex_r = ''.join(result)
    print "[+] Decrypted value (HEX):", hex_r.upper()
    padding = int(hex_r[len(hex_r) - 2:len(hex_r)], 16)
    print "[+] Decrypted value (ASCII):", hex_r[0:-(padding * 2)].decode("hex")


def long_to_bytes(flag):
    flag = str(hex(flag))[2:-1]
    return "".join([chr(int(flag[i:i + 2], 16)) for i in range(0, len(flag), 2)])


def bytes_to_long(data):
    return int(data.encode('hex'), 16)


ct = base64.b64decode(
    "9aMTHPS1oP9VQA9Hxz5mGSIRuOVSspcQrGJlBYUoZIUhmur9X1B8hJJFeR48trScLtToNPCeWZiSz4Qit3KvsHlv0Xqy8rHREJUvYNbff1I=")
hexlified = bytes_to_long(ct)
run(hex(hexlified)[2:-1], 16)
```

Co da??o nam flag?? w odszyfrowanych blokach: flag{what_if_i_told_you_you_solved_the_challenge}
