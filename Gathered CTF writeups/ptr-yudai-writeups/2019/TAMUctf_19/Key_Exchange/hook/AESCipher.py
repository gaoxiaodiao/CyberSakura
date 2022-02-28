import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

#https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256

class AESCipher(object):

    def __init__(self, key): 
        self.bs = 16
        self.key = key

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

if __name__ == '__main__':
    aes = AESCipher(b',\xe4\xed\x1f\x81\xd7\xb3\xeeK\x9eJ\x8f\x0br\xfb\xaeh.R\xd3\x8d\xc9\x9e\x1d"\xf8\x7f\x1f\xcbD_\xe4')
    data = b'3skMVQxtxehGwzfN0l2Y+sJISg65chbfxz/gex/lxIM9M/DfhTVMdIiv/WxplnEmh16UAI5pJzU0+/1CiHLJWm/PAvZykfxOISUCaRhD7gM='
    print(aes.decrypt(data))
