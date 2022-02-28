from ptrlib import *

def convert(num):
    if num == 'A': return 1
    if num == 'J': return 11
    if num == 'Q': return 12
    if num == 'K': return 13
    return int(num)

def parse(data):
    cards = []
    syms = []
    x = data[1:-1].split(", ")
    for card in x:
        cards.append(convert(card[1:]))
        syms.append(card[0])
    return cards, syms

def judge_by_symbol(sym1, sym2):
    if sym1 == 'S' and sym2 != 'S': return 1
    if sym2 == 'S' and sym1 != 'S': return 2
    if sym1 == 'D' and sym2 != 'D': return 1
    if sym2 == 'D' and sym1 != 'D': return 2
    if sym1 == 'H' and sym2 != 'H': return 1
    if sym2 == 'H' and sym1 != 'H': return 2
    if sym1 == 'C' and sym2 != 'C': return 1
    if sym2 == 'C' and sym1 != 'C': return 2
    return 1

def judge_by_symbols(syms1, syms2):
    if syms1.count('S') > syms2.count('S'): return 1
    if syms1.count('S') < syms2.count('S'): return 2
    if syms1.count('D') > syms2.count('D'): return 1
    if syms1.count('D') < syms2.count('D'): return 2
    if syms1.count('H') > syms2.count('H'): return 1
    if syms1.count('H') < syms2.count('H'): return 2
    if syms1.count('C') > syms2.count('C'): return 1
    if syms1.count('C') < syms2.count('C'): return 2
    return 0

def judge_by_number(a, b, c, d, func):
    cards1, syms1, cards2, syms2 = list(a), list(b), list(c), list(d)
    if func is None:
        for num in [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]:
            while True:
                if num in cards1 and num not in cards2: return 1
                if num not in cards1 and num in cards2: return 2
                if num in cards1 and num in cards2:
                    i, j = cards1.index(num), cards2.index(num)
                    if syms1[i] != syms2[j]:
                        return judge_by_symbol(syms1[i], syms2[j])
                    cards1 = cards1[:i] + cards1[i+1:]
                    syms1  = syms1[:i] + syms1[i+1:]
                    cards2 = cards2[:i] + cards2[i+1:]
                    syms2  = syms2[:i] + syms2[i+1:]
                break
    elif func == is_one_pair:
        for o1, c in enumerate(cards1):
            if cards1.count(c) == 2:
                n1 = c
                break
        for o2, c in enumerate(cards2):
            if cards2.count(c) == 2:
                n2 = c
                break
        oo1 = cards1.index(n1, o1+1)
        oo2 = cards2.index(n2, o2+1)
        s1, s2 = syms1[o1], syms2[o2]
        ss1, ss2 = syms1[oo1], syms2[oo2]
        if n1 > n2: return 1
        elif n2 > n1: return 2
        else:
            r = judge_by_symbols([s1, ss1], [s2, ss2])
            if r == 0:
                if sum(cards1) > sum(cards2):
                    return 1
                else:
                    return 2 # debug!!
            else:
                return r
    elif func == is_two_pairs:
        if sum(cards1) > sum(cards2):
            return 1
        else:
            return 2 # debug!!
    elif func == is_three_pairs:
        if sum(cards1) > sum(cards2):
            return 1
        else:
            return 2 # debug!!
    return 1

def is_royal(cards, syms):
    if 10 not in cards: return False
    if 11 not in cards: return False
    if 12 not in cards: return False
    if 13 not in cards: return False
    if 1 not in cards: return False
    if syms.count('S') == 5: return True
    if syms.count('H') == 5: return True
    if syms.count('C') == 5: return True
    if syms.count('D') == 5: return True
    return False

def is_straight_flush(cards, syms):
    base = min(cards)
    if base + 1 not in cards: return False
    if base + 2 not in cards: return False
    if base + 3 not in cards: return False
    if base + 4 not in cards: return False
    if syms.count('S') == 5: return True
    if syms.count('H') == 5: return True
    if syms.count('C') == 5: return True
    if syms.count('D') == 5: return True
    return False

def is_four_of_king(cards, syms):
    for c in cards:
        if cards.count(c) == 4:
            return True
    #if cards.count(13) >= 4: return True
    return False

def is_full_house(cards, syms):
    base1 = cards[0]
    if cards.count(base1) == 3:
        base2 = list(filter(lambda x: x != base1, cards))[0]
        if cards.count(base2) == 2:
            return True
    elif cards.count(base1) == 2:
        base2 = list(filter(lambda x: x != base1, cards))[0]
        if cards.count(base2) == 3:
            return True
    return False

def is_flush(cards, syms):
    if syms.count('S') == 5: return True
    if syms.count('H') == 5: return True
    if syms.count('C') == 5: return True
    if syms.count('D') == 5: return True
    return False

def is_straight(cards, syms):
    base = min(cards)
    if base + 1 not in cards: return False
    if base + 2 not in cards: return False
    if base + 3 not in cards: return False
    if base + 4 not in cards: return False
    return True

def is_three_of_king(cards, syms):
    for c in cards:
        if cards.count(c) == 3:
            return True
    return False

def is_two_pairs(cards, syms):
    x = 0
    for c in cards:
        if cards.count(c) == 2:
            x += 1
    return x == 4

def is_one_pair(cards, syms):
    for c in cards:
        if cards.count(c) == 2:
            return True
    return False

def judge(cards1, syms1, cards2, syms2):
    judge_funcs = [is_royal, is_straight_flush, is_four_of_king, is_full_house, is_flush, is_straight, is_three_of_king, is_two_pairs, is_one_pair]
    for func in judge_funcs:
        if func(cards1, syms1):
            if func(cards2, syms2):
                print("{} wins: {}".format(judge_by_number(cards1, syms1, cards2, syms2, func), func))
                return judge_by_number(cards1, syms1, cards2, syms2, func)
            else:
                print("1 wins: " + str(func))
                return 1
        elif func(cards2, syms2):
            print("2 wins: " + str(func))
            return 2
    print("{} wins: no pair".format(judge_by_number(cards1, syms1, cards2, syms2, None)))
    return judge_by_number(cards1, syms1, cards2, syms2, None)

sock = Socket("211.239.124.246", 12402)

for i in range(500):
    sock.recvuntil("[Round")
    sock.recvuntil("Player 1\n")
    cards1, syms1 = parse(bytes2str(sock.recvline()))
    sock.recvuntil("Player 2\n")
    cards2, syms2 = parse(bytes2str(sock.recvline()))
    print("[Round {}]".format(i + 1))
    print(cards1, syms1)
    print(cards2, syms2)
    sock.sendlineafter(">>", str(judge(cards1, syms1, cards2, syms2)))
    sock.recvuntil("Correct!")

sock.interactive()
