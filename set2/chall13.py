from utils import *

cipher = AES.new(urandom(16), AES.MODE_ECB)

def parse_cookie(cookie):
    result = {}
    for part in cookie.split(b'&'):
        k, v = part.split(b'=')
        result[k] = v
    return result

def profile_for(email):
    assert '=' not in email and '&' not in email
    return f'email={email}&uid=10&role=user'.encode()

def make_profile(email):
    return cipher.encrypt(pad(profile_for(email)))

def check_profile(ct):
    return parse_cookie(unpad(cipher.decrypt(ct)))[b'role'] == b'admin'

admin_and_junk = make_profile('A' * 10 + 'admin')[16:32]

before_role = 'email=&uid=10&role='
pre_role = make_profile('A' * (32 - len(before_role)))[:32]
eq_user = make_profile('A' * (32 - len(before_role[:-1])))[32:]

cookie = pre_role + admin_and_junk + eq_user
assert check_profile(cookie)
