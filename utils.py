from string import ascii_lowercase
from collections import Counter
from itertools import *
from base64 import b64encode, b64decode
from Crypto.Cipher import AES

def xor(A, B):
    assert len(A) == len(B)
    return bytes(a^b for a, b in zip(A, B))

def cyclic_xor(key, data):
    return bytes(a^b for a, b in zip(cycle(key), data))

def popcount(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def hamming_dist(A, B):
    return sum(popcount(a ^ b) for a, b in zip(A, B))

def blocks(data, size=16):
    for i in range(0, len(data), size):
        yield data[i:i+size]

def pad(data, block_size=16):
    rest = block_size - (len(data) % block_size)
    return data + bytes([rest] * rest)

def unpad(data, block_size=16):
    assert len(data) % block_size == 0
    padding_length = data[-1]
    assert 0 < padding_length <= block_size
    assert data[-padding_length:] == bytes([padding_length]*padding_length)
    return data[:-padding_length]

def cbc_decrypt(decrypt_block, iv, ct):
    pt = b''
    for block in blocks(ct):
        pt += xor(iv, decrypt_block(block))
        iv = block
    return pt

assert hamming_dist(b'this is a test', b'wokka wokka!!!') == 37

english_freq = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,  # A-G
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,  # H-N
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,  # O-U
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074                     # V-Z
]

space_freq = 0.19
# scale the rest to fit
english_freq = [x * (1 - space_freq) for x in english_freq]
english_freq.append(space_freq)

def chi_seq(expected, actual):
    return sum((act - exp)**2 / exp for exp, act in zip(expected, actual))

# lower is better
# https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis
def englishness(s):
    def index(c):
        assert type(c) == int
        try:
            return ascii_lowercase.encode().index(c)
        except ValueError:
            if c == b' '[0]:
                return 26
            elif c >= 127 or c < 32 and c not in b'\t\n\r':
                return 28
            else:
                return 27
    s = s.lower()
    freq = Counter(map(index, s))
    ignored = freq[27] + freq[28]
    count = len(s) - ignored
    if count == 0:# or freq[28]:
        return 1e1000
    expected = [count * x for x in english_freq]
    actual = [freq[i] for i in range(len(english_freq))]
    return chi_seq(expected, actual) + 300 * ignored
