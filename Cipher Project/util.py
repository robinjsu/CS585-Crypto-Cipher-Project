import constant
import block 

# block (bytes) as an integer
def getWords(block, hex=False):
    words = [0,0,0,0]
    blockInt = block
    # convert bytes => int representation
    if hex == False:
        blockInt = int(block.hex(), 16)
    remainder = blockInt
    for i in range(4):
        # print(hex(remainder))
        word = remainder % (16 ** 4)
        # insert into array starting from low order bits
        words[3-i] = word
        remainder //= (16 ** 4)
    return words

# xor each 4 words with the high 64 bits of the key
# key is passed in as an int
def whitening(block, key, integer=False):
    rVals = []

    # split high 64 bits of key into 4 words
    if integer == False:
        # split into 4 words
        words = getWords(block)
    else:
        words = getWords(block, hex=True)
    whiteningKey = key // (16 ** 4)
    keyWords = getWords(whiteningKey, hex=True)

    for word in range(len(words)):
        rVals.append(words[word] ^ keyWords[word])

    return rVals

# takes two keys as ints and concats their hex representation
def concatKeys(key1, key2):
    return (key1 * 0x100) + key2

def concatHexWords(cipherBlocks):
    cipher = 0
    for word in range(4):
        cipher = (cipher * 0x10000) + cipherBlocks[word]
    # print(hex(cipher))
    return cipher