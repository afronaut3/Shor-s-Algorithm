import Nonatomic
import SimulatorS
import string_processing
import math, numpy as np
import circuit
import math

def Phase_estimation(eigen_circuit_string, circ, eigen_count):
    total_wires = circ.get_wirenum()
    N_control = total_wires - eigen_count

    for i in range(N_control):
        circ.add_H(i)

    lines = eigen_circuit_string.strip().splitlines()
    parsed = [l.strip().split() for l in lines if l.strip()]

    for i in reversed(range(N_control)):
        reps = 2 ** (N_control - i - 1)
        if len(parsed) == 1:
            cmd_type = parsed[0][0].upper()
            if cmd_type == "P":
                local_target = int(parsed[0][1])
                orig_angle = float(parsed[0][2])
                new_angle = orig_angle * reps
                circ.add_gate(f"CPHASE {i} {N_control + local_target} {new_angle}")
                continue
            elif cmd_type == "CXYMODN":
                # We have 3 tokens after "CxyModN": [startpos, x, N]
                startpos = int(parsed[0][1])
                x_val = int(parsed[0][2])
                mod_val = int(parsed[0][3])
                x_exp = pow(x_val, reps, mod_val)
                circ.add_gate(f"CxyModN {i} {startpos} {x_exp} {mod_val}")
                continue
        for _ in range(reps):
            for ln in lines:
                t = ln.strip().split()
                if not t or t[0].upper() == "INITSTATE":
                    continue
                if t[0].upper() == "NOT":
                    local_target = int(t[1])
                    full_target = N_control + local_target
                    circ.add_gate(f"CNOT {i} {full_target}")
                elif t[0].upper() == "P":
                    local_target = int(t[1])
                    full_target = N_control + local_target
                    angle = t[2]
                    circ.add_gate(f"CPHASE {i} {full_target} {angle}")
                else:
                    raise Exception(f"Unsupported gate '{t[0]}'")

    # Inverse QFT
    for i in range(N_control):
        for j in range(i):
            ang = -math.pi / (2 ** (i - j))
            circ.add_CPHASE(i, j, ang)
        circ.add_H(i)
    for i in range(N_control // 2):
        j = N_control - 1 - i
        circ.add_SWAP(i, j)
    circ.add_measure()
    c_str = circ.to_string()
    compiled_body = Nonatomic.Compiler(c_str)
    compiled_circuit = f"{total_wires}\n{compiled_body}"
    result = SimulatorS.Sim(compiled_circuit)

    st = string_processing.DiracToVec(result)
    idx = np.argmax(np.abs(st)**2)
    idx >>= eigen_count
    phase = idx * 2 * math.pi / (2 ** (total_wires - eigen_count))
    return phase





def QFT(circ):
    N = circ.get_wirenum()
    for i in reversed(range(N)):
        circ.add_H(i)
        for j in reversed(range(i)):
            ang = math.pi / (2 ** (i - j))
            circ.add_CPHASE(i, j, ang)
    for i in range(N // 2):
        j = N - 1 - i
        circ.add_SWAP(i, j)

def InvQFT(circ):
    N = circ.get_wirenum
    for i in range(N):
        for j in range(i):
            ang = -math.pi / (2 ** (i - j))
            circ.add_CPHASE(i, j, ang)
        circ.add_H(i)
    for i in range(N // 2):
        j = N - 1 - i
        circ.add_SWAP(i, j)