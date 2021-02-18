import block 

# block (bytes) as an integer
def getWords(block):
    words = [0,0,0,0]
    remainder = block
    for i in range(4):
        word = remainder % (16 ** 4)
        # insert into array starting from low order bits
        words[3-i] = word
        remainder //= (16 ** 4)
    return words

# xor each 4 words with the high 64 bits of the key
def whitening(block, key):
    rVals = []
    words = getWords(block)
    whiteningKey = key // (16 ** 4)
    keyWords = getWords(whiteningKey)
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

def splitBlocks(plainText):
    blocks = []
    numBlocks = len(plainText) // 8
    for i in range(numBlocks):
        start = i * 8
        stop = (i * 8) + 8
        blocks.append(plainText[start:stop])
    return blocks

def pad(plainText):
    padding = len(plainText) % c.BLOCK_SIZE_BYTES
    if padding != 0 :
        pad = b'\x00' * (c.BLOCK_SIZE_BYTES - padding)
        plainText += pad
    elif padding == 0:
        pad = b'\x00' * c.BLOCK_SIZE_BYTES
        plainText += pad
    return plainText

def bytesToASCII(hexStr):
        plainBytes = bytes.fromhex(hexStr)
        plainText = plainBytes.decode()
        return plainText

def readFile(file):
    plainText = b''
    with open(file, 'rb') as f:
        block = f.read(c.BLOCK_SIZE_BYTES)
        while block != b'':
            plainText += block
            block = f.read(c.BLOCK_SIZE_BYTES)
    return plainText 