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
import Shor
## January 27th 2025
## Yiming Sun
## Quantum Simulator

## FUNCTION for testing
def random_command_string(num_wires, num_commands):
    commands = []
    commands.append(str(num_wires))
    command_types = ['H', 'P', 'CNOT']
    for _ in range(num_commands):
        ctype = random.choice(command_types)
        if ctype == 'H':
            wire = random.randint(0, num_wires - 1)
            commands.append(f"H {wire}")
        elif ctype == 'P':
            wire = random.randint(0, num_wires - 1)
            theta = random.uniform(0, 2 * np.pi)
            commands.append(f"P {wire} {theta:.3f}")
        elif ctype == 'CNOT':
            control = random.randint(0, num_wires - 1)
            target = random.randint(0, num_wires - 1)
            while target == control:
                target = random.randint(0, num_wires - 1)
            commands.append(f"CNOT {control} {target}")
    return "\n".join(commands)
def random_vector(n):
    dim = 2**n
    vec = np.random.randn(dim) + 1j * np.random.randn(dim)
    vec /= np.linalg.norm(vec)
    return vec
def plot_theta_distribution(thetas, num_bins=30):
    counts, bin_edges = np.histogram(thetas, bins=num_bins, density=True)
    
    centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    plt.figure(figsize=(8,6))
    plt.bar(centers, counts, width=(bin_edges[1]-bin_edges[0]), 
            color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel("Predicted Theta (radians)")
    plt.ylabel("Probability Density")
    plt.title("Probability Distribution of Predicted Theta")
    plt.axhline(0.1432394487827058, color='red', linestyle='--', label=f"Reference = {0.1432394487827058}")
    plt.show()



## Test begins:

## Test on String reading
# myState2=[
#    (np.sqrt(0.1)*1.j, '101'),
#    (np.sqrt(0.5), '000') ,
#    (-np.sqrt(0.4), '010' )]
# print("The Binary representation is:")
# (string_processing.PrettyPrintBinary(myState2))
# print("The decimal representation is:")
# (string_processing.PrettyPrintInteger(myState2))

# ## Testing vectorize functions
# print("THe vectorized representation is:")
# print(string_processing.DiracToVec(myState2))
# print("Which transferes to this:")
# vecstate = string_processing.DiracToVec(myState2)
# string_processing.PrettyPrintBinary(string_processing.VecToDirac(vecstate))



## Testing the Simulator S
# print("Now begin testing Simulator S")
# command_string = ('''
# 5
# P 3 6.27268427646
# H 4
# H 4
# P 1 5.10940500719
# P 1 4.9078263081
# CNOT 1 2
# P 3 0.49543462544
# P 2 3.83472723148
# H 4
# P 4 0.771206773752
# H 1
# CNOT 3 2
# H 3
# H 1
# CNOT 3 4
# CNOT 2 1
# H 3
# CNOT 0 1
# CNOT 0 1
# H 2
# CNOT 2 1
# P 3 4.9383121224
# CNOT 2 1
# H 1
# P 4 3.2883684441
# P 2 4.61949080556
# P 2 0.918989863254
# H 2
# P 2 3.10718130134
# CNOT 1 0
# CNOT 3 4
# P 4 4.9188406848
# H 3
# CNOT 3 4
# P 4 2.51037456068
# P 1 5.01293807682
# H 2
# CNOT 4 3
# P 3 0.945628001768
# CNOT 1 2
# H 3
# CNOT 2 1
# CNOT 1 0
# P 0 3.65276586215
# H 3
# H 0
# CNOT 1 2
# P 0 5.48166723266
# H 4
# CNOT 0 1
# CNOT 2 1
# H 0
# CNOT 2 3
# CNOT 2 3
# CNOT 1 0
# CNOT 1 2
# P 3 3.09910291231
# H 2
# P 0 4.62629990408
# P 0 0.613536553901
# H 4
# CNOT 0 1
# P 4 5.57649516772
# P 4 6.21800579498
# H 3
# CNOT 2 1
# CNOT 3 2
# P 0 5.48873760859
# CNOT 0 1
# H 3
# P 3 1.37899824562
# P 1 2.97479543629
# P 2 4.25967312042
# H 1
# P 2 1.18358991222
# H 4
# CNOT 1 0
# P 0 1.75820279861
# H 3
# H 1
# P 0 3.87614758734
# CNOT 1 0
# P 4 5.92692060653
# P 2 2.19007789964
# CNOT 0 1
# H 2
# CNOT 1 0
# P 0 4.4355136224
# P 2 5.39834474596
# P 4 3.88670062551
# P 1 4.25386222644
# P 3 3.89954154473
# P 2 1.49230397825
# CNOT 1 0
# CNOT 0 1
# H 4
# H 0
# P 3 3.23824985068
# H 3
# P 1 0.558258881544
# ''')

# string_processing.PrettyPrintBinary(SimulatorS.Sim(command_string))

# print("Now begin testing Simulator M-a")


# string_processing.PrettyPrintBinary(SimulatorM.SimA(command_string))

# print("Now begin testing Simulator M-b")

# string_processing.PrettyPrintBinary(SimulatorM.SimB(command_string))

## Test time used for each function
# time_S,time_MA,time_MB = [0],[0],[0]
# for gate in range(3,21):
#     init_state = string_processing.VecToDirac(random_vector(gate))
#     init_command = random_command_string(gate,gate)
#     if (time_S[-1]<100):
#         execution_timeS = timeit.timeit(lambda: SimulatorS.Sim(init_command, init_state), number=1)
#         time_S.append(execution_timeS)
#     if (time_MA[-1]<200):
#         execution_timeMA = timeit.timeit(lambda: SimulatorM.SimA(init_command, init_state), number=1)
#         time_MA.append(execution_timeMA)
#     if (time_MB[-1]<200):
#         execution_timeMB = timeit.timeit(lambda: SimulatorM.SimB(init_command, init_state), number=1)
#         time_MB.append(execution_timeMB)


# x = np.arange(21)
# plt.plot(x, time_S, marker='o', linestyle='-', color='blue', label='Simulator S')
# plt.plot(x, time_MA, marker='s', linestyle='--', color='green', label='Simulator M-a')
# plt.plot(x, time_MB, marker='^', linestyle='-.', color='red', label='Simulator M-b')
# plt.xlabel("Number of Qubits (n)")
# plt.ylabel("Execution Time (seconds)")
# plt.title("Execution Time vs. Number of Qubits")
# plt.legend()
# plt.show()

## Test measurement
# print("Now begin testing Measurement")
# test_file_1 = "test/measure_1.circuit"
# ff = open(test_file_1,'r')
# p_dist = np.full(int(2**5),0,dtype=complex)
# content = ff.read()
# for i in range(1000):
#     p_dist += (string_processing.DiracToVec(SimulatorS.Sim(content)))**2
# p_dist = p_dist/1000

# plt.plot(np.arange(2**5),p_dist)
# plt.xlabel("quantum states")
# plt.ylabel("probability")
# plt.show()
# print(f"The sum of the probabilities is {round(np.sum(p_dist),2)}")

# ## testing reading a specific state

# print("testing reading initial states")
# test_file_2 = "test/input.circuit"
# ff = open(test_file_2,'r')
# content = ff.read()
# string_processing.PrettyPrintBinary(SimulatorS.Sim(content))

## Testing Phase estimation:

# desc = '''
# 9
# H 0
# CPHASE 0 5 0.3
# P 1 0.3
# CNOT 4 7
# SWAP 2 8
# '''
# string_processing.PrettyPrintBinary(SimulatorS.Sim(Nonatomic.Compiler(desc)))

# # desc = "P 0 5"
# # circ = circuit.Circuit(9)
# # circ.set_state("INITSTATE BASIS |000000001>")
# # print(Phase_estimation.Phase_estimation(desc,circ,1))




# random_angs = np.random.uniform(0,2*np.pi,100)
# thetas = []
# for randang in random_angs:
#     desc = "P 0 " +str(randang)
#     circ = circuit.Circuit(7)
#     circ.set_state("INITSTATE BASIS |0000001>")
#     print(Phase_estimation.Phase_estimation(desc,circ,1))
#     print("\n")
#     thetas.append(Phase_estimation.Phase_estimation(desc,circ,1))


# plt.figure(figsize=(10,8))
# plt.plot(random_angs/(2*np.pi),thetas)
# plt.xlabel(r'$\phi/2 \pi$')
# plt.ylabel("Maximally predicted theta")
# plt.show()

# plot_theta_distribution(thetas)



# def plot_top_distribution(prob_control):
#     """
#     Given an array prob_control of length 2^N_control, plot
#     a bar chart with the probability of each integer outcome,
#     labeling them in binary if desired.
#     """
#     n_control = int(np.log2(len(prob_control)))
#     xvals = np.arange(len(prob_control))
#     labels = [f"{x:0{n_control}b}" for x in xvals]

#     fig, ax = plt.subplots(figsize=(10,6))
#     ax.bar(xvals, prob_control, color='skyblue', edgecolor='black')
#     ax.set_xticks(xvals)
#     ax.set_xticklabels(labels, rotation=90)
#     ax.set_xlabel("Top-wire Output (binary)")
#     ax.set_ylabel("Probability")
#     ax.set_title("Distribution over the Top Wires")
#     plt.tight_layout()
#     plt.show()


# ret = []
# for i in range(100):
#     desc = '''
# NOT 0
# P 0 0.3
# NOT 1
# '''
#     circ = circuit.Circuit(5)
#     ret.append(Phase_estimation.Phase_estimation(desc,circ,2))
# plt.hist(ret)
# plt.show()


# st = Phase_estimation.Phase_estimation(desc, circ, eigen_count=1)
# circ = circuit.Circuit(5)
# circ.set_state("INITSTATE FILE test/myInputState.txt")
# Phase_estimation.QFT(circ)
# string_processing.PrettyPrintBinary(SimulatorS.Sim(circ.to_string()))
# print(circ.to_string())
# Phase_estimation.InvQFT(circ)
# string_processing.PrettyPrintBinary(SimulatorS.Sim(circ.to_string()))
    

# print("Classical Shor of 247")
# print(Shor.classical_shor(247))
from fractions import Fraction
# x=20
# N=119
# eig = np.linalg.eigvals(SimulatorM.QuantumMatrix(x,N))
# sr = (np.angle(eig) + 2*np.pi)/(2*np.pi)
# frac = Fraction(phases[1]).limit_denominator(20)
# num=frac.denominator
# print(f"the period of Quantum matrix x={x},N={N} is {num}")
# print("Here's the result of modified Shor on 219")
# print(Shor.classical_shor_modified(219))


# desc1 = """3
# INITSTATE BASIS |011>
# xyModN 0 3 7
# MEASURE
# """

# print("=== Test 1: xyModN normal ===")
# print("Circuit Description:\n", desc1)
# result1 = SimulatorS.Sim(desc1)
# print("Result from simulator:\n", result1)
# print()



# desc2 = """4
# INITSTATE BASIS |1010>
# CxyModN 0 0 3 7
# MEASURE
# """

# print("=== Test 3: CxyModN controlled ===")
# print("Circuit Description:\n", desc2)
# result2 = SimulatorS.Sim(desc2)
# print("Result from simulator:\n", result2)
# print()

#print("HERE's The Quantum Shor's algorithm for 219")
print(Shor.Shor(35))