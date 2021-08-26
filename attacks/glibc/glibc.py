from functools import reduce
from math import gcd
import Crypto.Random.random

class glibc_rand:
    def __init__(self, seed):
        self.seq = []
        self.seq.append(seed)
        for i in range(1,31):
            self.seq.append((16807 * self.seq[i-1]) % 0x7fffffff)
        for i in range(31,34):
            self.seq.append(self.seq[i-31])
        for i in range(34, 344):
            self.seq.append(self.seq[i-31] + self.seq[i-3])
        self.ctr = 344

    def next(self):
        self.seq.append(self.seq[self.ctr-31] + self.seq[self.ctr-3])
        res = (self.seq[self.ctr] & 0xffffffff ) >> 1
        self.ctr += 1
        return res

def guess_next_glibc(states):
    if len(states) < 31:
        return 0, 1
    r1 = (states[-31] + states[-3]) % 2**31
    r2 = (states[-31] + states[-3] + 1) % 2**31
    return r1, r2

def test_glibc(values, type):
    input_len = len(values)
    if(input_len<31):
        return 0
    random_votes = 0
    glibc_votes = 0

    for i in range(31,input_len):
        r1, r2 = guess_next_glibc(values[:i])
        if(values[i] == r1 or values[i] == r2):
            glibc_votes+=1
        else:
            random_votes+=1
    guess = 'glibc' if glibc_votes > random_votes else 'rand'
    # print("votes glibc: "+str(glibc_votes))
    # print("votes random: "+str(random_votes))
    return 1 if type == guess else 0

def generate_random_seq(length):
    seq = []
    for _ in range(length):
        seq.append(Crypto.Random.random.getrandbits(64))
    return seq

def generate_glibc_seq(length):
    generator = glibc_rand(1)
    seq = []
    for _ in range(length):
        seq.append(generator.next())
    return seq


def test():
    correct = 0
    for i in range(1, 601):
        if i % 2 == 1:
            states = generate_glibc_seq(i)
            if(test_glibc(states,'glibc')==1):
                correct+=1
        else:
            states = generate_random_seq(i)
            if(test_glibc(states, 'rand')==1):
                correct+=1
    print(str(correct)+" guesses out of 600, "+str(((correct / 600)*10000)/100))

test()
