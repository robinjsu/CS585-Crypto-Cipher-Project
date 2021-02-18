## PROJECT 1 - PSU-CRYPT

### ROBIN SU
### Winter 2021
### CS 485-585 Cryptography  
  
<br/>

### Description
This program takes standard ASCII as input. 
Encrypted output is written to a file called ciphertext.txt. The ciphertext output writes each ciphertext block
on a new line, no '0x' appended. Padding is done with appending the appropriate number of '0's at the end of the last block to fill a full block (or just a full block of padding if the text works out to full blocks alone). 

Decrypted output is written to a file called <ciphertext-filname>-decrypted.txt. Decryption mode takes in a text file
of ciphertext blocks, each written on a new line, no '0x' appended.

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