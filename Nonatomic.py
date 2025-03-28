import numpy as np 
import string_processing


def Not(wire_num):
    return ("H " + wire_num +"\n" + "P " + wire_num + " " + str(np.pi)+"\n" + "H " + wire_num)

def Rz(wire_num, theta):
    theta = float(theta) 
    return (Not(wire_num) + "\n" +
            "P " + wire_num + " " + str(-1 * theta / 2) + "\n" +
            Not(wire_num) + "\n" +
            "P " + wire_num + " " + str(theta / 2))

def CRz(control,target,theta):
    ## Rz1 CNOT Rz2 CNOT
    theta = float(theta)
    return (Rz(target,theta/2) + "\n" + "CNOT " +control + " " + target +"\n" + "P "+target+" "+str(-theta/2) +"\n" + "CNOT " +control + " "+ target)

def CP(control,target,theta):
    theta = float(theta)
## after first step , 0 (control) gains a exp(-itheta/2) and 1(control) gains exp(itheta/2), after second step, 0|0 gains a exp(-itheta) and 11 is a exp(itheta) and 10 is 0 and 01 is 0, and after cnotting, 10 is exp(itheta) and 11 is 0, and after rz gate 10 is exp(itheta/2) and 11 is exp(itheta/2) after cnoting it back they remain, after another rz gate, 10 is 0 and 11 is exp (itheta)
    return (Rz(control,theta/2) + "\n" + Rz(target,theta/2) + "\n" + "CNOT " +control + " " + target +"\n" + "P "+target+" "+str(-theta/2) +"\n" + "CNOT " +control + " "+ target)

def Swap(first,second):
    ## only need to swap |1....0> and |0....1>, need not consider |0....0> or |1....1> since probability won't change, therefore, use 3 CNOTS
    return "CNOT " +first + " " + second +"\n" + "CNOT " +second + " "+ first +"\n" + "CNOT " +first + " "+ second

def Compiler(content):
    num_wires, command_collection = string_processing.ReadInputString(content)
    ret = ''''''
    ret = ret+str(num_wires) +"\n"
    for k in range(len(command_collection)):
        if command_collection[k][0] == "NOT":
            ret += Not(command_collection[k][1])
        elif command_collection[k][0] == "RZ":
            ret += Rz(command_collection[k][1], command_collection[k][2])
        elif command_collection[k][0] == "CPHASE":
            ret += CP(command_collection[k][1], command_collection[k][2], command_collection[k][3])
        elif command_collection[k][0] == "SWAP":
            ret += Swap(command_collection[k][1], command_collection[k][2])
        else:
            for i in range(len(command_collection[k])):
                ret += command_collection[k][i]
                if i != len(command_collection[k]) - 1:
                    ret += " "
        if k != len(command_collection) - 1:
            ret += "\n"
    return ret

    
