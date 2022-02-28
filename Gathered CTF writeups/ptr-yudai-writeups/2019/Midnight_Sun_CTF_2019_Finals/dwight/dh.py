#!/usr/bin/python -Btt

from Crypto.Random import random
from Crypto.Hash import BLAKE2b


class DHkey:

    def __init__(self, secret=None):
        self.gen = 0x2
        self.a = None
        self.secret = secret
        self.prime = 0xf2d0058fa043fb189699d118de484b66a10dce703b27209cfc6d23d9178067c9d560d7d8ba9d4439a22aed66322f25d886c0a5cd41821b49aae3d7a7b72f9b0e2d823709af5444c7e9474df5867e605e638923a2fad546a86b8014ba460d238a939b445d7489c91977b54ab531d75b0f4264f187218f885129751ec78654f4b21191365fea1b7fefc40842bbc07c4f1d1ad153f6a39b582406f6b5895336a1199f7556ee957eac716ae6678cbe5390730f0ebb3cc5210242a80cb128bfd747ed1b61af6bbd5b5dc07b34c5ca7af73d1ee973b93e13918801aefd674df92a0ad84bfa2a8cee1ad26140da1d5fc0c450a1eaebc88f8ea8e703a0f3a814e1f6975aa5be732473575d16f137d2ce5f7a546ce4371ecb5e8052295e122a9cf89a026e2d09bde56b8b04cc4cae66cd0c5e0dfe30695dd798c50e39c911c887febacaaefd2bfe7d454e051c432d66ad84680da7c126f1a9c7c540283ccb863b9414bb536ba358259104ecb406b4976f97558fa4e5854888a8d13c96a14025da0c55f869f6af954b1e7aa1d317262c52099860e870a7eaf72f9910aca809ff2dea37fca3efb31fd43a308e4138e40178beac0fbb0e79ed7d1dcf8f8a81a4abbfe6749f4c1b96bd65a14822490bc0a71e854bc8077c7a8f2c6fe308f86dec97f600a4a0015f086b021f7f0bcafde3da4d7e38a9aa1e992539389e99412fd22988f3ee7b13

    def generate(self):
        if self.secret is None:
            self.a = random.getrandbits(4096)
        else:
            self.a = int(self.secret.encode("hex"), 16)
        return pow(self.gen, self.a, self.prime)

    def digest(self, key):
        return BLAKE2b.new(
            digest_bits=256,
            key=str(key)[:64]
        ).digest()

    def shared(self, share):
        if self.a is None:
            raise Exception("Call generate first.")
        key = pow(share, self.a, self.prime)
        self.a = None
        return self.digest(key)
