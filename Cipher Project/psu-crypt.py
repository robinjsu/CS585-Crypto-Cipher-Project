import argparse as ap
import keySchedule as ks
import block as b
import constant as c
import util


def parseArgs():
    parser = ap.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help="Name of file to encrypt/decrypt")
    parser.add_argument("-k", "--key", type=str, required=True, help="text file with key in hex")
    parser.add_argument("-d", "--decrypt", action='store_true', help="(optional) flag to indicate decryption mode")
    args = parser.parse_args()
    return args.file, args.key, args.decrypt
    
def encryptText(txtFile, keySched):
    cipherTextBlocks = []
    plainText = util.pad(util.readFile(txtFile))
    blocks = util.splitBlocks(plainText)
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
    plainText = util.bytesToASCII(hexString)
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