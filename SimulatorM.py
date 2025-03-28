import numpy as np
from functools import reduce
import string_processing
import scipy
def H(wire, state):
    num_wire = int(np.log2(len(state)))
    mat = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    return np.kron(np.kron(np.identity(2**wire), mat),
                   np.identity(2**(num_wire - wire - 1)))

def P(wire, theta, state):
    num_wire = int(np.log2(len(state)))
    mat = np.array([[1, 0], [0, np.exp(1j * theta)]])
    return np.kron(np.kron(np.identity(2**wire), mat),
                   np.identity(2**(num_wire - wire - 1)))

def CNOT(control, target, state):
    num_wire = int(np.log2(len(state)))
    I = np.identity(2)
    X = np.array([[0, 1], [1, 0]])
    P0 = np.array([[1, 0], [0, 0]])
    P1 = np.array([[0, 0], [0, 1]])
    ops0 = []
    ops1 = []
    for qubit_index in range(num_wire):
        if qubit_index == control:
            ops0.append(P0)
            ops1.append(P1)
        elif qubit_index == target:
            ops0.append(I)
            ops1.append(X)
        else:
            ops0.append(I)
            ops1.append(I)
    return reduce(np.kron, ops0) + reduce(np.kron, ops1)

def SimA(myInput_lines):
    wire_num, command_collection = string_processing.ReadInputString(myInput_lines)
    state_vec = np.full(int(2**wire_num),0,dtype = 'complex')
    state_vec[0] = 1
    ret = np.eye(int(2**wire_num), dtype=complex)
    for command in command_collection:
        if command[0] == "INITSTATE":
            if command[1]=="FILE":
                state_vec = string_processing.gState(command[3],wire_num)
            else:
                state_vec = string_processing.DiracToVec([(1,command[3][1:-1])])
        if command[0] == "H":
            U_gate = H(int(command[1]), state_vec)
        elif command[0] == "P":
            U_gate = P(int(command[1]), float(command[2]), state_vec)
        elif command[0] == "CNOT":
            U_gate = CNOT(int(command[1]), int(command[2]), state_vec)
        elif command[0] == "MEASURE":
            ret = U_gate @ ret
            final_state = ret @ state_vec
            prob = np.abs(final_state)**2
            prob = prob / np.sum(prob)
            pp = np.random.random()
            prob_cum = np.cumsum(prob)
            index = np.searchsorted(prob_cum, pp)
            final_state[:] = 0
            final_state[index] = 1
            return string_processing.VecToDirac(final_state)
        else:
            raise Exception("Invalid Command")
        ret = U_gate @ ret
    final_state = ret @ state_vec
    return string_processing.VecToDirac(final_state)

def SimB(myInput_lines):
    wire_num, command_collection = string_processing.ReadInputString(myInput_lines)
    state_vec = np.full(int(2**wire_num),0,dtype = 'complex')
    state_vec[0] = 1
    for command in command_collection:
        if command[0] == "INITSTATE":
            if command[1]=="FILE":
                state_vec = string_processing.gState(command[3],wire_num)
            else:
                state_vec = string_processing.DiracToVec([(1,command[3][1:-1])])
        elif command[0] == "H":
            state_vec = H(int(command[1]), state_vec) @ state_vec
        elif command[0] == "P":
            state_vec = P(int(command[1]), float(command[2]), state_vec) @ state_vec
        elif command[0] == "CNOT":
            state_vec = CNOT(int(command[1]), int(command[2]), state_vec) @ state_vec
        elif command[0] == "MEASURE":
            prob = np.abs(state_vec)**2
            prob = prob / np.sum(prob)
            pp = np.random.random()
            prob_cum = np.cumsum(prob)
            index = np.searchsorted(prob_cum, pp)
            state_vec[:] = 0
            state_vec[index] = 1
            return string_processing.VecToDirac(state_vec)
        else:
            raise Exception("Invalid Command")
    return string_processing.VecToDirac(state_vec)

def QuantumMatrix(x, N):
    
    matrix = np.zeros((2**int(np.ceil(np.log2(N))), 2**int(np.ceil(np.log2(N)))))
    for i in range(2**int(np.ceil(np.log2(N)))):
        if i < N:
            matrix[i*x % N][i] = 1
        else:
            matrix[i][i] = 1
    return matrix

        
def xyModN(startpos,x,N,state):
    copy_state = state.copy()
    length = np.log2(len(state))
    matrix = scipy.sparse.kron(scipy.sparse.csr_matrix(scipy.sparse.identity(2**(startpos))),Quantum_matrix(x,N,length-startpos))
    return matrix @ state
    
            