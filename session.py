from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Estimator, Options
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

qc0 = random_circuit(2, 2, seed=1).decompose(reps=1)
qc1 = random_circuit(2, 2, seed=1).decompose(reps=1)

qc01 = QuantumCircuit(2)
qc01.compose(qc0,[0,1],inplace=True)
qc01.compose(qc1,[0,1],inplace=True)

qc = QuantumCircuit(3)
qc.h(0)
# qc.compose(qc01.control(1),[0,1,2], inplace=True)
qc.compose(qc0.control(1), [0,1,2], inplace=True)
qc.compose(qc1.control(1), [0,1,2], inplace=True)

obs = SparsePauliOp(["IIX","IIZ"], np.array([0.5, -0.5]))

service = QiskitRuntimeService()
backend =  "simulator_statevector"
backend = "ibmq_belem" 
# backend =  "ibmq_qasm_simulator"

with Session(service=service, backend=backend) as session:
    estimator = Estimator(session=session)
    
    job = estimator.run(qc, obs)
    result = job.result()
    # Close the session only if all jobs are finished, and you don't need to run more in the session
    session.close()

print(result)