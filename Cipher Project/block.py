import constant as c
import util
import keySchedule as ks

class Block:
    key = ''
    #key object
    keySchedule = None
    inputBytes = b''
    outputBytes = ""
    _rVals = []
    _rValsNew = []
    lastBlockPadded = False
    
    def __init__(self, plainBytes, keyObj, decrypt=False):
        self.inputBytes = plainBytes
        self.keySchedule = keyObj

    def fFunction(self, round):
        T0 = self.gPermutation(self._rVals[0], round, 0)
        T1 = self.gPermutation(self._rVals[1], round, 4)
        round_keys = self.keySchedule.keys[round]
        F0 = (T0 + (2 * T1) + util.concatKeys(round_keys[8], round_keys[9])) % (2**16)
        F1 = ((2 * T0) + T1 + util.concatKeys(round_keys[10], round_keys[11])) % (2**16)
        return F0, F1

    # g3 = Ftable(g2 ^ K(Round * 4 + x)) ^ g1
    def gFunc(self, g1, g2, roundKey):
        ft1 = g2 ^ roundKey
        ftable_output1 = c.F_TABLE[ft1 // (2**4)][ft1 % (2 ** 4)]
        g3 = ftable_output1 ^ g1
        return g3
        
    # return hex string of concat(g5, g6)
    def gPermutation(self, word, round, TVal):
        round_keys = self.keySchedule.keys[round]
        gVals = []
        if TVal == 0:
            key_index = 0
        else:
            key_index = 4     
        g1 = word // (16 ** 2)
        g2 = word % (16 ** 2)
        gVals = [g1, g2]

        for g in range(4):
            gVal = self.gFunc(gVals[g], gVals[g+1], round_keys[key_index])
            gVals.append(gVal)
            key_index += 1
        output = util.concatKeys(gVals[4], gVals[5])
        return output    

    # xor and swap before next round
    def swap(self, F0, F1):
        newR0 = F0 ^ self._rVals[2]
        newR1 = F1 ^ self._rVals[3]
        newR2 = self._rVals[0]
        newR3 = self._rVals[1]
        self._rValsNew = [newR0, newR1, newR2, newR3]

   # final swap before whitening 
    def finalSwap(self):
        y0 = self._rVals[2]
        y1 = self._rVals[3]
        y2 = self._rVals[0]
        y3 = self._rVals[1]
        self._rVals = [y0, y1, y2, y3]

    # encrypt block with key over 20 rounds
    def encrypt(self):
        self._rVals = util.whitening(int(self.inputBytes.hex(), 16), self.keySchedule.masterKey)
        for round in range(c.ROUNDS):
            F0, F1 = self.fFunction(round)
            self.swap(F0, F1)
            self._rVals = self._rValsNew
            self._rValsNew = []
        self.finalSwap()
        encryptBytes = util.concatHexWords(self._rVals)
        self._cipherVals = util.whitening(encryptBytes, self.keySchedule.masterKey)
        # concatenate 4 cipher words to get final cipherblock
        self.outputBytes = hex(util.concatHexWords(self._cipherVals))[2::]
        while len(self.outputBytes) < c.BLOCK_HEX_CHARS:
            self.outputBytes = '0' + self.outputBytes
    
    def decrypt(self):
        self._rVals = util.whitening(int(self.inputBytes, 16), self.keySchedule.masterKey)
        for round in range(c.ROUNDS):
            F0, F1 = self.fFunction((c.ROUNDS-1) - round)
            self.swap(F0, F1)
            self._rVals = self._rValsNew
            self._rValsNew = []
        self.finalSwap()
        decryptBytes = util.concatHexWords(self._rVals)  
        plainVals = util.whitening(decryptBytes, self.keySchedule.masterKey)
        self.outputBytes = hex(util.concatHexWords(plainVals))[2::]
        while len(self.outputBytes) < c.BLOCK_HEX_CHARS:
            self.outputBytes = '0' + self.outputBytes


        
