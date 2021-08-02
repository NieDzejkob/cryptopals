from utils import *

with open('input7.txt', 'r') as f:
    ct = b64decode(f.read())

cipher = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
print(cipher.decrypt(ct).decode())
