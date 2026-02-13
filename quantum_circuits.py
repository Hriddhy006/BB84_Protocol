from matplotlib import pyplot as plt
from qiskit import QuantumCircuit

def generate_circuit_diagram(bit, basis):
    qc = QuantumCircuit(1)
    if bit == 1: qc.x(0)
    if basis == 'X': qc.h(0)
    return qc.draw(output='mpl')

fig = generate_circuit_diagram(1, 'X')
plt.title("Alice's Encoding Circuit (Bit 1, X-basis)")

plt.show()
