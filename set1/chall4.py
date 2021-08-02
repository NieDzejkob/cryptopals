from utils import englishness
from chall3 import break_onexor

cts = []
with open('input4.txt', 'r') as f:
    for line in f:
        cts.append(bytes.fromhex(line.strip()))

pts = map(break_onexor, cts)
pt = min(pts, key=englishness)
print(pt)
