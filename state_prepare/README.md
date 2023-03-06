# Issue with state preparation

the following code :

```python
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
``` 

fails with the following error message:

```
2023-03-06T14:00:10.172706400Z Setting up watches.
2023-03-06T14:00:10.172786068Z Watches established.
2023-03-06T14:00:11.750388766Z INFO:     Started server process [7]
2023-03-06T14:00:11.750478954Z INFO:     Waiting for application startup.
2023-03-06T14:00:11.750766151Z INFO:     Application startup complete.
2023-03-06T14:00:11.752250537Z INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)
2023-03-06T14:00:48.270184676Z INFO:     127.0.0.1:56978 - "POST /run HTTP/1.1" 202 Accepted
2023-03-06T14:00:49.697884208Z webserver-starter - ERROR Failed to execute program: 'The num_qubits parameter to StatePreparation should only be used when params is an integer'
2023-03-06T14:00:49.698016931Z Traceback (most recent call last):
2023-03-06T14:00:49.698090725Z   File "/provider/server/main.py", line 60, in execute_program
2023-03-06T14:00:49.698125407Z     user_params=load_user_params(body.program_input_parameters_file, logger),
2023-03-06T14:00:49.698146160Z   File "/provider/programruntime/utils.py", line 73, in load_user_params
2023-03-06T14:00:49.698165436Z     user_params = json.loads(params, cls=ProgramRuntimeDecoder)
2023-03-06T14:00:49.698235061Z   File "/usr/lib64/python3.9/json/__init__.py", line 359, in loads
2023-03-06T14:00:49.698253845Z     return cls(**kw).decode(s)
2023-03-06T14:00:49.698273830Z   File "/usr/lib64/python3.9/json/decoder.py", line 337, in decode
2023-03-06T14:00:49.698981068Z     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
2023-03-06T14:00:49.699000426Z   File "/usr/lib64/python3.9/json/decoder.py", line 353, in raw_decode
2023-03-06T14:00:49.699019604Z     obj, end = self.scan_once(s, idx)
2023-03-06T14:00:49.699088177Z   File "/provider/programruntime/utils.py", line 297, in object_hook
2023-03-06T14:00:49.699106971Z     return _decode_and_deserialize(obj_val, load)[0]
2023-03-06T14:00:49.699125925Z   File "/opt/app-root/lib64/python3.9/site-packages/qiskit_ibm_runtime/utils/json.py", line 134, in _decode_and_deserialize
2023-03-06T14:00:49.699144283Z     return deserializer(buff)
2023-03-06T14:00:49.699207217Z   File "/opt/app-root/lib64/python3.9/site-packages/qiskit/qpy/interface.py", line 269, in load
2023-03-06T14:00:49.699226697Z     loader(
2023-03-06T14:00:49.699247909Z   File "/opt/app-root/lib64/python3.9/site-packages/qiskit/qpy/binary_io/circuits.py", line 905, in read_circuit
2023-03-06T14:00:49.699266327Z     _read_instruction(file_obj, circ, out_registers, custom_operations, version, vectors)
2023-03-06T14:00:49.699284373Z   File "/opt/app-root/lib64/python3.9/site-packages/qiskit/qpy/binary_io/circuits.py", line 277, in _read_instruction
2023-03-06T14:00:49.699348807Z     gate = gate_class(*params)
2023-03-06T14:00:49.699368593Z   File "/opt/app-root/lib64/python3.9/site-packages/qiskit/circuit/library/data_preparation/state_preparation.py", line 92, in __init__
2023-03-06T14:00:49.699387839Z     raise QiskitError(
2023-03-06T14:00:49.699406401Z qiskit.exceptions.QiskitError: 'The num_qubits parameter to StatePreparation should only be used when params is an integer'
2023-03-06T14:00:49.699546831Z /pod-data/ CLOSE_WRITE,CLOSE terminated
2023-03-06T14:00:49.706747699Z Termination marker file found. Kill process (7).
2023-03-06T14:00:49.729174956Z /bin/bash: line 3:     7 Killed                  python -m uvicorn server.main:app --port 8081
2023-03-06T14:00:49.729415730Z Termination signal received, exited.
```
