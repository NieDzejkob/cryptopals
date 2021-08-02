from utils import *
import random

def encryption_oracle(data):
    prefix = urandom(random.randrange(5, 10))
    suffix = urandom(random.randrange(5, 10))
    data = pad(prefix + data + suffix)
    key = urandom(16)
    cipher = AES.new(key, AES.MODE_ECB)

    global mode_used
    mode_used = random.choice(['cbc', 'ecb'])

    if mode_used == 'cbc':
        return cbc_encrypt(cipher.encrypt, urandom(16), data)
    else:
        return cipher.encrypt(data)

def detect():
    ct = encryption_oracle(b'A'*64)
    if len(set(blocks(ct))) < len(ct)//16:
        return 'ecb'
    else:
        return 'cbc'

for _ in range(50):
    answer = detect()
    assert answer == mode_used
