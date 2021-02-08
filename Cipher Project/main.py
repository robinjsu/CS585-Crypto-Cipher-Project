import argparse as ap
import keySchedule as ks
import block as b
import whitening as w
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
    args = parser.parse_args()
    return args.file, args.key 

def generateKeys(keySched):
# instantiate key class
    # generate  for all 20 rounds
    keySched.getKeySchedule()


def main():
    txtFile, key = parseArgs()
    keySched = ks.KeySchedule(int(key, 16))
    generateKeys(keySched)
    # print(keySched.keySchedule)
    with open(txtFile, 'rb') as f:
        block = b.Block(f.readline(8))
        plain = block.plainBytes
        while block != b'':
            # plain = block.plainBytes
            block.pad()
            print(block.plainBytes)      
            # w.whitening(text, key)
            block = f.readline(8)
        f.close()
    # print(keySched.keySchedule)


    

if __name__ == "__main__":
    main()