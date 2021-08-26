import random
from Crypto.Cipher import AES
import os

def int_to_bytes(int_iv):
    bar = str(bin(int_iv))[2:].zfill(128)
    bar = [bar[i:i+8] for i in range(0, len(bar), 8)]
    ddx = map((lambda x: int(x,2).to_bytes(1,'big')), bar)
    return b"".join(list(ddx))

rand_key = int_to_bytes(random.getrandbits(128))
rand_iv = int_to_bytes(random.getrandbits(128))

def pad(data):
    length = 16 - (len(data) % 16)
    data += bytes([length])*length
    return data

def unpad(data):
    data = data[:-data[-1]]
    return data

def encrypt(m):
    global rand_iv
    global rand_key
    m = pad(m)
    aes = AES.new(rand_key, AES.MODE_CBC, rand_iv)
    enc = aes.encrypt(m)
    return enc

def decrypt(c):
    global rand_iv
    global rand_key
    aes =  AES.new(rand_key, AES.MODE_CBC, rand_iv)
    m = aes.decrypt(c)
    m = unpad(m)
    return m

def padding_oracle(c, iv):
    global rand_key
    aes =  AES.new(rand_key, AES.MODE_CBC, iv)
    m = aes.decrypt(c)
    return all([n == m[-1] for n in m[-m[-1]:]])

def return_blocks(m):
    return [m[i:i+16] for i in range(0, len(m), 16)]

m = int_to_bytes(random.getrandbits(323))

c = encrypt(m)

def step(c, vals, pad, iv):
    bc = return_blocks(c)
    b1 = list(bc[-2])
    original = b1[16-pad]
    for x in range(1,pad):
        b1[16-x] = pad ^ vals[x-1]
    i = 0
    b1[16-pad] = i
    while not padding_oracle(c[:-32]+bytes(b1)+bc[-1], iv):
        i += 1
        if(i == original):
            i+=1
        if(i > 255):
            i = original
        b1[16-pad] = i
    v1 = i^pad
    v2 = v1^original
    vals.append(v1)
    return vals, v2

def iv_step(block, vals, pad, iv):
    iv = list(iv)
    original = iv[16-pad]

    for x in range(1,pad):
        iv[16-x] = pad ^ vals[x-1]
    i = 0
    iv[16-pad] = i
    while not padding_oracle(block, bytes(iv)):
        i += 1
        if(i == original):
            i+=1
        if(i > 255):
            i = original
        iv[16-pad] = i
    v1 = i^pad
    v2 = v1^original
    vals.append(v1)
    return vals, v2

def attack(c,iv):
    length = len(return_blocks(c))
    res = []
    temp_res = []
    vals = []
    for i in range(1,17):
        vals, r = iv_step(c[:16],vals,i, iv)
        temp_res.append(r)
    temp_res.reverse()
    res.append(temp_res)
    temp_res = []
    for i in range(1, length):
        vals = []
        ciphertext = c[:(16+i*16)]
        for j in range(1,17):
             vals, r = step(ciphertext,vals,j, iv)
             temp_res.append(r)
        temp_res.reverse()
        res.append(temp_res)
        temp_res = []
    flattened = [val for sublist in res for val in sublist]
    return flattened


res = attack(c,rand_iv)
res = unpad(res)

print("orginal message: ")
print(m)
print("\nmessage from oracle: ")
print(bytes(res))
print("\nare the same?? : ",m == bytes(res))
