from functools import reduce
from math import gcd
import Crypto.Random.random

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n
    else:
        return -1

class lcg_rand:
    mult = 45655645
    inc = 1337
    mod = 111221214

    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (self.state * self.mult + self.inc) % self.mod
        return self.state


def guess_next_lcg(states):
    #calc modulus
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    t_vals = zip(diffs, diffs[1:], diffs[2:])
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in t_vals]
    modulus = abs(reduce(gcd, zeroes))
    #calc multiplier
    x2 = states[1] - states[0]
    if(x2 < 0):
        x2 += modulus
    x1 = states[2] - states[1]
    if(x1 < 0):
        x1 += modulus
    multiplier = x1 * modinv(x2, modulus) % modulus
    #calc increment
    increment = (states[1] - states[0]*multiplier) % modulus
    #next value
    next = (states[-1]*multiplier+increment)%modulus
    return next

def test_lcg(values, type):
    input_len = len(values)
    if(input_len<4):
        return 0
    random_votes = 0
    lcg_votes = 0
    for i in range(4,input_len):
        if(values[i] == guess_next_lcg(values[:i])):
            lcg_votes+=1
        else:
            random_votes+=1
    guess = 'lcg' if lcg_votes > random_votes else 'rand'
    if(type == guess):
        return 1
    else:
        return 0


def generate_lcg_seq(length):
    generator = lcg_rand(131)
    seq = []
    for _ in range(length):
        seq.append(generator.next())
    return seq
def generate_random_seq(length):
    seq = []
    for _ in range(length):
        seq.append(Crypto.Random.random.getrandbits(64))
    return seq


def test():
    correct = 0
    for i in range(1, 401):
        if i % 2 == 1:
            states = generate_lcg_seq(i)
            if(test_lcg(states,'lcg')==1):
                correct+=1
        else:
            states = generate_random_seq(i)
            if(test_lcg(states, 'rand')==1):
                correct+=1

    print(str(correct)+" correct guesses out of 400, "+str(((correct / 400)*10000)/100))

test()
