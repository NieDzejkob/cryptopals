from utils import *

with open('input8.txt', 'r') as f:
    for line in f:
        ct = bytes.fromhex(line)
        if len(set(blocks(ct))) < len(ct)//16:
            print(line)
