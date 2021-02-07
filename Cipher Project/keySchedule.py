import constant

class KeySchedule:

    keySchedule = []
    masterKey = None

    def __init__(self, key):
        self.masterKey = key

    # returns 80-bit key as integer 
    def keyShift(self, key):
        # left shift and subtract largest factor of 2
        if (key >= pow(2, (constant.BITS - 1))):
            
            key = (key << 1) + 1
            key -= pow(2, constant.BITS)
        else:
            key = key << 1
        # print(hex(key))
        # print(bin(key))
        # print string with only the hex digits
        return key

    def calcSubKey(self, roundNum, counter, keyStr):
        keysK = []
        # if the key has 4 or more leading zeroes, they will get dropped after the shift
        # this will re-append them to the front of the hex string
        while len(keyStr) < 20:
            keyStr = str(0) + keyStr
        # print(keyStr)
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
        for k in range(constant.NUM_SUBKEYS):
            newKey = self.keyShift(newKey)
            # convert int to hex string to get keys
            subkey = self.calcSubKey(roundNum, k, hex(newKey)[2::])
            roundKeys.append(subkey)
        # return list of 12 keys
        return roundKeys, newKey

    # generate all subkeys for all 20 rounds
    def getKeySchedule(self):
        roundKey = self.masterKey
        for round in range(constant.ROUNDS):
            roundKeys, roundKey = self.getRoundKeys(round, roundKey)
            # print(roundKeys)
            self.keySchedule.append(roundKeys)
        # for round in self.keySchedule:
            # print(round)
        return self.keySchedule
