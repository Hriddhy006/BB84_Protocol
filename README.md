# 🛡️ Quantum Mesh: Self-Healing BB84 Network

**Quantum Mesh** is a simulated quantum network environment that demonstrates the **BB84 protocol** integrated with an autonomous, self-healing routing system. It simulates quantum bit (qubit) transmission across a mesh network of European cities, detecting interference—such as an Eve-in-the-middle attack—and rerouting traffic through "quieter" quantum channels.

## To learn more about this topic please go through the PPTX file in the file section


## 🚀 Key Features

* **Quantum Simulation:** Uses **Qiskit** to generate and measure statevectors and **PennyLane** for quantum-enhanced anomaly detection.
* **BB84 Protocol:** Full implementation of bit encoding, basis selection, sifting, and Quantum Bit Error Rate (QBER) calculation.
* **Self-Healing Topology:** A **NetworkX**-powered backend that dynamically calculates the shortest "quantum-safe" path using Dijkstra’s algorithm, penalizing links with high noise or interception.
* **Real-Time Dashboards:** * **Main Dashboard:** Monitor the live network graph, sifting logs, and the final shared secret key.
    * **Interference Panel:** A "God Mode" (or "Eve Mode") to manually inject noise or attacks into specific geographic links.
* **Noise Modeling:** Simulates depolarizing errors and physical link interference via Qiskit Aer.

---

## 🏗️ System Architecture

The project operates on a hub-and-spoke model via a Flask server:

1. **Server (`server.py`)**: The central nervous system managing the global network state and qubit buffer.
2. **Alice (`alice.py`)**: The sender. Encodes random bits into random bases (Rectilinear/Diagonal) and ships them via the active route.
3. **Bob (`bob.py`)**: The receiver. Measures qubits in random bases and reports results to the server.
4. **The Dashboard (`dashboard.py`)**: A Streamlit interface that visualizes the network and performs autonomous rerouting.
5. **Evli Dashboard (`evli_dashboard.py`)**: The interface used to simulate link sabotage.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.9+
* **Qiskit** & **Qiskit-Aer**
* **Streamlit**
* **PennyLane**
* **NetworkX**, **Pandas**, **Flask**, **Matplotlib**

### Installation
```bash
git clone [https://github.com/your-username/BB84_Protocol.git](https://github.com/your-username/BB84_Protocol.git)
cd BB84_Protocol
pip install qiskit qiskit-aer streamlit pennylane networkx pandas flask matplotlib requests
