from utils import *

with open('input10.txt') as f:
    ct = b64decode(f.read())

cipher = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
print(unpad(cbc_decrypt(cipher.decrypt, bytes(16), ct)).decode())
