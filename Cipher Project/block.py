import constant as c
import whitening as w
import keySchedule as ks

class Block:
    key = ''
    #key schedule object
    keySchedule = None
    plainBytes = b''
    cipherBytes = ""
    _rVals = []
    _cipherVals = []
    

    def __init__(self, plainBytes, keyObj):
        self.plainBytes = plainBytes
        self.pad()
        self.keySchedule = keyObj

    def generateKeys(self):
        # generate  for all 20 rounds
        self.keySchedule.keyGen()

    def fFunction(self):
        print('Implement Me')

    # return int
    # g3 = Ftable(g2 ^ K(Round * 4 + x)) ^ g1
    def gFunc(self, g1, g2, roundKey):
        ft1 = g2 ^ roundKey
        # print(hex(ft1))
        ftable_output1 = c.F_TABLE[ft1 // (2**4)][ft1 % (2 ** 4)]
        # print(hex(ftable_output1))
        g3 = ftable_output1 ^ g1
        # print("g3: ", g3)
        return g3
        
    # return hex string of concat(g5, g6)
    def gPermutation(self, word, round, TVal):
        round_keys = []
        gVals = []
        # convert round keys to hex from string
        for k in range(c.NUM_SUBKEYS):
            round_keys.append(int(self.keySchedule.keys[round][k], 16))
        if TVal == 0:
            key_index = 0
        else:
            key_index = 4

        print("round keys: ", round_keys)
        g1 = word // (16 ** 2)
        # print("g1: ", hex(g1))
        g2 = word % (16 ** 2)
        # print("g2: ", hex(g2))
        gVals = [g1, g2]
        for g in range(4):
            print("round key: ", hex(round_keys[key_index]))
            g = self.gFunc(gVals[g], gVals[g+1], round_keys[key_index])
            gVals.append(g)
            key_index += 1
        output = hex(gVals[4]) + hex(gVals[5])[2::]
        return output    

    def swap(self):
        print('Implement Me')
      
    
    def psu_crypt(self):
        self._rVals = w.whitening(self.plainBytes, self.keySchedule.masterKey)
        T0 = self.gPermutation(self._rVals[0], 0, 0)
        print("T0: ", T0)
        T1 = self.gPermutation(self._rVals[1], 0, 4)
        print("T1: ", T1)
        # F0 and F1
        # last whitening step
        #self._cipherVals = w.whitening(self.interBytes, self.key)
        # concatenate 4 cipher words to get final cipherblock
        
    def pad(self):
        if len(self.plainBytes) < c.BLOCK_SIZE_BYTES:
            for i in range(8-len(self.plainBytes)):
                self.plainBytes += b'0'
        self.plainBytes
