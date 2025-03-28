class Circuit:
    def __init__(self, num_wires):
        self.num_wires = num_wires
        self.commands = []
        self.commands.append(str(self.num_wires))
    
    def get_wirenum(self):
        return self.num_wires

    def set_state(self,file_string):
        if (len(self.commands)>1):
            if(self.commands[1].split())[0] == "INITSTATE":
                self.commands[1] = file_string
        else:
            self.commands.insert(1,file_string)

        
    def add_gate(self, gate_str):
        self.commands.append(gate_str)
        
    def add_H(self, wire):
        self.add_gate("H " + str(wire))

    def add_P(self, wire, theta):
        self.add_gate("P {} {}".format(wire, theta))
        
    def add_CNOT(self, control, target):
        self.add_gate("CNOT {} {}".format(control, target))
        
    def add_SWAP(self, wire1, wire2):
        self.add_gate("SWAP {} {}".format(wire1, wire2))
        
    def add_CPHASE(self, control, target, angle):
        self.add_gate("CPHASE {} {} {}".format(control, target, angle))
        
    def add_measure(self):
        self.add_gate("MEASURE")
        
    def to_string(self):
        return "\n".join(self.commands)
    
