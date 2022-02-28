# uncompyle6 version 3.4.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.7 (default, Apr  9 2019, 14:35:10) 
# [GCC 7.3.0]
# Embedded file name: circ.py
# Compiled at: 2019-12-14 03:29:55
# Size of source mod 2**32: 5146 bytes
佤 = 0
侰 = ~佤 * ~佤
俴 = 侰 + 侰

def 䯂(䵦):
    굴 = 佤
    굿 = 佤
    괠 = [佤] * 俴 ** (俴 * 俴)
    궓 = [佤] * 100
    괣 = []
    while 䵦[굴][佤] != '듃':
        굸 = 䵦[굴][佤].lower()
        亀 = 䵦[굴][侰:]
        if 굸 == '뉃':
            괠[亀[佤]] = 괠[亀[侰]] + 괠[亀[俴]]
        elif 굸 == '렀':
            괠[亀[佤]] = 괠[亀[侰]] ^ 괠[亀[俴]]
        elif 굸 == '렳':
            괠[亀[佤]] = 괠[亀[侰]] - 괠[亀[俴]]
        elif 굸 == '냃':
            괠[亀[佤]] = 괠[亀[侰]] * 괠[亀[俴]]
        elif 굸 == '뢯':
            괠[亀[佤]] = 괠[亀[侰]] / 괠[亀[俴]]
        elif 굸 == '륇':
            괠[亀[佤]] = 괠[亀[侰]] & 괠[亀[俴]]
        elif 굸 == '맳':
            괠[亀[佤]] = 괠[亀[侰]] | 괠[亀[俴]]
        elif 굸 == '괡':
            괠[亀[佤]] = 괠[亀[佤]]
        elif 굸 == '뫇':
            괠[亀[佤]] = 괠[亀[侰]]
        elif 굸 == '꼖':
            괠[亀[佤]] = 亀[侰]
        elif 굸 == '뫻':
            궓[亀[佤]] = 괠[亀[侰]]
        elif 굸 == '딓':
            괠[亀[佤]] = 궓[亀[侰]]
        elif 굸 == '댒':
            괠[亀[佤]] = 佤
        elif 굸 == '묇':
            궓[亀[佤]] = 佤
        elif 굸 == '묟':
            괠[亀[佤]] = input(괠[亀[侰]])
        elif 굸 == '꽺':
            궓[亀[佤]] = input(괠[亀[侰]])
        elif 굸 == '돯':
            print(괠[亀[佤]])
        elif 굸 == '뭗':
            print(궓[亀[佤]])
        elif 굸 == '뭿':
            굴 = 괠[亀[佤]]
        elif 굸 == '뮓':
            굴 = 궓[亀[佤]]
        elif 굸 == '뮳':
            굴 = 괣.pop()
        elif 굸 == '믃':
            if 괠[亀[侰]] > 괠[亀[俴]]:
                굴 = 亀[佤]
                괣.append(굴)
                continue
        elif 굸 == '꽲':
            괠[7] = 佤
            for i in range(len(괠[亀[佤]])):
                if 괠[亀[佤]] != 괠[亀[侰]]:
                    괠[7] = 侰
                    굴 = 괠[亀[俴]]
                    괣.append(굴)

        elif 굸 == '꾮':
            괢 = ''
            for i in range(len(괠[亀[佤]])):
                괢 += chr(ord(괠[亀[佤]][i]) ^ 괠[亀[侰]])

            괠[亀[佤]] = 괢
        elif 굸 == '꿚':
            괢 = ''
            for i in range(len(괠[亀[佤]])):
                괢 += chr(ord(괠[亀[佤]][i]) - 괠[亀[侰]])

            괠[亀[佤]] = 괢
        elif 굸 == '떇':
            if 괠[亀[侰]] > 괠[亀[俴]]:
                굴 = 괠[亀[佤]]
                괣.append(굴)
                continue
        elif 굸 == '뗋':
            if 괠[亀[侰]] > 괠[亀[俴]]:
                굴 = 궓[亀[佤]]
                괣.append(굴)
                continue
        elif 굸 == '똷':
            if 괠[亀[侰]] == 괠[亀[俴]]:
                굴 = 亀[佤]
                괣.append(굴)
                continue
        elif 굸 == '뚫':
            if 괠[亀[侰]] == 괠[亀[俴]]:
                굴 = 괠[亀[佤]]
                괣.append(굴)
                continue
        elif 굸 == '띇':
            if 괠[亀[侰]] == 괠[亀[俴]]:
                굴 = 궓[亀[佤]]
                괣.append(굴)
                continue
        굴 += 侰


