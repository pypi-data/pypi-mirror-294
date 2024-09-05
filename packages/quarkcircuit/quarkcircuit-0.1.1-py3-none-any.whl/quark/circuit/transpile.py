# Copyright (c) 2024 XX Xiao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Union
import itertools

from .circuit import *
from .matrix import gate_matrix_dict,u_mat,id_mat

def h2u(qubit: int) -> tuple:
    """Convert H gate to U3 gate tuple.

    Args:
        qubit (int): The qubit to apply the gate to.

    Returns:
        tuple: u3 gate information
    """
    return ('u', np.pi/2, 0.0, np.pi, qubit)

def s2u(qubit: int) -> tuple:
    """Convert S gate to U3 gate tuple.

    Args:
        qubit (int): The qubit to apply the gate to.

    Returns:
        tuple: u3 gate information
    """
    return ('u', 0.0, 0.7853981633974483, 0.7853981633974483, qubit)

def cx_decompose(control_qubit: int, target_qubit: int) -> list:
    """ Decompose CX gate to U3 gates and CZ gates 

    Args:
        control_qubit (int): The qubit used as control.
        target_qubit (int): The qubit targeted by the gate.

    Returns:
        list: List of U3 gates and CZ gates.
    """
    gates = []
    gates.append(h2u(target_qubit))
    gates.append(('cz', control_qubit, target_qubit))
    gates.append(h2u(target_qubit))
    return gates

def cy_decompose(control_qubit: int, target_qubit: int) -> list:
    """ Decompose CY gate with kak algorithm. 

    Args:
        control_qubit (int): The qubit used as control.
        target_qubit (int): The qubit targeted by the gate.

    Returns:
        list: List of U3 gates and CZ gates.
    """
    gates = []
    gates.append(('u',np.pi/2,-np.pi/2,np.pi/2,control_qubit))
    gates.append(('u',0.0,-np.pi,-np.pi,target_qubit))
    gates.append(('cz',control_qubit,target_qubit))
    gates.append(('u',0.0,-np.pi,-np.pi,target_qubit))
    gates.append(('u',np.pi/2,np.pi/2,-np.pi/2,control_qubit))
    return gates

def swap_decompose(qubit1: int, qubit2: int) -> list:
    """Decompose SWAP gate to U3 gates and CZ gates.

    Args:
        qubit1 (int): The first qubit to apply the gate to.
        qubit2 (int): The second qubit to apply the gate to.

    Returns:
        list: List of U3 gates and CZ gates.
    """
    gates = []
    gates.append(h2u(qubit2))
    gates.append(('cz',qubit1,qubit2))
    gates.append(h2u(qubit2))
    gates.append(h2u(qubit1))
    gates.append(('cz',qubit1,qubit2))
    gates.append(h2u(qubit1))
    gates.append(h2u(qubit2))
    gates.append(('cz',qubit1,qubit2))
    gates.append(h2u(qubit2))
    return gates

def iswap_decompose(qubit1: int, qubit2: int) -> list:
    """ Decompose iswap gate with qiskit decompose algorithm. 

    Args:
        qubit1 (int): The first qubit to apply the gate to.
        qubit2 (int): The second qubit to apply the gate to.

    Returns:
        list: List of U3 gates and CZ gates.
    """
    gates = []
    gates.append(('u',np.pi/2,-np.pi/2,np.pi/2,qubit1))
    gates.append(('u',np.pi/2,-np.pi/2,np.pi/2,qubit2))  
    gates.append(('cz',qubit1,qubit2))
    gates.append(('u',np.pi/2,0.0,-np.pi/2,qubit1))
    gates.append(('u',np.pi/2,0.0,np.pi/2,qubit2))    
    gates.append(('cz',qubit1,qubit2))
    gates.append(('u',np.pi/2,-np.pi,0.0,qubit1))
    gates.append(('u',np.pi/2,0.0,-np.pi,qubit2))  
    
    return gates

def u_dot_u(u_info1,u_info2):
    """Carry out u @ u and return a new u information

    Args:
        u_info1 (tuple): u gate information like ('u', 1.5707963267948966, 0.0, 3.141592653589793, 0)
        u_info2 (tuple): u gate information like ('u', 1.5707963267948966, 0.0, 3.141592653589793, 0)

    Returns:
        _tuple_: A new u gate information
    """
    assert(u_info1[-1] == u_info2[-1])
    u_mat1 = u_mat(*u_info1[1:-1])
    u_mat2 = u_mat(*u_info2[1:-1])
    
    new_u = u_mat2 @ u_mat1
    theta, phi, lamda, _ = u3_decompose(new_u)
    return ('u', theta, phi, lamda, u_info1[-1])

