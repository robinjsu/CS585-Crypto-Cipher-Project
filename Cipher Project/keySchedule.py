bits = 80
numOfRoundKeys = 12
counter = 0
keyList = []

# returns 80-bit key as integer type
def keyShift(key):
    # left shift and subtract largest factor of 2
    if (key >= pow(2, (bits-1))):
        
        key = (key << 1) + 1
        key -= pow(2, bits)
    else:
        key = key << 1
    print(hex(key))
    # print string with only the hex digits
    return key

def calcSubKey(roundNum, counter, keyStr):
    keysK = []
    for i in range(10):
        keysK.append(keyStr[i*2] + keyStr[(i*2)+1])
    print(keysK)
    # k = (round * 4 + counter) % 10
    indx = ((roundNum * 4) + (counter % 4)) % 10
    indx = 9 - indx
    print(keysK[indx])
    return keysK[indx] 

# loop 12 times for subkeys for single round of cipher
def getRoundKeys(roundNum, key):
    roundKeys = []
    newKey = keyShift(key)
    print(newKeyStr)
    # convert int to hex string to get keys
    calcSubKey(0, 0, hex(newKeyStr)[2::])

    # return list of 12 keys

def main():
    key = 0xabcdef0123456789abcd
    
    

if __name__ == "__main__":
    main()