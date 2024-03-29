### PROJECT 1 : PSU-CRYPT

#### ROBIN SU
#### CS 585
#### Winter 2021
  
<br/>

### Description
This program takes standard ASCII as input, writtent to `plaintext.txt`.
Encrypted output is written to a file called `ciphertext.txt`. 

The ciphertext output writes each ciphertext block
on a new line, no '0x' appended. Padding is done with appending the appropriate number of '0's at the end of the last block to fill a full block (or just a full block of padding if the text works out to full blocks alone). 

Decrypted output is written to a file called `<ciphertext-filename>-decrypted.txt`. Decryption mode takes in a text file
of ciphertext blocks, each written on a new line, no '0x' appended.

<br/>

### Files Included
- psu-crypt.py: main program file
- block.py: block class, contains methods for block cipher algorithm
- keySchedule.py: key object class, stores and generates subkeys
- util.py: utility file to help with file input/output, whitening, and other functions
- constant.py: constant, global variables, such as the `F_TABLE`
- plaintext.txt: plaintext file input
- key.txt: key file input (80-bit key)
- ciphertext.txt: resulting ciphertext
- README.md: this file

<br/>

### To Run:

#### Encryption Mode:
```
python3 psu-crypt.py -f <file_to_encrypt> -k <key_text_file>
```

#### Decryption Mode:
```
python3 psu-crypt.py -d -f <file_to_decrypt> -k <key_text_file>
```