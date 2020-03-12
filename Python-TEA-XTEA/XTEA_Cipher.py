#!/usr/bin/python3.7

from ctypes import *


# Class implementation of our TEA block cipher
class XTEA_Cipher:
    """
    XTEA_Cipher is a Python implementation of the (Tiny Encryption Algorithm) Tea Extensions
    named the Extensions to TEA (aka. XTEA).
    Refer to the paper "Tea Extensions", by Roger M. Needham and David J. Wheeler, Corrected October 1997'.
    """
    # Set block and key sizes according to cipher specification

    blocksize = 64
    keysize = 128

    # Storage for object-specific number of TEA rounds and key
    R = None
    key = None

    # Function to report the block size of the TEA cipher
    def blockSize(self):
        return self.blocksize

    # Function to report key  size of the TEA cipher
    def keySize(self):
        return self.keysize

    # Function to set the number of TEA rounds for the current object.
    def setRounds(self, R):
        self.R = R

    # Function to set the key for the current object.
    def setKey(self, key):
        self.key = key

    # Function to encrypt specified plaintext block.
    def encrypt(self, text: list) -> list:

        # Split plaintext into halves for input into feistal structure.
        sidea = c_uint(text[0])     # y in algorithm paper
        sideb = c_uint(text[1])     # z in algorithm paper

        # Value storage for key schedule.
        summ = c_uint(0)

        # Magic value used for key schedule.
        delta = 0X9E3779B9

        # Set the number of TEA rounds for the encryption process
        count = self.R

        # Output storage
        ciphertext = [0, 0]

        # Iterate through specified TEA encryption rounds
        while count > 0:

            # Perform first encryption with a TEA feistal round on one half of plaintext.
            # This is part of a full TEA cycle, which is two feistal rounds.
            sidea.value += (((sideb.value << 4 ^ sideb.value >> 5) + sideb.value) ^
                            (summ.value + self.key[summ.value & 3])) & 0xffffffff

            # Increment value for key schedule.
            summ.value += delta & 0xffffffff

            # Perform second encryption with a TEA feistal round on the other half of the plaintext.
            # This completes a full TEA cycle, or two feistal rounds.
            sideb.value += (((sidea.value << 4 ^ sidea.value >> 5) + sidea.value) ^
                            (summ.value + self.key[summ.value >> 11 & 3])) & 0xffffffff

            # Decrement remaining TEA rounds after finishing one.
            count -= 1

        # Get the resulting output of the TEA encryption rounds and put it in the output list.
        ciphertext[0] = sidea.value
        ciphertext[1] = sideb.value

        # Return the ciphertext of the encryption process.
        return ciphertext

    # Function to decrypt TEA encrypted ciphertext.
    def decrypt(self, ctext: list) -> list:

        # Split ciphertext into two halves for input into feistal structure.
        sidea = c_uint(ctext[0])  # y in algorithm paper
        sideb = c_uint(ctext[1])  # z in algorithm paper

        # Magic value used for key schedule.
        delta = 0X9E3779B9

        # Value storage for key schedule. During the decryption process,
        # this is set to the magic value multiplied by the number of TEA decryption rounds.
        summ = c_uint((delta * self.R) & 0xffffffff)

        # Set the number of TEA rounds for the decryption process.
        count = self.R

        # Output storage.
        plaintext = [0, 0]

        # Iterate through specified TEA decryption rounds.
        while count > 0:
            # Perform first decryption with a TEA feistal round on one half of the ciphertext.
            # This is part of a full TEA cycle, which is two feistal rounds.
            sideb.value -= (((sidea.value << 4 ^ sidea.value >> 5) + sidea.value) ^
                             (summ.value + self.key[summ.value >> 11 & 3])) & 0xffffffff

            # Decrement value of key schedule.
            summ.value -= delta & 0xffffffff

            # Perform second decryption with a TEA feistal round on the other half of the ciphertext.
            # This completes a full TEA cycle, or two feistal rounds.
            sidea.value -= (((sideb.value << 4 ^ sideb.value >> 5) + sideb.value) ^
                             (summ.value + self.key[summ.value & 3])) & 0xffffffff

            # Decrement remaining TEA rounds after finishing one.
            count -= 1

            # Decrement remaining TEA rounds and put it in the output list.
            plaintext[0] = sidea.value
            plaintext[1] = sideb.value

            # Return the plaintext of the decryption process.
        return plaintext
