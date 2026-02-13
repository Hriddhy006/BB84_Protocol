from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit import QuantumCircuit, transpile

# 1. Create a Noise Model (Representing Eve or Link Interference)
noise_model = NoiseModel()
error_prob = 0.15  # 15% noise level
error = depolarizing_error(error_prob, 1)
noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3', 'h', 'x'])

# 2. Setup the Aer Simulator with the Noise Model
sim_noisy = AerSimulator(noise_model=noise_model)

# 3. Logic from alice.py: Prepare a Qubit
qc = QuantumCircuit(1, 1)
qc.h(0) # Alice sends in X-basis
qc.measure(0, 0)

# 4. Run the simulation
# transpiling ensures the circuit is optimized for the simulator
t_qc = transpile(qc, sim_noisy)
result = sim_noisy.run(t_qc, shots=1024).result()
counts = result.get_counts()

print(f"Noisy Results (QBER Analysis): {counts}")