class Transpile:
    """The transpilation process involves converting the operations
    in the circuit to those supported by the device and swapping
    qubits (via swap gates) within the circuit to overcome limited
    qubit connectivity.
    """
    def __init__(self, qc: Union[QuantumCircuit,str,list], physical_qubit_list: list = None):
        if isinstance(qc, QuantumCircuit):
            self.nqubits = qc.nqubits
            self.ncbits = qc.ncbits
            self.gates = qc.gates
        elif isinstance(qc, str):
            qc =  QuantumCircuit()
            qc.from_openqasm2(qc)
            self.nqubits = qc.nqubits
            self.ncbits = qc.ncbits
            self.gates = qc.gates
        elif isinstance(qc, list):
            qc =  QuantumCircuit()
            qc.from_qlisp(qc)
            self.nqubits = qc.nqubits
            self.ncbits = qc.ncbits
            self.gates = qc.gates
        else:
            raise TypeError("Expected a Quark QuantumCircuit or OpenQASM 2.0 or qlisp, but got a {}.".format(type(qc)))
        
        self.virtual_qubit_list = [i for i in range(self.nqubits)]
        if physical_qubit_list is not None:
            assert(len(physical_qubit_list) == self.nqubits)
            self.physical_qubit_list = physical_qubit_list
            self.nqubits = max(physical_qubit_list)+1
            self.ncbits = len(physical_qubit_list)
        else:
            self.physical_qubit_list = [i for i in range(self.nqubits)]

    def _add_basic_swap(self, mid_qubit_list = None, print_details = False):
        """Inject swap gates into the original circuit to make it compatible with the backend's connectivity.

        Args:
            print_details (bool, optional): Print the ordinary of qubit index, after inject swap gates. Defaults to False.

        Returns:
            class: QuantumCircuit
        """
        # physical_qubit_list: physical qubit
        # virtual_qubit_list: the nth qubit line
        # mid_qubit_list: virtual qubit index, 
        # 每条line对应的虚拟比特指标在加入swap门后会发生变化
        # 初始（虚拟）线路的虚拟指标就是qubit line的指标
        new = []
        nswap = 0  
        if mid_qubit_list is None:
            mid_qubit_list = [i for i in range(self.nqubits)]
        elif isinstance(mid_qubit_list, tuple):
            mid_qubit_list = list(mid_qubit_list)    
        mid_vir_dict = dict(zip(mid_qubit_list,self.virtual_qubit_list))
        vir_phy_dict = dict(zip(self.virtual_qubit_list,self.physical_qubit_list))
        if print_details:
            print('Initial qubit index:',mid_qubit_list)
            print('physical qubit | qubit line --> after swap')
        for gate_info in self.gates:
            gate = gate_info[0]
            if gate in one_qubit_gates_avaliable.keys():
                mid0 = mid_vir_dict[gate_info[1]]
                new.append((gate,vir_phy_dict[mid0]))
            elif gate in two_qubit_gates_avaliable.keys():
                pos0 = mid_vir_dict[gate_info[1]]
                pos1 = mid_vir_dict[gate_info[2]]
                if (pos1 - pos0) > 1:
                    for i in range(pos0, pos1-1):
                        new.append(('swap',vir_phy_dict[i],vir_phy_dict[i+1]))
                        nswap += 1
                        mid_qubit_list[i],mid_qubit_list[i+1] =\
                        mid_qubit_list[i+1],mid_qubit_list[i]
                        mid_vir_dict = dict(zip(mid_qubit_list,self.virtual_qubit_list))
                        mid0 = mid_vir_dict[gate_info[1]]
                        mid1 = mid_vir_dict[gate_info[2]]
                    new.append((gate, vir_phy_dict[mid0], vir_phy_dict[mid1]))
                elif (pos0 - pos1) > 1:
                    for i in range(pos0, pos1+1, -1):
                        new.append(('swap',vir_phy_dict[i-1],vir_phy_dict[i]))
                        nswap += 1
                        mid_qubit_list[i-1],mid_qubit_list[i] =\
                        mid_qubit_list[i],mid_qubit_list[i-1]
                        mid_vir_dict = dict(zip(mid_qubit_list,self.virtual_qubit_list))
                        mid0 = mid_vir_dict[gate_info[1]]
                        mid1 = mid_vir_dict[gate_info[2]]
                    new.append((gate, vir_phy_dict[mid0], vir_phy_dict[mid1]))            
                elif abs(pos1 - pos0) == 1:
                    new.append((gate, vir_phy_dict[pos0], vir_phy_dict[pos1]))
            elif gate in one_qubit_parameter_gates_avaliable:
                if gate == 'u':
                    new.append((gate, gate_info[1], gate_info[2], gate_info[3], vir_phy_dict[mid_vir_dict[gate_info[4]]]))
                else:
                    new.append((gate, gate_info[1], vir_phy_dict[mid_vir_dict[gate_info[2]]]))
            elif gate in ['reset']:
                mid0 = mid_vir_dict[gate_info[1]]
                new.append((gate,vir_phy_dict[mid0]))             
            elif gate in ['measure']:
                for idx in range(len(gate_info[1])):
                    mid0 = mid_vir_dict[gate_info[1][idx]]
                    new.append((gate, [vir_phy_dict[mid0]], [gate_info[2][idx]]))
            elif gate in ['barrier']:
                #for idx in range(len(gate_info[1])):
                #    mid0 = mid_vir_dict[gate_info[1][idx]]
                #    new.append((gate, (vir_phy_dict[mid0],)))
                new.append((gate, tuple(vir_phy_dict[mid_vir_dict[gate_info[1][idx]]] for idx in range(len(gate_info[1])))))

            if print_details:
                for k,v in mid_vir_dict.items():
                    print(vir_phy_dict[v], '|', v,'--->',k)
                print(gate_info)
        return new, nswap, tuple(mid_qubit_list)
    
    def _basic_swap(self, print_details = False):
        new,nswap,after_swap = self._add_basic_swap(mid_qubit_list = None, print_details = print_details)
        self.gates = new

        print('Routing finished ! add {} swap gate(s)'.format(nswap))
        print('Physical qubits <--> Virtual qubits <--> After SWAP')
        for idx, Qi in enumerate(self.physical_qubit_list):
            print(f'     Q{Qi}       <-->       {self.virtual_qubit_list[idx]}       <-->       {after_swap[idx]}')
        return self
        
    def run_basic_swap(self, print_details = False):
        """Inject swap gates into the original circuit to make it compatible with the backend's connectivity.

        Args:
            print_details (bool, optional): Print the ordinary of qubit index, after inject swap gates. Defaults to False.

        Returns:
            class: QuantumCircuit
        """
        self._basic_swap(print_details = print_details)
        qcc = QuantumCircuit(self.nqubits,self.ncbits)
        qcc.gates = self.gates
        return qcc
    
    def _baisic_swap_minimal(self, print_details = False):
        permutations = list(itertools.permutations(self.virtual_qubit_list))
        nswap_list = []
        gates_list = []
        after_swap_list = []
        for idx,mid_qubit_list in enumerate(permutations):
            new, nswap, after_swap = self._add_basic_swap(mid_qubit_list = mid_qubit_list, print_details = print_details)
            nswap_list.append(nswap)
            gates_list.append(new)
            after_swap_list.append(after_swap)
        min_idx = nswap_list.index(min(nswap_list))
        self.gates = gates_list[min_idx]
        
        print('Routing finished ! add {} swap gate(s)'.format(nswap_list[min_idx]))
        print('Physical qubits <--> Virtual qubits <--> After SWAP')
        for idx, Qi in enumerate(self.physical_qubit_list):
            print(f'     Q{Qi}       <-->       {permutations[min_idx][idx]}       <-->       {after_swap_list[min_idx][idx]}')
        return self
    
    def run_basic_swap_minimal(self, print_details = False):
        self._baisic_swap_minimal(print_details = print_details)
        qcc = QuantumCircuit(self.nqubits,self.ncbits)
        qcc.gates = self.gates
        return qcc

    def _basic_gates(self):
        new = []
        for gate_info in self.gates:
            gate = gate_info[0]
            if gate in one_qubit_gates_avaliable.keys():
                gate_matrix = gate_matrix_dict[gate]
                theta,phi,lamda,_ = u3_decompose(gate_matrix)
                new.append(('u',theta,phi,lamda,gate_info[-1]))
            elif gate in one_qubit_parameter_gates_avaliable.keys():
                if gate == 'u':
                    new.append(gate_info)
                else:
                    gate_matrix = gate_matrix_dict[gate](*gate_info[1:-1])
                    theta,phi,lamda,_ = u3_decompose(gate_matrix)
                    new.append(('u',theta,phi,lamda,gate_info[-1]))
            elif gate in two_qubit_gates_avaliable.keys():
                if gate in ['cz']:
                    new.append(gate_info)
                elif gate in ['cx', 'cnot']:
                    _cx = cx_decompose(gate_info[1],gate_info[2])
                    new += _cx
                elif gate in ['swap']:
                    _swap = swap_decompose(gate_info[1],gate_info[2])
                    new += _swap
                elif gate in ['iswap']:
                    _iswap = iswap_decompose(gate_info[1], gate_info[2])
                    new += _iswap
                elif gate in ['cy']:
                    _cy = cy_decompose(gate_info[1], gate_info[2])
                    new += _cy
                else:
                    raise(TypeError(f'Input {gate} gate is not support now. Try kak please'))       
            elif gate in functional_gates_avaliable.keys():
                new.append(gate_info)
        self.gates = new
        print('Mapping to basic gates done !')
        return self
                          
    def run_basic_gates(self):
        self._basic_gates()
        qc =  QuantumCircuit(self.nqubits, self.ncbits)
        qc.gates = self.gates
        return qc

    def _u_gate_optimize(self):
        n = len(self.gates)
        ops = [[('@',)]+[('O',) for _ in range(n)] for _ in range(self.nqubits)]
        for gate_info in self.gates:
            gate = gate_info[0]
            if gate == 'u':
                if np.allclose(u_mat(*gate_info[1:-1]),id_mat) is False:
                    for idx in range(n-1,-1,-1):
                        if ops[gate_info[4]][idx] not in [('O',)]:
                            if ops[gate_info[4]][idx][0] == 'u':
                                uu_info = u_dot_u(ops[gate_info[4]][idx],gate_info)
                                if np.allclose(u_mat(*uu_info[1:-1]),id_mat) is False:
                                    ops[gate_info[4]][idx] = uu_info
                                else:
                                    ops[gate_info[4]][idx] = ('O',)
                            else:
                                ops[gate_info[4]][idx+1] = gate_info
                            break
            elif gate == 'cz':
                contrl_qubit = gate_info[1]
                target_qubit = gate_info[2]
                for idx in range(n-1,-1,-1):
                    if ops[contrl_qubit][idx] not in [('O',)] or ops[target_qubit][idx] not in [('O',)]:
                        ops[contrl_qubit][idx+1] = gate_info
                        ops[target_qubit][idx+1] = ('V',)
                        break
            elif gate == 'barrier':
                for idx in range(n-1,-1,-1):
                    e_ = [ops[pos][idx] for pos in gate_info[1]]
                    if all(e == ('O',) for e in e_) is False:
                        for jdx, pos in enumerate(gate_info[1]):
                            if jdx == 0:
                                ops[pos][idx+1] = gate_info
                            else:
                                ops[pos][idx+1]= ('V',)
                        break
            elif gate == 'reset':
                for idx in range(n-1,-1,-1):
                    if ops[gate_info[1]][idx] not in [('O',)]:
                        ops[gate_info[1]][idx+1] = gate_info
                        break
            elif gate == 'measure':
                for jdx,pos in enumerate(gate_info[1]):
                    for idx in range(n-1,-1,-1):
                        if ops[pos][idx] not in [('O',)]:
                            ops[pos][idx+1] = ('measure', [pos], [gate_info[2][jdx]])
                            break
            else:
                raise(TypeError(f'Only u and cz gate and functional gates are supported! Input {gate}'))
                        
        for idx in range(n,-1,-1):
            e_ = [ops[jdx][idx] for jdx in range(len(ops))]
            if all(e == ('O',) for e in e_) is False:
                cut = idx
                break
        #print('check',cut,ops)
        new = []
        for idx in range(1,cut+1):
            for jdx in range(len(ops)):
                if ops[jdx][idx] not in [('V',),('O',)]:
                    new.append(ops[jdx][idx])
        self.gates = new
        #print('check',cut,new)
        return self
    
    def run_u_gate_optimize(self):
        self._u_gate_optimize()
        qc =  QuantumCircuit(self.nqubits, self.ncbits)
        qc.gates = self.gates
        return qc
            
    def run(self, optimize_level=1):
        if optimize_level == 0:
            self._basic_swap()
        elif optimize_level == 0.5:
            self._baisic_swap_minimal()
        elif optimize_level == 1:
            self._baisic_swap_minimal()
        else:
            raise(ValueError('More optimize level is not support now!'))
            
        self._basic_gates()
        if optimize_level == 1:
            self._u_gate_optimize()
        qc = QuantumCircuit(self.nqubits, self.ncbits)
        qc.gates = self.gates
        print('Transpiled done !')
        return qc