## Issue with controlled subcircuit and primitives

The following code (see session.py) crashes

```python

from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Estimator, Options
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

qc = QuantumCircuit(3)
qc.compose(qc0.control(1), [0,1,2], inplace=True)
qc.compose(qc1.control(1), [0,1,2], inplace=True)

obs = SparsePauliOp(["IIX","IIZ"], np.array([0.5, -0.5]))

service = QiskitRuntimeService()
backend =  "simulator_statevector"

with Session(service=service, backend=backend) as session:
    estimator = Estimator(session=session)
    job = estimator.run(qc, obs)
    result = job.result()
    session.close()
``` 
The code crashes with the following error 
```
raise RuntimeJobFailureError(
qiskit_ibm_runtime.exceptions.RuntimeJobFailureError: 'Unable to retrieve job result. Job cfsdnlrmcdu64k5e3vfg has failed:\n
2023-02-24T15:40:35.272526810Z Setting up watches.\n
2023-02-24T15:40:35.272636707Z Watches established.\n
2023-02-24T15:40:39.160368901Z INFO:     Started server process [7]\n
2023-02-24T15:40:39.160443689Z INFO:     Waiting for application startup.\n
2023-02-24T15:40:39.161004923Z INFO:     Application startup complete.\n
2023-02-24T15:40:39.164282158Z INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)\n
2023-02-24T15:46:31.914113195Z INFO:     127.0.0.1:42780 - "POST /run HTTP/1.1" 202 Accepted\n
2023-02-24T15:46:35.423550954Z webserver-starter - ERROR Failed to execute program: unpack requires a buffer of 33 bytes\n
2023-02-24T15:46:35.423607535Z Traceback (most recent call last):\n
2023-02-24T15:46:35.423626454Z   File "/provider/server/main.py", line 60, in execute_program\n
2023-02-24T15:46:35.423639632Z     user_params=load_user_params(body.program_input_parameters_file, logger),\n
2023-02-24T15:46:35.423657419Z   File "/provider/programruntime/utils.py", line 73, in load_user_params\n
2023-02-24T15:46:35.423672619Z     user_params = json.loads(params, cls=ProgramRuntimeDecoder)\n
2023-02-24T15:46:35.423687826Z   File "/usr/lib64/python3.9/json/__init__.py", line 359, in loads\n
2023-02-24T15:46:35.423700748Z     return cls(**kw).decode(s)\n
2023-02-24T15:46:35.423717291Z   File "/usr/lib64/python3.9/json/decoder.py", line 337, in decode\n
2023-02-24T15:46:35.423732049Z     obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n
2023-02-24T15:46:35.423747118Z   File "/usr/lib64/python3.9/json/decoder.py", line 353, in raw_decode\n
2023-02-24T15:46:35.423761642Z     obj, end = self.scan_once(s, idx)\n
2023-02-24T15:46:35.423776062Z   File "/provider/programruntime/utils.py", line 297, in object_hook\n
2023-02-24T15:46:35.423791029Z     return _decode_and_deserialize(obj_val, load)[0]\n
2023-02-24T15:46:35.423806100Z   File "/opt/app-root/lib64/python3.9/site-packages/qiskit_ibm_runtime/utils/json.py", line 134, in _decode_and_deserialize\n
2023-02-24T15:46:35.423821202Z     return deserializer(buff)\n
2023-02-24T15:46:35.423835224Z   File "/opt/app-root/lib64/python3.9/site-packages/qiskit/qpy/interface.py", line 269, in load\n
2023-02-24T15:46:35.423849164Z     loader(\n
2023-02-24T15:46:35.423864000Z   File "/opt/app-root/lib64/python3.9/site-packages/qiskit/qpy/binary_io/circuits.py", line 871, in read_circuit\n
2023-02-24T15:46:35.423884614Z     _read_instruction(file_obj, circ, out_registers, custom_operations, version, vectors)\n
2023-02-24T15:46:35.423899538Z   File "/opt/app-root/lib64/python3.9/site-packages/qiskit/qpy/binary_io/circuits.py", line 161, in _read_instruction\n
2023-02-24T15:46:35.423913459Z     struct.unpack(\n
2023-02-24T15:46:35.423928694Z struct.error: unpack requires a buffer of 33 bytes\n
2023-02-24T15:46:35.425425338Z /pod-data/ CLOSE_WRITE,CLOSE terminated\n
2023-02-24T15:46:35.426554604Z Termination marker file found. Kill process (7).\n
2023-02-24T15:46:35.455574572Z /bin/bash: line 3:     7 Killed                  python -m uvicorn server.main:app --port 8081\n
2023-02-24T15:46:35.455776693Z Termination signal received, exited.\n'
```

## Possible fix

It seems that the issue is related to the controlled circuit as the replacing for example

```python
qc.compose(qc1.control(1), [0,1,2], inplace=True)
``` 

by

```python
qc.compose(qc1, [1,2], inplace=True)
```

fixes the problem. 

## Other fix
Similarly creating the circuit as below also works (see session_works.py)

```python
qc01 = QuantumCircuit(2)
qc01.compose(qc0, [0,1], inplace=True)
qc01.compose(qc1, [0,1], inplace=True)


qc = QuantumCircuit(3)
qc.compose(qc01.control(1), [0,1,2], inplace=True)
```

