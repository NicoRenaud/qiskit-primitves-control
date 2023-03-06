from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Estimator, Options
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
import numpy as  np



# ensure the vector is double
b = np.random.rand(4)
vector = b.astype("float64")
vector /= np.linalg.norm(vector)
vector = vector.tolist()

# circuit to prepare the state
qc = QuantumCircuit(2)
qc.prepare_state(vector)

# # create the circuit
# qc_prep = StatePreparation(vector, num_qubits=None)
# circuit = QuantumCircuit(2)
# qc = circuit.compose(qc_prep, inplace=False)

# prep the vector if its norm is non nul
# circuit = random_circuit(2,2,seed=1).decompose(reps=1)

# create observable 
observable = SparsePauliOp("IY")

options = Options()
options.optimization_level = 2
options.resilience_level = 2

backend = "ibmq_qasm_simulator"
backend = "simulator_statevector"

service = QiskitRuntimeService()
with Session(service=service, backend=backend) as session:
    estimator = Estimator(session=session, options=options)
    job = estimator.run(qc, observable)
    result = job.result()
    # Close the session only if all jobs are finished, and you don't need to run more in the session
    session.close()


print(f" > Observable: {observable.paulis}")
print(f" > Expectation value: {result.values[0]}")
print(f" > Metadata: {result.metadata[0]}")