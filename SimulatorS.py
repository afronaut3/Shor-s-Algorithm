import string_processing
import numpy as np
import cmath
## This is the implementation of Simulator S

def H(wire,VecState):
    Copy_state = VecState.copy()
    wire_num = int(np.log2(len(VecState)))
    for i in range(len(VecState)):
        if ((i >> (wire_num-wire-1)) & 1):
            VecState[i]=(1/(np.sqrt(2)))*(-Copy_state[i] + Copy_state[i - int(np.power(2,wire_num-wire-1))])
        else:
            VecState[i]=(1/(np.sqrt(2)))*(Copy_state[i] + Copy_state[i + int(np.power(2,wire_num-wire-1))])
    return VecState



def Phase(wire, theta,VecState):
    Copy_state = VecState.copy()
    wire_num = int(np.log2(len(VecState)))
    for i in range(len(VecState)):
        if ((i >> (wire_num - wire - 1)) & 1):
            VecState[i] = np.exp(1j*theta) * Copy_state[i]
    return VecState


def CNOT(control_wire,not_wire,VecState):
    Copy_state = VecState.copy()
    wire_num = int(np.log2(len(VecState)))
    for i in range(len(VecState)):
        if ((i>>(wire_num-control_wire-1)) & 1):
            if ((i >> (wire_num-not_wire-1))&1):
                VecState[i] = Copy_state[i-int(np.power(2,wire_num-not_wire-1))]
            else:
                VecState[i] = Copy_state[i+int(np.power(2,wire_num-not_wire-1))]
    return VecState

def xyModN_full(startpos, x, modulus, VecState):
    Dirac_state = string_processing.VecToDirac(VecState)
    ret = []
    for amplitude, bitstr in Dirac_state:
        substring = bitstr[startpos:]
        extracted = int(substring, 2)
        new_val = (extracted * x) % modulus
        new_sub = format(new_val, f'0{len(substring)}b')
        new_str = bitstr[:startpos] + new_sub
        ret.append((amplitude, new_str))
    return string_processing.DiracToVec(ret)

def control_xyModN(control, startpos, x, modulus, VecState):
    Dirac_state = string_processing.VecToDirac(VecState)
    ret = []
    for amp, bstr in Dirac_state:
        if bstr[control] == '1':
            substring = bstr[startpos:]
            extracted = int(substring, 2)
            new_val = (extracted * x) % modulus
            new_sub = format(new_val, f'0{len(substring)}b')
            new_str = bstr[:startpos] + new_sub
            ret.append((amp, new_str))
        else:
            ret.append((amp, bstr))
    return string_processing.DiracToVec(ret)

def Sim(myInput_lines):
    wire_num, command_collection = string_processing.ReadInputString(myInput_lines)
    state_vec = np.full(int(2**wire_num),0,dtype = 'complex')
    state_vec[0] = 1
    for command in command_collection:
        if command[0] == "INITSTATE":
            if command[1]=="FILE":
                state_vec = string_processing.gState(command[2],wire_num)
            else:
                state_vec = string_processing.DiracToVec([(1,command[2][1:-1])])
        elif (command[0]== "H"):
            state_vec = H(int(command[1]),state_vec)
        elif (command[0] == "P"):
            state_vec = Phase(int(command[1]),float(command[2]),state_vec)
        elif (command[0] == "CNOT"):
            state_vec = CNOT(int(command[1]),int(command[2]),state_vec)
        elif(command[0] == "xyModN"):
            state_vec = xyModN_full(int(command[1]),int(command[2]),int(command[3]),state_vec)
        elif(command[0] == "CxyModN"):
            state_vec = control_xyModN(int(command[1]),int(command[2]),int(command[3]),int(command[4]),state_vec)
        elif command[0] == "MEASURE":
            prob = np.abs(state_vec)**2
            prob = prob / np.sum(prob)
            pp = np.random.random()
            prob_cum = np.cumsum(prob)
            index = np.searchsorted(prob_cum, pp)
            state_vec[:] = 0
            state_vec[index] = 1
            return string_processing.VecToDirac(state_vec)
    return string_processing.VecToDirac(state_vec)