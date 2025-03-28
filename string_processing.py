import numpy as np

## This file contains useful information to parse and correctly read the input
## As well as format transformation,etc


def PrettyPrintBinary(myState):
    ret = ""
    myState.sort(key = lambda x: int(x[1]))
    ret += "("
    for i in range(len(myState)):
        ret+=str(round(myState[i][0],6))
        ret+=("|")
        ret+=str(myState[i][1])
        ret+=(">")
        if (i != (len(myState)-1)):
            ret+=(" + ")
    ret+=(")")
    print(ret)

## Also make it print integer
    
def PrettyPrintInteger(myState):
    ret = ""
    myState.sort(key = lambda x: int(x[1]))
    ret += "("
    for i in range(len(myState)):
        ret+=str(round(myState[i][0],6))
        ret+=("|")
        ret+=(str(int(myState[i][1],2)))
        ret+=(">")
        if (i != (len(myState)-1)):
            ret+=(" + ")
    ret+=(")")
    print(ret)


def DiracToVec(myState):
    ## fetch the number of wires
    
    num = len(myState[0][1])
    ret = np.full(np.power(2,num),0,dtype=complex)
    for item in myState:
        ret[int(item[1],2)] = item[0]
    return ret

def VecToDirac(myVec):
    ret = []
    num = int(np.log2(len(myVec)))
    for i in range(myVec.shape[0]):
        if (np.abs(myVec[i] ** 2)>=1e-10):
            temp = len(bin(i)[2:])
            dig = ""
            for _ in range(temp,num):
                dig +="0"
            dig += str(bin(i)[2:])
            ret.append([myVec[i],dig])
    return ret

def ReadInputString(myInput_lines):
    myInput=[]
    myInput_lines=myInput_lines.split('\n')
    myInput_lines = [ i for i in myInput_lines if i!='']
    numberOfWires=int(myInput_lines[0])
    for line in myInput_lines[1:]:
        myInput.append(line.split())
    return (numberOfWires,myInput)

def gState(file_address, wire_num):
    with open(file_address, 'r') as file:
        content = file.read()
    lines = [line for line in content.split('\n') if line.strip() != '']
    ret = np.full(2**wire_num, 0, dtype=complex)
    if len(lines) != 2**wire_num:
        raise ValueError("The number of lines in the file does not match 2**wire_num")
    for i, line in enumerate(lines):
        specific = line.split()
        ret[i] = float(specific[0]) + float(specific[1])*1j
        
    return ret
