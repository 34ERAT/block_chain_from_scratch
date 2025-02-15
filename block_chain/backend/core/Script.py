from block_chain.backend.util.util import encode_varint, int_to_little__endian


class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

    def serialize(self):
        # initialize  what we'll send back
        result = b""
        # go through  each cmd
        for cmd in self.cmds:
            # if the cmd is  and integer , it's an opcode
            if type(cmd) is int:
                # turn the cmd into single byte interger using int_to_little_endian
                # result += int_to_little_endian(cmd,1)
                result += int_to_little__endian(cmd, 1)
            else:
                # otherwise , this is and element
                # get the length is byte
                length = len(cmd)
                # for large length into a single byte interger
                if length < 75:
                    # turn the length into a single byte interger
                    result += int_to_little__endian(length, 1)
                elif length > 75 and length < 0x100:
                    # 76 is pushdata 1
                    result += int_to_little__endian(76, 1)
                    result += int_to_little__endian(length, 1)
                elif length >= 0x100 and length <= 520:
                    # 77 is pushdata2
                    result += int_to_little__endian(77, 1)
                    result += int_to_little__endian(length, 2)
                else:
                    raise ValueError("too long an cmd")

                result += cmd
        # get the length of the whole thing
        total = len(result)
        # encode_varint the total length of the result and prepend
        return encode_varint(total) + result

    @classmethod
    def p2pkh_script(cls, h160):
        """Takes a hash160 and returns  the p2pkh  script PubKey"""
        return Script([0x76, 0xA9, h160, 0x80, 0xAC])
