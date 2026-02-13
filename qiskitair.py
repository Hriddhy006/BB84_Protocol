from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit import QuantumCircuit, transpile


noise_model = NoiseModel()
error_prob = 0.15  # 15% noise level
error = depolarizing_error(error_prob, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3', 'h', 'x'])


sim_noisy = AerSimulator(noise_model=noise_model)


qc = QuantumCircuit(1, 1)
qc.h(0) 
qc.measure(0, 0)

t_qc = transpile(qc, sim_noisy)
result = sim_noisy.run(t_qc, shots=1024).result()
counts = result.get_counts()


print(f"Noisy Results (QBER Analysis): {counts}")
