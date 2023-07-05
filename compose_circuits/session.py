from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Estimator, Options
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit import qpy 

# create subcircuits
qc0 = random_circuit(2, 2, seed=1).decompose(reps=1)
qc1 = random_circuit(2, 2, seed=1).decompose(reps=1)
qc2 = random_circuit(2, 2, seed=1).decompose(reps=1)

# compose them with a control
qc_app = QuantumCircuit(3)
qc_comp = QuantumCircuit(3)

qc_app.append(qc0.control(1), [0,1,2])
qc_app.append(qc1.control(1), [0,1,2])
# qc_app.append(qc2.control(1), [0,1,2])

qc_comp.compose(qc0.control(1), [0,1,2], inplace=True)
qc_comp.compose(qc1.control(1), [0,1,2], inplace=True)
# qc_comp.compose(qc2.control(1), [0,1,2], inplace=True)

# qc_comp.data[0].operation.name  = qc_app.data[0].operation.name 


# with open('comp.qpy','wb') as fd:
#     qpy.dump(qc_comp, fd)

with open('app.qpy','wb') as fd:
    qpy.dump(qc_app, fd)

# with open('app.qpy','rb') as fd:
#     new_qc_app = qpy.load(fd)[0]

# with open('comp.qpy','rb') as fd:
#     new_qc_comp = qpy.load(fd)[0]


# assert new_qc == qc_comp 

# # init runtim
# service = QiskitRuntimeService()
# backend =  "simulator_statevector"
# # backend = "ibmq_belem" 
# # backend =  "ibmq_qasm_simulator"

# # execute in a session
# with Session(service=service, backend=backend) as session:
#     estimator = Estimator(session=session)
#     job = estimator.run(qc, obs)
#     result = job.result()
#     session.close()
