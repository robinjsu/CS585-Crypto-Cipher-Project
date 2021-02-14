import constant as c
import util
import keySchedule as ks

class Block:
    key = ''
    #key schedule object
    keySchedule = None
    inputBytes = b''
    outputBytes = ""
    _rVals = []
    _rValsNew = []
    lastBlockPadded = False
    # _cipherVals = []
    

    def __init__(self, plainBytes, keyObj, decrypt=False):
        self.inputBytes = plainBytes
        if decrypt == False:
            self.pad()
        self.keySchedule = keyObj

    def fFunction(self, round):
        T0 = self.gPermutation(self._rVals[0], round, 0)
        print("T0: ", hex(T0))
        T1 = self.gPermutation(self._rVals[1], round, 4)
        print("T1: ", hex(T1))
        round_keys = self.keySchedule.keys[round]
        # F0 = (T0 + 2T1 + concat(k8, k9)) % BLOCK_SIZE_BITS
        F0 = (T0 + (2 * T1) + util.concatKeys(round_keys[8], round_keys[9])) % (2**16)
        # F1 = (2T0 + T1 + concat(k10, k11)) % BLOCK_SIZE_BITS
        F1 = ((2 * T0) + T1 + util.concatKeys(round_keys[10], round_keys[11])) % (2**16)
        print(hex(F0), hex(F1))
        return F0, F1

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
        round_keys = self.keySchedule.keys[round]
        gVals = []
        # # convert round keys to hex from string
        # for k in range(c.NUM_SUBKEYS):
        #     round_keys.append(int(self.keySchedule.keys[round][k], 16))
        if TVal == 0:
            key_index = 0
        else:
            key_index = 4
            
        # print("round keys")
        # for k in round_keys:
        #     print(hex(k))
        
        g1 = word // (16 ** 2)
        print("g1: ", hex(g1))
        g2 = word % (16 ** 2)
        print("g2: ", hex(g2))
        gVals = [g1, g2]
        for g in range(4):
            # print("round key: ", hex(round_keys[key_index]))
            gVal = self.gFunc(gVals[g], gVals[g+1], round_keys[key_index])
            print("g" + str(g+3) + ": " + hex(gVal))
            gVals.append(gVal)
            key_index += 1
        output = util.concatKeys(gVals[4], gVals[5])
        print("gPermutation output: ", hex(output))
        return output    

    def swap(self, F0, F1):
        newR0 = F0 ^ self._rVals[2]
        newR1 = F1 ^ self._rVals[3]
        newR2 = self._rVals[0]
        newR3 = self._rVals[1]
        self._rValsNew.append(newR0)
        self._rValsNew.append(newR1)
        self._rValsNew.append(newR2)
        self._rValsNew.append(newR3)

        print(hex(newR0), hex(newR1), hex(newR2), hex(newR3))      
    
    def finalSwap(self):
        y0 = self._rVals[2]
        y1 = self._rVals[3]
        y2 = self._rVals[0]
        y3 = self._rVals[1]
        self._rVals = [y0, y1, y2, y3]


    def encrypt(self):
        self._rVals = util.whitening(self.inputBytes, self.keySchedule.masterKey)
        #rVals are R0 R1 R2 R3
        for round in range(20):
            print("****ROUND: {}******".format(round))
            F0, F1 = self.fFunction(round)
            self.swap(F0, F1)
            self._rVals = self._rValsNew
            self._rValsNew = []
            print("NEW R VALUES: {}".format(self._rVals))
        
        self.finalSwap()
        encryptBytes = util.concatHexWords(self._rVals)
        # last whitening step
        self._cipherVals = util.whitening(encryptBytes, self.keySchedule.masterKey, integer=True)
        # for i in self._cipherVals:
        #     print("cipherVals: ", hex(i)) 
        # concatenate 4 cipher words to get final cipherblock
        self.outputBytes = hex(util.concatHexWords(self._cipherVals))
        print(self.outputBytes)

        
    def decrypt(self):
        print("input: {}".format(self.inputBytes))
        self._rVals = util.whitening(int(self.inputBytes, 16), self.keySchedule.masterKey, integer=True)
        # for r in self._rVals:
        #     print(hex(r))
        for round in range(1):
            print("****ROUND: {}******".format(round))
            F0, F1 = self.fFunction(round)
            self.swap(F0, F1)
            self._rVals = self._rValsNew
            self._rValsNew = []
            print("NEW R VALUES: {}".format(self._rVals))
        self.finalSwap()
        decryptBytes = util.concatHexWords(self._rVals)  
        plainVals = util.whitening(decryptBytes, self.keySchedule.masterKey, integer=True)
        self.outputBytes = hex(util.concatHexWords(self._rVals))
        print(self.outputBytes)

    def pad(self):
        if len(self.inputBytes) < c.BLOCK_SIZE_BYTES:
            self.lastBlockPadded = True
            for i in range(8-len(self.inputBytes)):
                self.inputBytes += b'0'
        # self.plainBytes
