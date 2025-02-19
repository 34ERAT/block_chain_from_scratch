import json
import os


class BaseDB:
    def __init__(self):
        self.basepath = "data"
        self.filepath = "/".join((self.basepath, self.filename))

    def Read(self):
        if not os.path.exists(self.filepath):
            print(f"File {self.filepath}  does not exists")
            return False
        with open(self.filepath, "r") as file:
            raw = file.readline()
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []
        return data

    def write(self, item):
        data = self.Read()
        if data:
            data = data + item
        else:
            data = item

        with open(self.filepath, "w") as file:
            file.write(json.dumps(data))


class BlockchainDB(BaseDB):
    def __init__(self):
        self.filename = "block_chain.json"
        super().__init__()

    def LastBlock(self):
        data = self.Read()
        if data:
            return data[-1]


class AccountDB(BaseDB):
    def __init__(self):
        self.filename = "account.json"
        super().__init__()
