# "Attacks" directory<br/>


*This directory contains some examplary attack on cryptographic functions etc.*

---
<br/>

### AES
- Script in this directory performs attack on AES Block Cipher. 
- Mode of operation is CBC mode with PKCS#5 padding. 
- The attacker is assumed to have access to a padding oracle.
- Attack is known as Padding oracle attack [WIKI](https://en.wikipedia.org/wiki/Padding_oracle_attack).
---
<br/>

### LCG 

*This program is breaking the LCG pseudorandom function*<br/>
Functions implemented in the script:
- Linear congruential generator 
- Crypto pseudorandom generator
- Guessing function
- Testing function (distinguisher)
---
<br/>

### GLIBC 

*This program is breaking the C standard library `rand()` pseudorandom function*<br/>
Functions implemented in the script:
- C standard library function 
- Crypto pseudorandom generator
- Guessing function
- Testing function (distinguisher)
---
<br/>

### FASTEXP

This directory contains program that presents timing attack on fast exponentation algorithm. <br/>
The algorithm under attack is: [PAPER](http://homepages.math.uic.edu/~leon/cs-mcs401-s08/handouts/fastexp.pdf) <br/>
Attack is performed based on the data (timestamps) collected during the execution of exponentation function.

---
<br/>

### KEYSTORE

*Code in this directory performs some operations using Java KeyStore (JKS).*

#### Files description:
- create_cmds <- cheat sheet for generating keys through the terminal (keytool command)
- keystore.jck <- JCK file
- store_pass.txt <- file that contains password to the keystore
- store.py <- script to perform encryption/decryption operations (AES). It uses secret key from JKS.
- messages <- directory to store unencrypted messages
- encrypted <- directory to store encrypted messages
- distingusher.py <- attack on badly used AES CBC

#### Store.py usage (supported operations):
1. `python3 store.py encrypt [mode_of_operation] [keystore_path] [filename]`
2. `python3 store.py decrypt [mode_of_operation] [keystore_path] [filename]`
3. `python3 store.py oracle [mode_of_operation] [keystore_path] [files_names - coma separated]`
4. `python3 store.py challenge [mode_of_operation] [keystore_path] [message 1] [message 2]`

#### Supported \[mode_of_operation] parameters: 
- cbc (Cipher block chaining)
- ofb (Output feedback)
- ctr (Counter)

#### Operations description: <br/>

**encrypt** -  encrypts file named \[filename] in messages catalog using AES with \[mode_of_operation] and secret key from \[keystore_path] <br/><br/>
**decrypt** -  decrypts file named \[filename] in encrypted catalog using AES with \[mode_of_operation] and secret key from \[keystore_path] <br/><br/>
**oracle** -  encrypts many files - \[files_names - coma separated] at once<br/><br/>
**challenge** -  on input \[message 1] \[message 2] returns ciphertext of randomly choosen message (1 or 2). It writes to files `messages/challenge` and `encrypted/challenge`

#### Examples of use
```
python3 store.py encrypt cbc keystore.jck test 
python3 store.py decrypt cbc keystore.jck test
python3 store.py oracle cbc keystore.jck test1,test2,test3
python3 store.py challenge cbc keystore.jck funny_message_testtest this_message_is_sad
```
<br/>

#### Distingusher.py description:

Distinguisher is a program that is able to win CPA (Choosen plaintext attack) experiment with probability 1. <br/>
Vulnerale verion of AES CBC  generates consecutive IV (initialization vectors) by incrementing its value by 1.

**Experiment:** <br/>
- attacker asks to encrypt message m<sub>0</sub>
- attacker prepares messages m<sub>1</sub> and m<sub>2</sub>
- attacker asks to encrypt one of the messages
- attacker, based on the given ciphertext, answers which message was enctypted

---
