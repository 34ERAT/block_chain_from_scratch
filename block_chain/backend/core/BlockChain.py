from block_chain.backend.core.Block import Block
from block_chain.backend.core.BlockHeader import BlockHeader
import sys
from block_chain.backend.core.DataBase.DataBase import BlockChainDB
from block_chain.backend.core.Tx import CoibaseTx
from block_chain.backend.util.util import hash256
import time
import json


sys.path.append("/home/huble/Projects/block_chain_from_scratch/")

ZERO_HASH = "o" * 65
VERSION = 1


class BlockChain:
    def __init__(self):
        # self.chain = []
        self.GenesisBlock()

    def WriteOnDisk(self, Block):
        pass
        blockchaindb = BlockChainDB()
        blockchaindb.write(Block)

    def get_last_block(self):
        blockchaindb = BlockChainDB()
        return blockchaindb.LastBlock()

    def GenesisBlock(self):
        BlockHeight = 0
        PrevBlockHash = ZERO_HASH
        self.addBlock(BlockHeight, PrevBlockHash)

    def addBlock(self, BlockHeight, PrevBlockHash):
        timestamp = int(time.time())
        # Transaction = f"codies Alert sent {BlockHeight} Bitcoins to joe"
        coinbase_instance = CoibaseTx(BlockHeight)
        coinbaseTx = coinbase_instance.CoibaseTransaction()
        markleRoot = coinbaseTx.TxId
        bits = "ffff001f"
        blockheader = BlockHeader(VERSION, PrevBlockHash, markleRoot, timestamp, bits)
        blockheader.mine()

        self.WriteOnDisk(
            [
                Block(
                    BlockHeight, 1, blockheader.__dict__, 1, coinbaseTx.to_dict()
                ).__dict__
            ]
        )
        # print(json.dumps(self.chain))

    def main(self):
        while True:
            lastBlock = self.get_last_block()
            BlockHeight = lastBlock["Height"] + 1
            PrevBlockHash = lastBlock["BlockHeader"]["BlockHash"]
            self.addBlock(BlockHeight, PrevBlockHash)


if __name__ == "__main__":
    blockchain = BlockChain()
    blockchain.main()
