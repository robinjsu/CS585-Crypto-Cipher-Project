import argparse as ap
import keySchedule as ks
import block as b
import constant as c

# set commmand line arguments with flags
# read argv
# read in 64 bits at a time? read in entire file and process 64 bits at a time?
# 0xabcdef0123456789abcd
key = ''
# key schedule is global
# keySched = ks.KeySchedule()

def parseArgs():
    parser = ap.ArgumentParser()
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-k", "--key", type=str)
    parser.add_argument("-d", "--decrypt", action='store_true')
    args = parser.parse_args()
    return args.file, args.key, args.decrypt

def readFile(file):
    plainText = b''
    with open(file, 'rb') as f:
        block = f.read(c.BLOCK_SIZE_BYTES)
        while block != b'':
            plainText += block
            block = f.read(c.BLOCK_SIZE_BYTES)
    padding = c.BLOCK_SIZE_BYTES - (len(plainText) % c.BLOCK_SIZE_BYTES)
    if padding > 0:
        pad = b'0' * padding
        plainText += pad
    elif padding == 0:
        pad = b'0' * c.BLOCK_SIZE_BYTES
        plainText += pad
    print(plainText)
    return plainText

def splitBlocks(plainText):
    blocks = []
    numBlocks = len(plainText) // 8
    for i in range(numBlocks):
        start = i * 8
        stop = (i * 8) + 8
        blocks.append(plainText[start:stop])
    return blocks

    

def encryptText(txtFile, keySched):
    cipherTextBlocks = []
    plainText = readFile(txtFile)
    blocks = splitBlocks(plainText)
    # read in textfile as bytes
    for bl in blocks:
        block = b.Block(bl, keySched)
    # while block.inputBytes != b'00000000':
        # print(block.inputBytes)
        block.encrypt()
        cipherTextBlocks.append("{}\n".format(block.outputBytes))
        # block = b.Block(f.readline(c.BLOCK_SIZE_BYTES), keySched)
    # if block.lastBlockPadded is False:
    #     print(block.inputBytes)
    #     block.encrypt() 
    #     cipherTextBlocks.append("{}\n".format(block.outputBytes))
    # f.close()
    return cipherTextBlocks

def decryptText(txtFile, keySched):
    plainText = ""
    with open(txtFile, 'r') as f:
        block = b.Block(f.readline(18), keySched, decrypt=True)
        # strip newline character
        block.inputBytes = block.inputBytes
        print(type(block.inputBytes))
        while block.inputBytes != "":
            block.decrypt()
            plainText += "{}".format(block.plainText)
            block = b.Block(f.readline(18), keySched, decrypt=True)
            block.inputBytes = block.inputBytes    
        f.close()    
    return plainText


def main():
    # parse command line arguments
    txtFile, key, decrypt = parseArgs()
    with open(key, 'r') as f:
        key = f.readline()
        f.close()
    # instantiate key object
    keySched = ks.KeySchedule(int(key, 16))
    # generate key schedule
    keySched.keyGen()
    if decrypt == False:
        cipherTextBlocks = encryptText(txtFile, keySched)
        print(cipherTextBlocks)
        encryptedFile = txtFile[:-4:] + "-encrypted.txt"
        with open(encryptedFile, 'w') as f:
            f.writelines(cipherTextBlocks)
            f.close()
    else:
        keySched.reverseKeySchedule()
        plainText = decryptText(txtFile, keySched)
        print(plainText)
        decryptedFile = txtFile[:-4:] + "-decrypted.txt"
        with open(decryptedFile, 'w') as f:
            f.writelines(plainText)
            f.close()
        print("{} decrypted, plaintext written to {}.".format(txtFile, decryptedFile))

if __name__ == "__main__":
    main()
    # plain = readFile('testfile.txt')
    # blocks = splitBlocks(plain)
    # print(blocks)