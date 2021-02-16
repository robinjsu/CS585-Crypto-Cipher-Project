import constant
import block 

# divide up plaintext into 4 words
# divide up key into 4 words
# xor the 4 pieces together bitwise
# output R0 R1 R2 R3
# xoring with which 64 bits of the key? The high 64 bits

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
    # print("block words: {}, key words: {}".format(words, keyWords))

    for word in range(len(words)):
        rVals.append(words[word] ^ keyWords[word])
    
    # final xor'd values for 4 16-bit blocks
    # print("r values:")
    # for r in rVals:
    #     print(hex(r))

    return rVals

# takes two keys as ints and concats their hex representation
def concatKeys(key1, key2):
    return (key1 * 0x100) + key2

def concatHexWords(cipherBlocks):
    cipher = 0
    for word in range(4):
        cipher = (cipher * 0x10000) + cipherBlocks[word]
    print(hex(cipher))
    return cipher
    # print("IMPLEMENT ME")    

# def main():
#     whitening('security', key)

# if __name__ == "__main__":
#     main()