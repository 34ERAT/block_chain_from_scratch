import hashlib


def hashGenerator(data):
    result = hashlib.sha256(data.encode())
    return result.hexdigest()


class Block:
    def __init__(self, data, hash, prev_hash):
        self.data = data
        self.hash = hash
        self.prev_hash = prev_hash


class MyBlockchain:
    def __init__(self):
        hashLast = hashGenerator("last_gen")
        hashfirst = hashGenerator("first_gen")

        genesis = Block("first_gen", hashfirst, hashLast)
        self.chain = [genesis]

    def add_block(self, data):
        prev_hash = self.chain[-1].hash
        hash = hashGenerator(data + prev_hash)
        block = Block(data, hash, prev_hash)
        self.chain.append(block)


blck = MyBlockchain()
blck.add_block("A")
blck.add_block("B")
blck.add_block("c")
blck.add_block("D")

for block in blck.chain:
    print(block.__dict__)
