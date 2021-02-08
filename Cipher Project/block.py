import constant as c

class Block:
    plainBytes = b''
    cipherBytes = ""

    def __init__(self, plainBytes):
        self.plainBytes = plainBytes
    

    def pad(self):
        if len(self.plainBytes) < c.BLOCK_SIZE_BYTES:
            for i in range(8-len(self.plainBytes)):
                self.plainBytes += b'0'
        self.plainBytes
