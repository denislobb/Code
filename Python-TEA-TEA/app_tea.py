#!/usr/bin/python3.7

from TEA_Cipher import *
# Main function to create an instance of the TEA_Cipher class and utilise provided functions.
def main():

    # Create new TEA_Cipher object.
    test = TEA_Cipher()
    
    # Set the key to be used for the encryption and decryption operations.
    key = [0x30cee881, 0x8a3d9263, 0xcae86177, 0xf89f438b]

    # Take the specified key and set that as the encryption/decryption key for the current TEA_Cipher object.
    test.setKey(key)

    # Set the number of TEA rounds for the current TEA_Cipher object.
    rounds = 48
    test.setRounds(int(rounds))

    # Cleartext to be encrypted.
    cleartext = [0x44656e69, 0x734c6f62]

    # Pass given plaintext block to the TEA_Cipher encrypt function and store the encrypted output.
    ciphertext = test.encrypt(cleartext)

    # ciphertext should decipher back to target_cleartext = [0x44656e69, 0x734c6f62]
    target_cleartext = cleartext

    # Take ciphertext output from encryption operation then perform the decryption function on the value.
    returned_cleartext = test.decrypt(ciphertext)

    # Print out specifics of the TEA implementation to the user.
    text_width = 24

    print('\nImplementation of the Tiny Encryption Algorithm (TEA) in python.')
    # Output the specified number of TEA rounds.
    print(f'{"number of TEA rounds:":>{text_width}} {test.R}')
    print(f'{"blocksize:":>{text_width}} {test.blockSize()}')
    print(f'{"keysize:":>{text_width}} {test.keySize()}')
    print(f'{"key:":>{text_width}} {str([hex(x) for x in key])}')

    # Output the plaintext presented for the encryption.
    print(f'{"plaintext:":>{text_width}} {str([hex(x) for x in cleartext])}')

    # Output the resulting ciphertext from the encryption process
    print(f'{"ciphertext:":>{text_width}} {str([hex(x) for x in ciphertext])}')

    # Output the resulting plaintext from the decryption function performed on the ciphertext.
    print(f'{"ciphertext decrypted:":>{text_width}} {str([hex(x) for x in returned_cleartext])}')

    # Output: the resulting plaintext from the decryption function should be.
    print(f'{"target_plaintext:":>{text_width}} {str([hex(x) for x in target_cleartext])}')

    # Output: the resulting plaintext from the decryption function should be.
    print(f'{"Decipher:":>{text_width}} {"Successful!!!" if returned_cleartext == target_cleartext else "FAILED!"}')


# Run the main function.
if __name__ == '__main__':
    main()
