from block_chain.backend.core.Script import Script
from block_chain.backend.util.util import (
    bytes_needed,
    decode_base58,
    int_to_little__endian,
    little_endian_to_int,
)

ZERO_HASH = b"\0" * 32
REWARD = 50
PRIVATE_KEY = (
    "111491678717360410153283178954333886687375818537248469595805407557079361456834"
)
MINER_ADDRESS = "19N7AvhwpPpF5RqBfX7gLd1HmkUC2du44H"


class CoibaseTx:
    def __init__(self, BlockHeight):
        self.BlockHeightInLittleIndian = int_to_little__endian(
            BlockHeight, bytes_needed(BlockHeight)
        )

    def CoibaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xFFFFFFFF
        tx_ins = []
        tx_ins.append(TxIn(prev_tx, prev_index))
        tx_ins[0].script_sig.cmds.append(self.BlockHeightInLittleIndian)
        tx_outs = []
        target_amount = REWARD * 100000000
        target_h160 = decode_base58(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_h160)
        tx_outs.append(TxOut(amount=target_amount, script_pubkey=target_script))
        return TX(1, tx_ins, tx_outs, 0)


class TX:
    def __init__(self, version, tx_ins, tx_outs, locktime):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime

    def is_coinbase(self):
        """
        #checks that their is exactily one input
        # grab  the first  input and  check  if  the prev_tx  is b'\x00'*32
        # check that the  first  input  prev_index  is 0xFFFFFFFF
        """
        if len(self.tx_ins) != 1:
            return False
        first_input = self.tx_ins[0]
        if first_input.prev_tx != "\x00" * 32:
            return False

        if first_input.prev_index != 0xFFFFFFFF:
            return False
        return True

    def to_dict(self):
        """
        Convert coibase transaction
        #convert  prev_tx  hash  in  hex from bytes_neede
        #convert Blockheight  in hex which is stored  in script signature
        """
        if self.is_coinbase():
            self.tx_ins[0].prev_tx = self.tx_ins[0].prev_tx.hex()
            self.tx_ins[0].script_sig.cmds[0] = little_endian_to_int(
                self.tx_ins[0].script_sig.cmds[0]
            )
            self.tx_ins[0].script_sig = self.tx_ins[0].script_sig.__dict__
        self.tx_ins[0] = self.tx_ins[0].__dict__

        """
        Convert  transaction  OUtput  to dict 
        #if  there are  numbers  we don't  need  to do anything 
        #if  values are  in bytes  convert to hex
        # loop Through  all the TxOut Objects and  convert  them  into dict
        """
        self.tx_outs[0].script_pubkey.cmds[2] = (
            self.tx_outs[0].script_pubkey.cmds[2].hex()
        )
        self.tx_outs[0].script_pubkey = self.tx_outs[0].script_pubkey.__dict__
        self.tx_outs[0] = self.tx_outs[0].__dict__
        # print(f"i am  a dict now {self.__dict__}")

        return self.__dict__


class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xFFFFFFFF):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig

        self.sequence = sequence


class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey
