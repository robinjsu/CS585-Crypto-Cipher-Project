import constant as c

class KeySchedule:

    keys = []
    masterKey = None
    subKey = None

    def __init__(self, key):
        self.masterKey = key

    # returns 80-bit key as integer 
    def keyShift(self, key):
        # left shift and subtract largest factor of 2
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
        # print("key str: ", keyStr)
        for i in range(10):
            keysK.append(keyStr[i*2] + keyStr[(i*2)+1])
        # print(keysK)
        indx = ((roundNum * 4) + (counter % 4)) % 10
        indx = 9 - indx
        # print(keysK[indx])
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
            # print("round key: {}, round: {} ".format(hex(roundKey), round))
            self.keys.append(roundKeys)
        # save last subkey value to use for decryption
        self.subKey = roundKey
        # convert round keys from string to int
        for r in range(c.ROUNDS):
            for k in range(c.NUM_SUBKEYS):
                self.keys[r][k] = (int(self.keys[r][k], 16))   
        return self.keys

    def reverseKeySchedule(self):
        newKeySchedule = []
        for r in range(c.ROUNDS):
            subkeys = []
            for k in range(c.NUM_SUBKEYS):
                subkeys.append(self.keys[(c.ROUNDS-1)-r][k])
            newKeySchedule.append(subkeys)
        
        self.keys = newKeySchedule        