#include <iostream>
#include <bitset>
#include <cstring>
#include <cmath>
// use this lib?
#include <boost/integer.hpp>

using namespace std;
// use hex representation to do bit shifting
// convert with format string to get key bits
// TODO: how to store the 80 bits?

// number of bits in key
int numBits = 80;
// bits for bit string to do left shifting
const size_t BITS = 80;

// left shift bits by one and add 1 to end if necessary
int shiftBits(uint key) {
    int carry = 0;
    boost::uint_t<76>::fast threshold = pow(2, numBits - 1);
    bitset<BITS> keyBits{key};
    cout << "original key: " << keyBits << endl;
    if (key > threshold) {
        key = ((key % threshold) << 1) + 1;
        carry = 1;
    } else {
        key <<= 1;
    }
    keyBits = key;
    cout << "new key: " << keyBits << endl; 

    return key;
}

// after shifting, get new string of bits before grabbing subkey values
int castToStr(char* keyStr, uint key, int numBits) {
    int hex = numBits / 4;
    if (key == 0) {
        return -1;
    }
    char kBuf[hex] = {};
    sprintf(kBuf, "%x", key);
    for (int i = 0; i < (hex); i++) {
        keyStr[i] = kBuf[i];
    }
    return 0;
}


int main(void) {
    char keyBuf[20];
    // char keyStrn[2];
    // uint threshold = pow(2, 15);
    boost::uint<120>::fast key = 0xabcdef01;
    bitset<BITS> keyBits{key};

    key = shiftBits(key);
    castToStr(keyBuf, key, 16);
    printf("%c%c\n", keyBuf[0], keyBuf[1]);

    return 0;
}