from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Estimator, Options
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

# create subcircuits
qc0 = random_circuit(2, 2, seed=1).decompose(reps=1)
qc1 = random_circuit(2, 2, seed=1).decompose(reps=1)

# compose them with a control
qc = QuantumCircuit(3)
qc.compose(qc0.control(1), [0,1,2], inplace=True)
qc.compose(qc1.control(1), [0,1,2], inplace=True)

# create observable
obs = SparsePauliOp(["IIX","IIZ"], np.array([0.5, -0.5]))

# init runtim
service = QiskitRuntimeService()
backend =  "simulator_statevector"
# backend = "ibmq_belem" 
# backend =  "ibmq_qasm_simulator"

# execute in a session
with Session(service=service, backend=backend) as session:
    estimator = Estimator(session=session)
    job = estimator.run(qc, obs)
    result = job.result()
    session.close()
