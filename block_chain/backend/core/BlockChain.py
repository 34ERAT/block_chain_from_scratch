from block_chain.backend.core.Block import Block
from block_chain.backend.core.BlockHeader import BlockHeader
import sys
from block_chain.backend.util.util import hash256
import time
import json


sys.path.append("/home/huble/Projects/block_chain_from_scratch/")

ZERO_HASH = "o" * 65
VERSION = 1


class BlockChain:
    def __init__(self):
        self.chain = []
        self.GenesisBlock()

    def GenesisBlock(self):
        BlockHeight = 0
        PrevBlockHash = ZERO_HASH
        self.addBlock(BlockHeight, PrevBlockHash)

    def addBlock(self, BlockHeight, PrevBlockHash):
        timestamp = int(time.time())
        Transaction = f"codies Alert sent {BlockHeight} Bitcoins to joe"
        markleRoot = hash256(Transaction.encode()).hex()
        bits = "ffff001f"
        blockheader = BlockHeader(VERSION, PrevBlockHash, markleRoot, timestamp, bits)
        blockheader.mine()
        self.chain.append(
            Block(BlockHeight, 1, blockheader.__dict__, 1, Transaction).__dict__
        )
        print(json.dumps(self.chain))

    def main(self):
        while True:
            lastBlock = self.chain[::-1]


if __name__ == "__main__":
    blockchain = BlockChain()
