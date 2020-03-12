#!/usr/bin/python3.7

from ctypes import *


# Class implementation of our TEA block cipher
class Blockcipher:
    """
    Blockcipher is a Python implementation of the Corrected Block TEA Algorithm (aka. XXTEA).
    Refer to the paper "Tea Extensions", by Roger M. Needham and David J. Wheeler, Corrected October 1997'.
    """
    # Set key size according to cipher specification
    keysize = 128

    # Storage for object-specific number of words in word block, number of TEA rounds and cipher key
    blocksize = None
    rounds = None
    key = None

    # Function to set number of words in word block of the TEA Block cipher.
    def set_blocksize(self,  n: int):
        self.blocksize = n

    # Function to report number of words in word block of the TEA Block cipher.
    def get_blocksize(self):
        if not self.blocksize:
            print('Block size not yet set ... set_blocksize(n)')
        else:
            return self.blocksize

    # Function to report key size of the TEA cipher
    def keySize(self):
        return self.keysize

    # Function to set the number of TEA rounds for the current object.
    def setRounds(self, rounds: int):
        self.rounds = rounds

    # Function to set the key for the current object.
    def setKey(self, key):
        self.key = key

    # Function to encrypt specified plaintext block.
    def encrypt(self, text: list) -> list:
        """
        encrypt - encrypts the input list of integers into a encrypted list of integers using the Block TEA algorithm.
        :param text: the block of text to be encrypted - encoded as integer values.
        :return: list: the encrypted text.
        """
        # using letters to be compatible with algorithm
        n = self.blocksize

        v = []
        for i in range(n):
            v.append(c_uint32(text[i]))

        # set initial z value
        z = v[n-1]
        y = v[0]
        summ = c_uint32(0)

        # Magic value used for key schedule.
        delta = 0x9e3779b9

        # Set the mix operations per word of the blocksize for the encryption process
        q = 6 + 2 * (self.rounds - 6) // n

        # Iterate through specified TEA encryption rounds
        while q > 0:

            # Increment value for key schedule.
            summ.value += delta & 0xffffffff
            e = summ.value >> 2 & 3

            for p in range(n):
                y = v[(p+1) % n]

                v[p].value += (((z.value >> 5 ^ y.value << 2) + (y.value >> 3 ^ z.value << 4)) ^
                               ((summ.value ^ y.value) + (self.key[p & 3 ^ e] ^ z.value))) & 0xffffffff
                z = v[p]

            # Decrement remaining TEA rounds after finishing one round.
            q -= 1

        return [x.value for x in v]

    # Function to decrypt TEA encrypted ciphertext.
    def decrypt(self, ctext: list) -> list:
        """
        decrypt - decrypts the input list of encrypted integers into list of plaintext integers
        using the Block TEA algorithm.
        :param ctext: the block of text to be decrypted - encoded as integer values.
        :return: v: the list of plaintext.
        """
        # using letters to be compatible with algorithm
        n = self.blocksize

        v = []
        for i in range(n):
            v.append(c_uint32(ctext[i]))

        # set initial y value
        y = v[0]

        # Magic value used for key schedule.
        delta = 0X9E3779B9

        # Set the mix operations per word of the blocksize for the encryption process
        q = 6 + 2 * (self.rounds - 6) // n

        # Value storage for key schedule.
        summ = c_uint32(0)
        summ.value = (q * delta) & 0xffffffff

        # Iterate through specified TEA decryption rounds.
        while summ.value != 0:

            e = summ.value >> 2 & 3

            for p in range(n-1, -1, -1):

                z = v[(p-1) % n]  # = v[1]
                v[p].value -= (((z.value >> 5 ^ y.value << 2) + (y.value >> 3 ^ z.value << 4)) ^
                               ((summ.value ^ y.value) + (self.key[p & 3 ^ e] ^ z.value))) & 0xffffffff
                y = v[p]

            summ.value -= delta & 0xffffffff

        return [x.value for x in v]
