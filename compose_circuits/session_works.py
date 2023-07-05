from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Estimator, Options
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit import qpy 

# create subcircuits
qc0 = random_circuit(2, 2, seed=1).decompose(reps=1)
qc1 = random_circuit(2, 2, seed=2).decompose(reps=1)
qc2 = random_circuit(2, 2, seed=3).decompose(reps=1)

# compose them with a control
qc = QuantumCircuit(3)
qc.compose(qc0, [1,2], inplace=True)
qc.compose(qc1.control(1), [0,1,2], inplace=True)
qc.compose(qc2, [1,2], inplace=True)

# create observable
obs = SparsePauliOp(["IIX","IIZ"], np.array([0.5, -0.5]))

with open('ctrl.qpy','wb') as fd:
    qpy.dump(qc, fd)

with open('ctrl.qpy','rb') as fd:
    new_qc = qpy.load(fd)[0]

# service = QiskitRuntimeService()
# backend =  "simulator_statevector"
# # backend = "ibmq_belem" 
# # backend =  "ibmq_qasm_simulator"

# with Session(service=service, backend=backend) as session:
#     estimator = Estimator(session=session)
    
#     job = estimator.run(qc, obs)
#     result = job.result()
#     session.close()

# print(result)