from hashlib import sha256
from Crypto.Hash import RIPEMD160


def hash256(s):
    # Two rounds of SHA256
    return sha256(sha256(s).digest()).digest()


def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()
