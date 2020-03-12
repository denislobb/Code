#!/usr/bin/python3.7

from CXXTEA_Cipher import *


# Main function to create an instance of the Blockcipher class and utilise provided functions.
def main():
    # Create new Blockcipher object.
    test = Blockcipher()

    # Set the key to be used for the encryption and decryption operations.
    key = [0x30cee881, 0x8a3d9263, 0xcae86177, 0xf89f438b]

    # Set the encryption/decryption key for the current Blockcipher object.
    test.setKey(key)

    # Set the number of TEA rounds for the current Blockcipher object.
    rounds = 48
    test.setRounds(int(rounds))

    # Set the word blocksize for the current Blockcipher object.
    blocksize = 2
    test.set_blocksize(blocksize)

    # Set the cleartext desired for the encryption operation.
    cleartext = [0x34FE6E4A, 0x73D7172C]

    # Pass given cleartext block to the Blockcipher encrypt function and store the output.
    ciphertext = test.encrypt(cleartext)

    # ciphertext should decipher to target_cleartext = [0x34FE6E4A, 0x73D7172C]
    target_cleartext = cleartext

    # Take ciphertext output from encryption operation then perform the decryption function on the value.
    returned_cleartext = test.decrypt(ciphertext)

    # Print out specifics of the TEA implementation to the user.
    text_width = 24

    print('\nImplementation of the Tiny Encryption Algorithm (TEA) in python.')
    # Output the specified number of TEA rounds.
    print(f'{"number of TEA rounds:":>{text_width}} {test.rounds}')
    print(f'{"blocksize:":>{text_width}} {test.blocksize}')
    print(f'{"keysize:":>{text_width}} {test.keySize()}')
    print(f'{"key:":>{text_width}} {str([hex(x) for x in key])}')

    # Output the cleartext presented for the encryption.
    print(f'{"cleartext:":>{text_width}} {str([hex(x) for x in cleartext])}')

    # Output the resulting ciphertext from the encryption process
    print(f'{"ciphertext:":>{text_width}} {str([hex(x) for x in ciphertext])}')

    # Output the resulting cleartext from the decryption function performed on the ciphertext.
    print(f'{"ciphertext decrypted:":>{text_width}} {str([hex(x) for x in returned_cleartext])}')

    # Output: the resulting cleartext from the decryption function should be.
    print(f'{"target_cleartext:":>{text_width}} {str([hex(x) for x in target_cleartext])}')

    # Output: the resulting cleartext from the decryption function should be.
    print(f'{"Decipher:":>{text_width}} {"Successful!!!" if returned_cleartext == target_cleartext else "FAILED!"}')


# Run the main function.
if __name__ == '__main__':
    main()
