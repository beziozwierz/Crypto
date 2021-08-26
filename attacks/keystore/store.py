import jks
import os
from Crypto.Cipher import AES
from Crypto.Random.random import randint
import sys
from Crypto.Util import Counter

f = open('store_pass.txt',"r")
storepass = f.read()[:-1]
f.close()
keystore = jks.KeyStore.load('keystore.jck', storepass)

def pad(data):
    length = 16 - (len(data) % 16)
    data += bytes([length])*length
    return data

def unpad(data):
    data = data[:-data[-1]]
    return data

def bytes_to_int(iv):
    ddx = map((lambda x: bin(x)[2:].zfill(8)), iv)
    bar = list(ddx)
    bar = ''.join(bar)
    return (int(bar,2))

def encrypt_file(path_to_keystore, mode, key_alias):
    keystore = jks.KeyStore.load(path_to_keystore, storepass)
    if key_alias in keystore.secret_keys:
        data = keystore.secret_keys[key_alias].key
    else:
        cmd = f"keytool -genseckey -alias {key_alias} -keyalg AES -keysize 256 -storetype jceks -keystore keystore.jck -storepass {storepass}"
        os.system(cmd)
        keystore = jks.KeyStore.load(path_to_keystore, storepass)
        data = keystore.secret_keys[key_alias].key
    if(mode=='cbc'):
        key= data[16:]
        iv = data[:16]
    elif(mode=='ofb'):
        key = data[16:]
        iv = data[:16]
    elif(mode == 'ctr'):
        key = data[16:]
        nonce = data[:16]
    f = open('messages/'+key_alias,"r+")
    mess = f.read()
    f.close()
    mess.strip()
    mess = mess.encode('utf-8')
    mess = pad(mess)
    if(mode=='cbc'):
        aes = AES.new(key, AES.MODE_CBC, iv)
        enc = aes.encrypt(mess)
    elif(mode=='ctr'):
        ctr = Counter.new(128, initial_value=bytes_to_int(nonce))
        aes = AES.new(key, AES.MODE_CTR, counter = ctr)
        enc = aes.encrypt(mess)
    elif(mode=='ofb'):
        aes =  AES.new(key, AES.MODE_OFB, iv)
        enc = aes.encrypt(mess)
    f = open('encrypted/'+key_alias, "wb+")
    f.write(enc)
    f.close()

def decrypt_file(path_to_keystore, mode, key_alias):
    keystore = jks.KeyStore.load(path_to_keystore, storepass)
    data = keystore.secret_keys[key_alias].key
    if(mode=='cbc'):
        key= data[16:]
        iv = data[:16]
    elif(mode=='ctr'):
        key = data[16:]
        nonce = data[:16]
    elif(mode=='ofb'):
        key = data[16:]
        iv = data[:16]

    f = open('encrypted/'+key_alias,"rb")
    enc = f.read()
    f.close()

    if(mode=='cbc'):
        aes =  AES.new(key, AES.MODE_CBC, iv)
    elif(mode=='ctr'):
        ctr = Counter.new(128, initial_value=bytes_to_int(nonce))
        aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    elif(mode=='ofb'):
        aes =  AES.new(key, AES.MODE_OFB, iv)

    mess = aes.decrypt(enc)
    mess = unpad(mess)
    print(mess)
    f = open('messages/'+key_alias,'wb+')
    f.write(mess)
    f.close()

def read_test_mess():
    f = open('messages/test',"r+")
    m = f.read()
    f.close()
    m.strip()
    return m

def test():
    path_to_keystore = str(sys.argv[2])
    original_m = read_test_mess()
    #cbc
    encrypt_file(path_to_keystore,'cbc','test')
    decrypt_file(path_to_keystore,'cbc','test')
    cbc_m = read_test_mess()

    encrypt_file(path_to_keystore,'ctr','test')
    decrypt_file(path_to_keystore,'ctr','test')
    ctr_m = read_test_mess()

    encrypt_file(path_to_keystore,'ofb','test')
    decrypt_file(path_to_keystore,'ofb','test')
    ofb_m = read_test_mess()

    if(original_m == cbc_m):
        print("cbc test success")
    else:
        print("cbc test fail")

    if(original_m == ctr_m):
        print("ctr test success")
    else:
        print("ctr test fail")

    if(original_m == ofb_m):
        print("ofb test success")
    else:
        print("ofb test fail")


action = str(sys.argv[1])
if(action=='test'):
    test()
else:
    mode_of_encryption = str(sys.argv[2])
    path_to_keystore = str(sys.argv[3])

if(action == 'encrypt'):
    file_name = str(sys.argv[4])
    encrypt_file(path_to_keystore, mode_of_encryption, file_name)
elif(action == 'decrypt'):
    file_name = str(sys.argv[4])
    decrypt_file(path_to_keystore, mode_of_encryption, file_name)
elif(action == 'oracle'):
    files = sys.argv[4].split(',')
    for i in range(len(files)):
        encrypt_file(path_to_keystore, mode_of_encryption, files[i])
elif(action == 'challenge'):
    m1 = str(sys.argv[4])
    m2 = str(sys.argv[5])
    choice = randint(1,2)
    f = open('messages/challenge', 'w+')
    if(choice == 1):
        f.write(m1)
    else:
        f.write(m2)
    f.close()
    encrypt_file(path_to_keystore, mode_of_encryption, 'challenge')
