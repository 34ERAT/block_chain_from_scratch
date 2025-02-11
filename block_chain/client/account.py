from block_chain.backend.core.EllepticCurve.EllepticCurve import (
    BASE58_ALPHABET,
    PrivateKey,
    Sha256Point,
)
import secrets

from block_chain.backend.util.util import hash160, hash256


class account:
    def createkeys(self):
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        G = Sha256Point(Gx, Gy)
        PrivateKey = secrets.randbits(256)
        # print(f"Private key is {PrivateKey}")
        uncompressedPublickey = PrivateKey * G
        xpoint = uncompressedPublickey.x
        ypoint = uncompressedPublickey.y
        if ypoint.num % 2 == 0:
            compressskey = b"\x02" + xpoint.num.to_bytes(32, "big")
        else:
            compressskey = b"\x03" + ypoint.num.to_bytes(32, "big")
        hsh160 = hash160(compressskey)
        # prefix for Mainnet
        main_prefix = b"\x00"
        newAdress = main_prefix + hsh160

        # check sum
        checksum = hash256(newAdress)[:4]
        newAdress = newAdress + checksum
        count = 0
        for c in newAdress:
            if c == 0:
                count += 1
            else:
                break
        num = int.from_bytes(newAdress, "big")
        prefix = "1" * count
        result = ""
        while num > 0:
            num, mod = divmod(num, 58)
            result = BASE58_ALPHABET[mod] + result

        PublicAddress = prefix + result
        print(f"Private key {PrivateKey}")
        print(f"public address key {PublicAddress}")


if __name__ == "__main__":
    acct = account()
    acct.createkeys()
