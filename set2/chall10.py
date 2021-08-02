from utils import *

with open('input10.txt') as f:
    ct = b64decode(f.read())

cipher = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
pt = unpad(cbc_decrypt(cipher.decrypt, bytes(16), ct))
print(pt.decode())

assert cbc_encrypt(cipher.encrypt, bytes(16), pad(pt)) == ct
