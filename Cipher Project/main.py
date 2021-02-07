import argparse as ap
import keySchedule as ks
import whitening as w

# set commmand line arguments with flags
# read argv
# read in 64 bits at a time? read in entire file and process 64 bits at a time?

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
    print(keySched.keySchedule)
    with open(txtFile) as f:
        text = f.read()
        print(text)
    # print(keySched.keySchedule)


    

if __name__ == "__main__":
    main()