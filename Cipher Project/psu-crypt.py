import argparse as ap
import keySchedule as ks
import block as b
import constant as c

key = ''
padded = False

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
        block = f.read(c.BLOCK_HEX_CHARS)
        while block != b'':
            plainText += block
            block = f.read(c.BLOCK_HEX_CHARS)
    padding = c.BLOCK_HEX_CHARS - (len(plainText) % c.BLOCK_HEX_CHARS)
    if padding > 0:
        pad = b'0' * padding
        plainText += pad
    elif padding == 0:
        pad = b'0' * c.BLOCK_HEX_CHARS
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
        block.encrypt()
        cipherTextBlocks.append("{}\n".format(block.outputBytes))
    # if block.lastBlockPadded is False:
    #     print(block.inputBytes)
    #     block.encrypt() 
    #     cipherTextBlocks.append("{}\n".format(block.outputBytes))
    return cipherTextBlocks

def decryptText(txtFile, keySched):
    plainText = ""
    with open(txtFile, 'r') as f:
        inputBytes = f.readline()
        block = b.Block(inputBytes[:-1], keySched, decrypt=True)
        while block.inputBytes != "":
            block.decrypt()
            plainText += "{}".format(block.plainText)
            inputBytes = f.readline()
            block = b.Block(inputBytes[:-1], keySched, decrypt=True)
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

    # encrypt
    if decrypt == False:
        print("encrypting...")
        cipherTextBlocks = encryptText(txtFile, keySched)
        print(cipherTextBlocks)
        encryptedFile = "ciphertext.txt"
        with open(encryptedFile, 'w') as f:
            f.writelines(cipherTextBlocks)
            f.close()
    # decrypt        
    else:
        print("decrypting...")
        keySched.reverseKeySchedule()
        plainText = decryptText(txtFile, keySched)
        print(plainText)
        decryptedFile = txtFile[:-4:] + "-decrypted.txt"
        with open(decryptedFile, 'w') as f:
            f.writelines(plainText)
            f.close()
        print("\n\n{} decrypted. plaintext written to {}.".format(txtFile, decryptedFile))

if __name__ == "__main__":
    main()