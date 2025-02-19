import secrets
import time
from block_chain.backend.core.DataBase.DataBase import AccountDB
from block_chain.backend.core.EllepticCurve.EllepticCurve import PrivateKey
from block_chain.backend.core.Script import Script
from block_chain.backend.core.Tx import TX, TxIn, TxOut
from block_chain.backend.util.util import decode_base58


class SendBTC:
    def __init__(self, fromAccount, toAccount, Amount, UTXOS):
        self.COIN = 100000000
        self.FromPublicAdress = fromAccount
        self.toAccount = toAccount
        self.Amount = Amount * self.COIN
        self.utxos = UTXOS

    def scriptPubKey(self, PublicAddress):
        h160 = decode_base58(PublicAddress)
        script_pubkey = Script().p2pkh_script(h160)
        return script_pubkey

    def getPrivateKey(self):
        AllAccounts = AccountDB().Read()
        for account in AllAccounts:
            if account["PublicAddress"] == self.FromPublicAdress:
                return account["privateKey"]

    def prepareTxOut(self):
        TxOuts = []
        to_scriptPubKey = self.scriptPubKey(self.toAccount)
        TxOuts.append(TxOut(self.Amount, to_scriptPubKey))

        """Calculate fee"""
        self.fee = self.COIN
        self.changeAmount = self.Total - self.Amount - self.fee
        TxOuts.append(TxOut(self.changeAmount, self.From_address_script_pubkey))

        return TxOuts

    def prepareTxIn(self):
        TxIns = []
        self.Total = 0

        """convert Public Address into Public Hash to find tx_outs that are locked to this hash"""
        self.From_address_script_pubkey = self.scriptPubKey(self.FromPublicAdress)
        self.fromPubKeyHash = self.From_address_script_pubkey.cmds[2]
        newutxos = {}
        try:
            while len(newutxos) < 1:
                newutxos = dict(self.utxos)
                time.sleep(2)
        except Exception as e:
            print(f"Errorin converting the Managed Dict to Normal Dict \n {e} ")

        for Txbyte in newutxos:
            if self.Total < self.Amount:
                TxObj = newutxos[Txbyte]

                for index, txout in enumerate(TxObj.txout):
                    if txout.script_pubkey.cmds[2] == self.fromPubKeyHash:
                        self.Total += txout.Amount
                        prev_tx = bytes.fromhex(TxObj.id())
                        TxIns.append(TxIn(prev_tx, index))
            else:
                break

        self.isBalanceEnough = True
        if self.Total < self.Amount:
            self.isBalanceEnough = False

        return TxIns

    def signTx(self):
        secret = self.getPrivateKey()
        priv = PrivateKey(secret=secret)
        for index, input in enumerate(self.TxIns):
            self.TxObj.sign_input(index, priv, self.From_address_script_pubkey)

        return True

    def prepareTransaction(self):
        self.TxIns = self.prepareTxIn()
        if self.isBalanceEnough:
            self.TxOuts = self.prepareTxOut()
            self.TxObj = TX(1, self.TxIns, self.TxOuts, 0)
            self.signTx()
            return True
        return False
