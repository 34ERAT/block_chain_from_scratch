from hashlib import sha256
from Crypto.Hash import RIPEMD160
from math import log

from block_chain.backend.core.EllepticCurve.EllepticCurve import BASE58_ALPHABET


def hash256(s):
    # Two rounds of SHA256
    return sha256(sha256(s).digest()).digest()


def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()


def bytes_needed(n):
    if n == 0:
        return 1

    return int(log(n, 256)) + 1


def int_to_little__endian(n, length):
    """init to int_to_little__endian  takes and inter aga returns the little-endian sequence of length"""
    # print(f"Value of n: {n}, Expected length: {length}")
    return n.to_bytes(length, "little")


def little_endian_to_int(b):
    """takes  a byte  sequence  and  returns  an interger"""
    return int.from_bytes(b, "little")


def decode_base58(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)

    combined = num.to_bytes(25, byteorder="big")
    checksum = combined[-4:]

    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(f"bad Address {checksum} {hash256(combined[:-4][:4])}")
    return combined[1:-4]


def encode_varint(i):
    """encode an interger as a varint"""
    if i < 0xFD:
        return bytes([i])
    elif i < 0x10000:
        return b"\xfd" + int_to_little__endian(i, 2)
    elif i < 0x100000000:
        return b"\xfe" + int_to_little__endian(i, 4)
    elif i < 0x10000000000000000:
        return b"\xff" + int_to_little__endian(i, 8)
    else:
        raise ValueError("interger too larger : {}".format(i))