䯂([
 [
  '꼖', 佤, 'Authentication token: '],
 [
  '꽺', 佤, 佤],
 [
  '꼖', 6, '\xc3\xa1\xc3\x97\xc3\xa4\xc3\x93\xc3\xa2\xc3\xa6\xc3\xad\xc3\xa4\xc3\xa0\xc3\x9f\xc3\xa5\xc3\x89\xc3\x9b\xc3\xa3\xc3\xa5\xc3\xa4\xc3\x89\xc3\x96\xc3\x93\xc3\x89\xc3\xa4\xc3\xa0\xc3\x93\xc3\x89\xc3\x96\xc3\x93\xc3\xa5\xc3\xa4\xc3\x89\xc3\x93\xc3\x9a\xc3\x95\xc3\xa6\xc3\xaf\xc3\xa8\xc3\xa4\xc3\x9f\xc3\x99\xc3\x9a\xc3\x89\xc3\x9b\xc3\x93\xc3\xa4\xc3\xa0\xc3\x99\xc3\x94\xc3\x89\xc3\x93\xc3\xa2\xc3\xa6\xc3\x89\xc3\xa0\xc3\x93\xc3\x9a\xc3\x95\xc3\x93\xc3\x92\xc3\x99\xc3\xa6\xc3\xa4\xc3\xa0\xc3\x89\xc3\xa4\xc3\xa0\xc3\x9f\xc3\xa5\xc3\x89\xc3\x9f\xc3\xa5\xc3\x89\xc3\xa4\xc3\xa0\xc3\x93\xc3\x89\xc3\x9a\xc3\x93\xc3\xa1\xc3\x89\xc2\xb7\xc3\x94\xc3\xa2\xc3\x97\xc3\x9a\xc3\x95\xc3\x93\xc3\x94\xc3\x89\xc2\xb3\xc3\x9a\xc3\x95\xc3\xa6\xc3\xaf\xc3\xa8\xc3\xa4\xc3\x9f\xc3\x99\xc3\x9a\xc3\x89\xc3\x85\xc3\xa4\xc3\x97\xc3\x9a\xc3\x94\xc3\x97\xc3\xa6\xc3\x94\xc3\x89\xc3\x97\xc3\x9a\xc3\xaf\xc3\xa1\xc3\x97\xc3\xaf\xc3\xa5\xc3\x89\xc3\x9f\xc3\x89\xc3\x94\xc3\x99\xc3\x9a\xc3\xa4\xc3\x89\xc3\xa6\xc3\x93\xc3\x97\xc3\x9c\xc3\x9c\xc3\xaf\xc3\x89\xc3\xa0\xc3\x97\xc3\xa2\xc3\x93\xc3\x89\xc3\x97\xc3\x89\xc3\x91\xc3\x99\xc3\x99\xc3\x94\xc3\x89\xc3\xa2\xc3\x9f\xc3\x94\xc3\x89\xc3\x96\xc3\xa3\xc3\xa4\xc3\x89\xc3\x9f\xc3\x89\xc3\xa6\xc3\x93\xc3\x97\xc3\x9c\xc3\x9c\xc3\xaf\xc3\x89\xc3\x93\xc3\x9a\xc3\x9e\xc3\x99\xc3\xaf\xc3\x89\xc3\xa4\xc3\xa0\xc3\x9f\xc3\xa5\xc3\x89\xc3\xa5\xc3\x99\xc3\x9a\xc3\x91\xc3\x89\xc3\x9f\xc3\x89\xc3\xa0\xc3\x99\xc3\xa8\xc3\x93\xc3\x89\xc3\xaf\xc3\x99\xc3\xa3\xc3\x89\xc3\xa1\xc3\x9f\xc3\x9c\xc3\x9c\xc3\x89\xc3\x93\xc3\x9a\xc3\x9e\xc3\x99\xc3\xaf\xc3\x89\xc3\x9f\xc3\xa4\xc3\x89\xc3\x97\xc3\xa5\xc3\xa1\xc3\x93\xc3\x9c\xc3\x9c\xc2\x97\xc3\x89\xc3\xaf\xc3\x99\xc3\xa3\xc3\xa4\xc3\xa3\xc3\x96\xc3\x93\xc2\x9a\xc3\x95\xc3\x99\xc3\x9b\xc2\x99\xc3\xa1\xc3\x97\xc3\xa4\xc3\x95\xc3\xa0\xc2\xa9\xc3\xa2\xc2\xab\xc2\xb3\xc2\xa3\xc3\xaf\xc2\xb2\xc3\x95\xc3\x94\xc3\x88\xc2\xb7\xc2\xb1\xc3\xa2\xc2\xa8\xc3\xab'],
 [
  '꼖', 俴, 俴 ** (3 * 俴 + 侰) - 俴 ** (俴 + 侰)],
 [
  '꼖', 4, 15],
 [
  '꼖', 3, 侰],
 [
  '냃', 俴, 俴, 3],
 [
  '뉃', 俴, 俴, 4],
 [
  '괡', 佤, 俴],
 [
  '댒', 3],
 [
  '꾮', 6, 3],
 [
     '꼖', 佤, 'Thanks.'],
 [
  '꼖', 侰, 'Authorizing access...'],
 [
  '돯', 佤],
 [
  '딓', 佤, 佤],
 [
  '꾮', 佤, 俴],
 [
  '꿚', 佤, 4],
 [
  '꼖', 5, 19],
 [
  '꽲', 佤, 6, 5],
 [
  '돯', 侰],
 [
  '듃'],
 [
  '꼖', 侰, 'Access denied!'],
 [
  '돯', 侰],
 [
  '듃']])
# okay decompiling 3nohtyp.pyc
