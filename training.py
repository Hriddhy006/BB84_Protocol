import pennylane as qml
from pennylane import numpy as np
import pandas as pd


data = pd.read_csv('training_data.csv')
X = data['qber'].values
Y = data['label'].values 

dev = qml.device("default.qubit", wires=1)

@qml.qnode(dev)
def circuit(weights, x):
    qml.RY(x * np.pi, wires=0)
    qml.RX(weights, wires=0)
    return qml.expval(qml.PauliZ(0))

def cost(weights):
    predictions = [circuit(weights, x) for x in X]
   
    return np.mean((np.array(predictions) - (1 - 2*Y))**2)


opt = qml.GradientDescentOptimizer(stepsize=0.1)
weights = np.array(0.5, requires_grad=True)

print("Training the PennyLane Eye...")
for i in range(50):
    weights = opt.step(cost, weights)
    if i % 10 == 0:
        print(f"Step {i}: Cost = {cost(weights):.4f}")


print(f"Optimal Weight for your Dashboard: {weights}")
