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
## Possible fix

It seems that the issue is relalted to the controlled circuit as the replacing for example

```python
qc.compose(qc1.control(1), [0,1,2], inplace=True)
``` 

by

```python
qc.compose(qc1, [1,2], inplace=True)
```

fixes the problem. 

## Other fix
Similarly creating the circuit following also works (see session_works.py)

```python
qc01 = QuantumCircuit(2)
qc01.compose(qc0, [0,1], inplace=True)
qc01.compose(qc1, [0,1], inplace=True)


qc = QuantumCircuit(3)
qc.compose(qc01.control(1), [0,1,2], inplace=True)
```

