import base64
import os
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import codecs

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]


class AESCipher:

    root_path = os.path.dirname(os.path.abspath(__file__))

    def __init__( self, key ):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

    def read_file(self, filename):
        with codecs.open(filename, "rb",encoding='utf-8', errors='ignore') as f:
            raw = f.read()
            return raw

    def write_file(self, filename, raw):
        with codecs.open(filename, "wb",encoding='utf-8', errors='ignore') as f:
            f.write(raw)

    def enc_file(self, filename):
        data = self.read_file(self.root_path + '/static/onlinetest/docs/' + filename)
        self.encrypt(data)
        self.write_file(filename)

    def dec_file(self, filename):
        data = self.read_file(self.root_path + '/static/onlinetest/docs/' + filename)
        self.decrypt(data)
        self.write_file(filename)


cipher = AESCipher('mysecretpassword')

'''
encrypted = cipher.encrypt('Secret Message A')
decrypted = cipher.decrypt(encrypted)
print(encrypted)
print(decrypted)
'''
cipher.enc_file('201703211847.xlsx')
cipher.dec_file('201703211847.xlsx')

