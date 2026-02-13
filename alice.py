import requests, time, random
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

SERVER_URL = "http://127.0.0.1:5000"


def run_alice():
    batch_count = 0
    while True:
        try:
            state = requests.get(f"{SERVER_URL}/get_state").json()
            if state["delivery_status"] in ["WAITING_FOR_ALICE", "RECEIVED"]:
                batch_count += 1
                current_route = state.get("active_route")

                batch_data = []
                for _ in range(6):
                    bit, basis = random.randint(0, 1), random.choice(['Z', 'X'])
                    qc = QuantumCircuit(1)
                    if bit == 1: qc.x(0)
                    if basis == 'X': qc.h(0)
                    sv = [[c.real, c.imag] for c in Statevector.from_instruction(qc).data.tolist()]
                    batch_data.append({"sv": sv, "basis": basis, "bit": bit})

                payload = {"batch_id": batch_count, "data": batch_data, "route_used": current_route}
                requests.post(f"{SERVER_URL}/send_qubits", json=payload)
                print(f"✅ Batch #{batch_count} sent on route: {current_route}")
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    run_alice()