## PROJECT 1 - PSU-CRYPT

### ROBIN SU
### Winter 2021
### CS 485-585 Cryptography

#### Description
This program takes standard ASCII as input. 
Encrypted output is written to a file called ciphertext.txt. The ciphertext output writes each ciphertext block
on a new line, NOT appended with '0x'. Padding is done with appending the appropriate number of '0's at the end of the last block to fill a full block.
Decrypted output is written to a file called <ciphertext-filname>-decrypted.txt. Decryption mode takes in a text file
of ciphertext blocks, each written on a new line, NOT appended with '0x'.

### To Run:

#### Encryption Mode:
```
python3 psu-crypt.py -f <file_to_encrypt> -k <key_text_file>
```

#### Decryption Mode:
```
python3 psu-crypt.py -d <file_to_decrypt> -k <key_text_file>
```