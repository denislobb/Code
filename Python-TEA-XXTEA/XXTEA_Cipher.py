#!/usr/bin/python3.7

from ctypes import *


# Class implementation of our TEA block cipher
class BlockTEA:
    """
    # BlockTEA is a Python 3 implementation of the (Tiny Encryption Algorithm) Tea Extensions known as Block TEA.
    # Refer to "Tea Extensions" by Roger M. Needham and David J. Wheeler, Corrected October 1997.
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
            v.append(c_ulong(text[i]))

        # set initial z value
        z = v[n - 1]

        # Value storage for key schedule.
        summ = c_ulong(0)

        # Magic value used for key schedule.
        delta = 0x9e3779b9

        # Set the mix operations per word of the blocksize for the encryption process
        q = 6 + 2 * (self.rounds - 6) // n

        # Value storage for key mixer operator for the encryption process
        # e = c_ulong(0)

        # Iterate through specified TEA encryption rounds
        while q > 0:

            # Increment value for key schedule.
            summ.value += delta & 0xffffffff
            # key mixer operator for the encryption process
            e = summ.value >> 2 & 3

            for p in range(n):

                # Perform first encryption with a TEA feistal round on one part of plaintext.
                v[p].value += (((z.value << 4 ^ z.value >> 5) + z.value) ^
                                (self.key[p & 3 ^ e] + summ.value)) & 0xffffffff
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
            if isinstance(ctext[i], c_ulong):
                v.append(ctext[i])
            else:
                v.append(c_ulong(ctext[i]))

        # Magic value used for key schedule.
        delta = 0X9E3779B9

        # Set the mix operations per word of the blocksize for the encryption process
        q = 6 + 2 * (self.rounds - 6) // n

        # Value storage for key schedule.
        summ = c_ulong(0)
        summ.value = q * delta

        # Iterate through specified TEA decryption rounds.
        while summ.value != 0:
            # key mixer operator for the decryption process
            e = summ.value >> 2 & 3

            for p in range(n-1, 0, -1):
                z = v[p-1]
                v[p].value -= (((z.value << 4 ^ z.value >> 5) + z.value) ^
                                (self.key[p & 3 ^ e] + summ.value)) & 0xffffffff

            z = v[n - 1]
            v[0].value -= (((z.value << 4 ^ z.value >> 5) + z.value) ^
                            (self.key[0 & 3 ^ e] + summ.value)) & 0xffffffff

            summ.value -= delta & 0xffffffff

        return [x.value for x in v]
