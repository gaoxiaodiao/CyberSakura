#!/usr/bin/python -Btt

from Crypto import Random
from Crypto.Cipher import Salsa20, ChaCha20
from Crypto.Hash import Poly1305


class Protocol:

    def __init__(self, kex):
        self.key = None
        self.kex = kex
        self.ctr = 0
        self.execution = None

    def init_kex(self):
        return self.kex.generate()

    def sharedkey(self, share):
        self.key = self.kex.shared(share)

    def nonce(self):
        if self.key is None:
            raise BaseException("Missing shared key.")
        return Random.get_random_bytes(8)

    def mac(self, command, nonce=None):
        mac = Poly1305.new(
            key=self.key,
            cipher=ChaCha20,
            data=command.encode("ascii"),
            nonce=nonce
        )
        return "{}.{}".format(
            mac.nonce.encode("hex"),
            mac.hexdigest()
        )

    def encrypt(self, message):
        nonce = self.nonce()
        cipher = Salsa20.new(
            key=self.key,
            nonce=nonce
        )
        return nonce + cipher.encrypt(message)

    def decrypt(self, ciphertext):
        cipher = Salsa20.new(
            key=self.key,
            nonce=ciphertext[:8]
        )
        return cipher.decrypt(ciphertext[8:])
