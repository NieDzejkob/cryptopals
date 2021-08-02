from utils import xor

in1 = bytes.fromhex('1c0111001f010100061a024b53535009181c')
in2 = bytes.fromhex('686974207468652062756c6c277320657965')
expected = bytes.fromhex('746865206b696420646f6e277420706c6179')

assert xor(in1, in2) == expected
