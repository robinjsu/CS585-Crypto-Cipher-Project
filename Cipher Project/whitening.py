import constant
import block 

# divide up plaintext into 4 words
# divide up key into 4 words
# xor the 4 pieces together bitwise
# output R0 R1 R2 R3
# xoring with which 64 bits of the key? The high 64 bits

# key = '0xabcdef0123456789abcd'


# block (bytes) as an integer
def getWords(block, key=False):
    words = [0,0,0,0]
    blockInt = block
    # convert bytes => int representation
    if key == False:
        blockInt = int(block.hex(), 16)
    remainder = blockInt
    for i in range(4):
        print(hex(remainder))
        word = remainder % (16 ** 4)
        # insert into array starting from low order bits
        words[3-i] = word
        remainder //= (16 ** 4)
    # print(words)
    return words

# xor each 4 words with the high 64 bits of the key
def whitening(block, key):
    rVals = []
   
    # split into 4 words
    words = getWords(block)
    # split high 64 bits of key into 4 words
    whiteningKey = int(key, 16) // (16 ** 4)
    keyWords = getWords(whiteningKey, key=True)
    print(words, keyWords)

    for word in range(len(words)):
        rVals.append(words[word] ^ keyWords[word])

    # final xor'd values for 4 16-bit blocks
    for r in rVals:
        print(hex(r))


# def main():
#     whitening('security', key)

# if __name__ == "__main__":
#     main()