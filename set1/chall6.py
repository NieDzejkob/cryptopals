from utils import *
from base64 import b64decode
from chall3 import break_onexor

with open('input6.txt', 'r') as f:
    ct = b64decode(f.read())

def score_keysize(keysize):
    total = 0
    for i in range(3):
        left = ct[keysize*i:][:keysize]
        right = ct[keysize*(i+1):][:keysize]
        total += hamming_dist(left, right)
    return total / keysize

keysizes = sorted(range(2, 40), key=score_keysize)

def doit(keysize):
    pt = bytearray(len(ct))
    for offset in range(keysize):
        part = ct[offset::keysize]
        solved = break_onexor(part)
        if min(englishness(cyclic_xor(bytes([k]), part)) for k in range(256)) == 1e1000:
            return None
        for i, byte in zip(range(offset, len(ct), keysize), solved):
            pt[i] = byte

    return pt

pt = min(map(doit, keysizes[:3]), key=englishness)
print(pt.decode())
print(xor(pt, ct)[:29])
