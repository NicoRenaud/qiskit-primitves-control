# Issue with different backends with noise

The backends defined through the `Aer` estimator as:

```python
device = FakeGuadalupe()
seed = 170
coupling_map = device.configuration().coupling_map
noise_model = NoiseModel.from_backend(device)
estimator_fake = AerEstimator(
    backend_options={
        "method": "density_matrix",
        "coupling_map": coupling_map,
        "noise_model": noise_model,
    },
    run_options={"seed": seed, "shots": 10000},
    transpile_options={"seed_transpiler": seed},
)
```

and a backend defined via the `BackendEstimator`

```python
estimator_fake_2 = BackendEstimator(device)
```

give widely different results. The `Aer` seems to be giving reasonable results but the other one not. See notebook for details

