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
    args = parser.parse_args()
    return args.file, args.key 

def main():
    # parse command line arguments
    txtFile, key = parseArgs()
    # instantiate key object
    keySched = ks.KeySchedule(int(key, 16))
    # generate key schedule
    keySched.keyGen()
    # print(keySched.keySchedule)
    with open(txtFile, 'rb') as f:
        block = b.Block(f.readline(8), keySched)
        plain = block.plainBytes
        print("plaintext block: ", plain)
        # while block != b'':
            # plain = block.plainBytes
        block.encrypt()
        # block = b.Block(f.readline(8), keySched.masterKey)
        f.close()
    # print(keySched.keySchedule)


    

if __name__ == "__main__":
    main()