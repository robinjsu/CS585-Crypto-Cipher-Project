import argparse as ap
import keySchedule as ks
import block as b
import constant as c


def parseArgs():
    parser = ap.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help="Name of file to encrypt/decrypt")
    parser.add_argument("-k", "--key", type=str, required=True, help="text file with key in hex")
    parser.add_argument("-d", "--decrypt", action='store_true', help="(optional) flag to indicate decryption mode")
    args = parser.parse_args()
    return args.file, args.key, args.decrypt

def readFile(file):
    plainText = b''
    with open(file, 'rb') as f:
        block = f.read(c.BLOCK_SIZE_BYTES)
        while block != b'':
            plainText += block
            block = f.read(c.BLOCK_SIZE_BYTES)
    return plainText       

def pad(plainText):
    padding = len(plainText) % c.BLOCK_SIZE_BYTES
    if padding != 0 :
        pad = b'\x00' * (c.BLOCK_SIZE_BYTES - padding)
        plainText += pad
    elif padding == 0:
        pad = b'\x00' * c.BLOCK_SIZE_BYTES
        plainText += pad
    return plainText

def splitBlocks(plainText):
    blocks = []
    numBlocks = len(plainText) // 8
    for i in range(numBlocks):
        start = i * 8
        stop = (i * 8) + 8
        blocks.append(plainText[start:stop])
    return blocks

def bytesToASCII(hexStr):
        plainBytes = bytes.fromhex(hexStr)
        plainText = plainBytes.decode()
        return plainText

def encryptText(txtFile, keySched):
    cipherTextBlocks = []
    plainText = pad(readFile(txtFile))
    blocks = splitBlocks(plainText)
    for bl in blocks:
        block = b.Block(bl, keySched)
        block.encrypt()
        cipherTextBlocks.append("{}\n".format(block.outputBytes))
    return cipherTextBlocks

def decryptText(txtFile, keySched):
    hexString = ""
    with open(txtFile, 'r') as f:
        inputBytes = f.readline()
        block = b.Block(inputBytes[:-1], keySched, decrypt=True)
        while block.inputBytes != '':
            block.decrypt()
            hexString += block.outputBytes
            inputBytes = f.readline()
            block = None
            block = b.Block(inputBytes[:-1], keySched, decrypt=True)
        f.close()
    plainText = bytesToASCII(hexString)
    return plainText


def main():
    txtFile, key, decrypt = parseArgs()
    with open(key, 'r') as f:
        key = f.readline()
        f.close()
    keySched = ks.KeySchedule(int(key, 16))
    # generate key schedule
    keySched.keyGen()
    # encrypt
    if decrypt == False:
        print("encrypting...")
        cipherTextBlocks = encryptText(txtFile, keySched)
        encryptedFile = "ciphertext.txt"
        with open(encryptedFile, 'w') as f:
            f.writelines(cipherTextBlocks)
            f.close()
    # decrypt        
    else:
        print("decrypting...")
        plainText = decryptText(txtFile, keySched)
        decryptedFile = txtFile[:-4:] + "-decrypted.txt"
        with open(decryptedFile, 'w') as f:
            f.writelines(plainText)
            f.close()
        print("...\n{} decrypted. plaintext written to {}.\n".format(txtFile, decryptedFile))

if __name__ == "__main__":
    main()