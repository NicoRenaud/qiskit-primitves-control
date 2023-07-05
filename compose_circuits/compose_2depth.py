from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Estimator, Options
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit import qpy 

# create subcircuits
qc0 = random_circuit(2, 2, seed=1).decompose(reps=1)


# compose them with a control
qc = QuantumCircuit(3)
qc.compose(qc0.control(1), [0,1,2], inplace=True)

qc2 = QuantumCircuit(4)
qc2.compose(qc.control(1), [0,1,2,3], inplace=True)



with open('qc.qpy','wb') as fd:
    qpy.dump(qc2, fd)



with open('qc.qpy','rb') as fd:
    new_qc_comp = qpy.load(fd)[0]


