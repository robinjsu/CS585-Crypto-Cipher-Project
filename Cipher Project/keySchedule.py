import constant as c

class KeySchedule:

    keys = []
    masterKey = None

    def __init__(self, key):
        self.masterKey = key

    # returns 80-bit key as integer 
    def keyShift(self, key):
        if (key >= pow(2, (c.BITS - 1))):        
            key = (key << 1) + 1
            key -= pow(2, c.BITS)
        else:
            key = key << 1
        return key

    def calcSubKey(self, roundNum, counter, keyStr):
        keysK = []
        # if the key has 4 or more leading zeroes, they will get dropped after the shift
        # this will re-append them to the front of the hex string
        while len(keyStr) < 20:
            keyStr = str(0) + keyStr
        for i in range(10):
            keysK.append(keyStr[i*2] + keyStr[(i*2)+1])
        indx = ((roundNum * 4) + (counter % 4)) % 10
        indx = 9 - indx
        return keysK[indx] 

    # generate 12 subkeys for single round of cipher
    def getRoundKeys(self, roundNum, key):
        roundKeys = []
        newKey = key
        for k in range(c.NUM_SUBKEYS):
            newKey = self.keyShift(newKey)
            # convert int to hex string to get keys
            subkey = self.calcSubKey(roundNum, k, hex(newKey)[2::])
            roundKeys.append(subkey)
        # return list of 12 keys
        return roundKeys, newKey

    # generate all subkeys for all 20 rounds
    def keyGen(self):
        roundKey = self.masterKey
        for round in range(c.ROUNDS):
            roundKeys, roundKey = self.getRoundKeys(round, roundKey)
            self.keys.append(roundKeys)
        for r in range(c.ROUNDS):
            for k in range(c.NUM_SUBKEYS):
                self.keys[r][k] = (int(self.keys[r][k], 16))   
        return self.keys       