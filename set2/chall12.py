from utils import *

cipher = AES.new(urandom(16), AES.MODE_ECB)

def oracle(data):
    data = data + b64decode('''
        Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
        aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
        dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
        YnkK
    ''')

    return cipher.encrypt(pad(data))

known = b''

while not known.endswith(b'\x01'):
    pad_length = 16 - (len(known) + 1) % 16
    prefix = b'A' * pad_length
    attack_block = (prefix + known)[-15:]
    skip_count = len(prefix + known) - 15
    recognizers = b''.join(attack_block + bytes([x]) for x in range(256))

    ct = oracle(recognizers + prefix)
    block_dict = {}
    for i in range(0, 256*16, 16):
        block_dict[ct[i:i+16]] = i//16

    next_byte = block_dict[ct[256*16 + skip_count:][:16]]
    known += bytes([next_byte])

print(known[:-1].decode())
