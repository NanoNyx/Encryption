import random
import math
import string
import sys

import codecs

import rand_prime as pgen
from commons import *

sys.setrecursionlimit(100000)

keys_default_fname = "default"

def pad(text: bytes) -> bytes:
    while len(text) % 8 != 0:
        text += b'\x00'
    return text

def remove_pad(text: bytes) -> bytes:
    return text.replace(b'\x00', b'')

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
    else:
        return x % m

class RSAKeyContainer:
    def __init__(self, len = 128, p = 0, q = 0):
        self.n = 0
        self.e = 0
        self.d = 0
        self.len = len
        if (p == 0 or q == 0):
            return
        self.create(p, q)
    
    def create(self, p = 0, q = 0):
        if (p == 0 or q == 0):
            self.generate_factors(self.len)
            return
        self.generate_keys(p, q)

    def generate_keys(self, p, q):
        self.n = p * q
        phi = (p - 1) * (q - 1)
        self.e = phi

        while(math.gcd(phi, self.e) != 1):
            self.e = random.randrange(1, phi)

        self.d = modinv(self.e, phi)
        
        print("n = " + str(self.n))
        print("e = " + str(self.e))
        print("d = " + str(self.d))

    def generate_factors(self, len):
        p = pgen.generateLargePrime(len)
        q = pgen.generateLargePrime(len)
        print("Генерація p и q ["+str(len)+" бит]")
        print("p = " + str(p))
        print("q = " + str(q))
        self.generate_keys(p, q)

    def get_public_keypair(self):
        return self.e, self.n

    def get_private_keypair(self):
        return self.d, self.n
    
    def show_public_keypair(self):
        e, n = self.get_public_keypair()
        print("Публічний ключ:")
        print("e = " + str(e))
        print("n = " + str(n))
    
    def show_private_keypair(self):
        d, n = self.get_private_keypair()
        print("Секретний ключ:")
        print("d = " + str(d))
        print("n = " + str(n))
    
    def show_keys(self):
        self.show_public_keypair()
        print("")
        self.show_private_keypair()
    
    def get_priv_key_file(self, name):
        return "priv_key" + key_ext
    
    def get_pub_key_file(self, name):
        return "pub_key" + key_ext
    
    def save_keys(self):
        e, n = self.get_public_keypair()
        d, n = self.get_private_keypair()
        nw = str(now())
        pu_name = self.get_pub_key_file(nw)
        rv_name = self.get_priv_key_file(nw)
        write(pu_name, str(e) + " " + str(n))
        write(rv_name, str(d) + " " + str(n))
        print("Публічний ключ збережено [" + pu_name + "]")
        print("Секретний ключ збережено [" + rv_name + "]")
    
    def load_keys(self, name):
        pu_name = self.get_pub_key_file(name)
        rv_name = self.get_priv_key_file(name)
        pub = read(pu_name)
        p_tok = pub.split()
        self.e = int(p_tok[0])
        self.n = int(p_tok[1])
        prv = read(rv_name)
        p_tok = prv.split()
        self.d = int(p_tok[0])
        print("Публічний ключ завантажено [" + pu_name + "]")
        self.show_public_keypair()
        print("\nСекретний ключ завантажено [" + rv_name + "]")
        self.show_private_keypair()


class RSAEncoder:
    def __init__(self, keyContainer = None):
        self.keys = keyContainer

    def load_keyset(self, keys):
        self.keys = keys

    def rsa_encrypt(self, M):
        e, n = self.keys.get_public_keypair()
        if (M > n):
            return -1
        C = pow(M, e, n)
        return C

    def rsa_decrypt(self, C):
        d, n = self.keys.get_private_keypair()
        if (C > n):
            return -1
        M = pow(C, d, n)
        return M

    def rsa_encrypt_msg(self, msg):
        if (self.keys == None):
            return
        encrypted = []
        for c in msg:
            encrypted.append(str(self.rsa_encrypt(ord(c))))
        return " ".join(encrypted)

    def rsa_decrypt_msg(self, msg):
        if (self.keys == None):
            return
        encrypted = msg.encode().decode("ascii").split(" ")
        decrypted = []
        i = 0
        for block in encrypted:
            decrypted.append(chr(self.rsa_decrypt(int(encrypted[i]))))
            i += 1
        return "".join(decrypted)


def gen_des_key():
    return bytes(
        "".join(random.choice(
            string.ascii_uppercase
                + string.ascii_lowercase
                + string.digits
                + string.punctuation
        ) for _ in range(8))
        , "ascii")


def des_set_key(key: bytes):
    global des, rsa, des_key, enc_des_key
    des_key = key
    enc_des_key = rsa.rsa_encrypt_msg(des_key.decode())
    des = DES.new(des_key, DES.MODE_ECB)





# Генерация ключей + Шифрование/Дешифрование
#"""
keys = RSAKeyContainer()
rsa = RSAEncoder()
msg = read("msg.txt")
keys.create()
rsa.load_keyset(keys)
keys.save_keys()
print("")
keys.show_public_keypair()
keys.show_private_keypair()
print("")
show_text("Повідомлення:", msg)
print("")
msg = rsa.rsa_encrypt_msg(msg)
show_text("Зашифроване повідомлення:", msg)
write("encrypted.txt", msg)
print("")
msg = rsa.rsa_decrypt_msg(msg)
show_text("Розшифроване повідомлення:", msg)
write("decrypted.txt", msg)
#"""


# Дешифрование из сохраненных сообщений+ключей
"""
print("\nДешифрування із файла")
keys = RSAKeyContainer()
rsa = RSAEncoder()
msg = read("encrypted.txt")
keys.load_keys("")
rsa.load_keyset(keys)
show_text("Завантажене зашифроване повідомлення:", msg)
msg = rsa.rsa_decrypt_msg(msg)
show_text("Розшифроване повідомлення:", msg)
"""
