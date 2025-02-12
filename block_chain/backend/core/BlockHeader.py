from block_chain.backend.util.util import hash256


class BlockHeader:
    def __init__(self, version, prevBlockHash, merkelRoot, timestamp, bits):
        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkelRoot = merkelRoot
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.BlockHash = ""

    def mine(self):
        while (self.BlockHash[0:4]) != "0000":
            self.BlockHash = hash256(
                (
                    str(self.version)
                    + self.prevBlockHash
                    + self.merkelRoot
                    + str(self.timestamp)
                    + self.bits
                    + str(self.nonce)
                ).encode()
            ).hex()
            self.nonce += 1
            print(f"mining started {self.nonce}", end="\r")

        print(f"you have mined the block successfully {self.nonce}")
