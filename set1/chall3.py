from utils import cyclic_xor, englishness

def break_onexor(ct):
    key = min(range(256), key=lambda k: englishness(cyclic_xor(bytes([k]), ct)))
    return cyclic_xor(bytes([key]), ct)

if __name__ == '__main__':
    ct = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    print(break_onexor(ct))
