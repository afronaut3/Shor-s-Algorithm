import numpy as np
import matplotlib.pyplot as plt
import random
import SimulatorS
import SimulatorM
import string_processing
import time
import timeit
import circuit
import os
import Nonatomic
import Phase_estimation
import sympy
from fractions import Fraction


def gcd(a, b):
    if (a == 0):
        return b
    return gcd(b % a, a)



def classical_shor(N):
    if(sympy.isprime(N) or N%2 == 0):
        return -1,-1
    for i in range(2,int(np.log2(N))):
        if (float(N**(1/i) - int(N**(1/i)) < 1e-10)):
            return -1,-1
    while(True):
        x = np.random.randint(3,N)
        if (gcd(x,N))!= 1:
            continue
        for i in range (2,26,2):
            temp = x**i
            if temp % N == 1:
                if (i % 2 ==1):
                    continue
                candidate_1 = int(gcd(x**(i/2)+1,N))
                candidate_2 = int(gcd(x**(i/2)-1,N))
                if(candidate_1 != 1 and candidate_2 !=1):
                    print(f"N:{N}, x:{x}, i:{i}")
                    return candidate_1,candidate_2
                else:
                    continue
            if (temp > 2**32/N):
                continue



def classical_shor_modified(N):
    if(sympy.isprime(N) or N%2 == 0):
        return -1,-1
    for i in range(2,int(np.log2(N))):
        if (float(N**(1/i) - int(N**(1/i)) < 1e-10)):
            return -1,-1
    while(True):
        x = np.random.randint(3,N)
        if (gcd(x,N))!= 1:
            continue
        eigenvalues,eigenvectors = np.linalg.eig(SimulatorM.QuantumMatrix(x,N))
        sr = (np.angle(eigenvalues) + 2*np.pi)/(2*np.pi)
        frac = Fraction(sr[1]).limit_denominator(20)
        r = frac.denominator
        if (r % 2 ==1):
            continue
        candidate_1 = int(gcd(x**(r/2)+1,N))
        candidate_2 = int(gcd(x**(r/2)-1,N))
        if(candidate_1 != 1 and candidate_2 !=1):
            print(f"N:{N}, x:{x}, r:{r}")
            return candidate_1,candidate_2
        else:
            continue

def Shor(N):

    if (np.log2(N)*2 + 1) > 20:
        raise Exception("TOO BIG")
    if sympy.isprime(N) or (N%2 == 0):
        return -1, -1
    for i in range(2, int(np.log2(N))):
        val = N ** (1 / i)
        if abs(val - round(val)) < 1e-10:
            return -1, -1

    while True:
        x = random.randint(3, N - 1)
        if gcd(x, N) != 1:
            continue
        n = int(np.log2(N)) + 1
        startpos = 0
        description = f"CxyModN {startpos} {x} {N}"

        binary_str = format(1, f'0{2*n+1}b')
        state_str = "INITSTATE BASIS |" + binary_str + ">"
        circ = circuit.Circuit(2 * n + 1)
        circ.set_state(state_str)

        estimated_phase = Phase_estimation.Phase_estimation(description, circ, n)
        if estimated_phase == 0:
            continue
        frac = Fraction(estimated_phase).limit_denominator(20)
        r = frac.denominator
        if (r % 2) == 1:
            continue

        candidate_1 = int(gcd(pow(x, r // 2, N) + 1, N))
        candidate_2 = int(gcd(pow(x, r // 2, N) - 1, N))
        if candidate_1 != 1 and candidate_2 != 1:
            return candidate_1, candidate_2