import random
from Crypto.Cipher import AES
import os

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

#16 bytes -> int
def bytes_to_int(iv):
    ddx = map((lambda x: bin(x)[2:].zfill(8)), iv)
    bar = list(ddx)
    bar = ''.join(bar)
    return (int(bar,2))

#int->string
def int_to_bytes(int_iv):
    bar = str(bin(int_iv))[2:].zfill(128)
    bar = [bar[i:i+8] for i in range(0, len(bar), 8)]
    ddx = map((lambda x: int(x,2).to_bytes(1,'big')), bar)
    return b"".join(list(ddx))

def increment_iv(iv):
    x = bytes_to_int(iv)
    x = x + 1
    return int_to_bytes(x)

def prepare_next_message(m,iv):
    part_to_change = m[:16]
    iv2 = increment_iv(iv)
    iv_xor = byte_xor(iv,iv2)
    m2 = byte_xor(iv_xor, part_to_change)
    return m2+m[16:]

#oracle vars
rand_key = int_to_bytes(random.getrandbits(128))
rand_iv = int_to_bytes(random.getrandbits(128))
mess_chosen = 0

def return_encrypted(m):
    global rand_iv
    global rand_key
    aes = AES.new(rand_key, AES.MODE_CBC, rand_iv)
    enc = aes.encrypt(m)
    rand_iv = increment_iv(rand_iv)
    return enc

def return_one_encrypted(m1, m2):
    global mess_chosen
    mess_chosen = random.randint(1,2)
    if(mess_chosen == 1):
        return return_encrypted(m1)
    else:
        return return_encrypted(m2)


m0 = int_to_bytes(random.getrandbits(128))
m1 = prepare_next_message(m0, rand_iv)
m2 = int_to_bytes(random.getrandbits(128))

enc0 = return_encrypted(m0)
enc_x = return_one_encrypted(m1,m2)

print("enc x:")
print(enc_x)
print("enc 0:")
print(enc0)
print("")
if(enc_x == enc0):
    print("adversary: message 1")
else:
    print("adversary: message 2")
print("correct answer: "+str(mess_chosen))
