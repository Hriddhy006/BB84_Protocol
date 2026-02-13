import requests
import time
import random
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

SERVER_URL = "http://127.0.0.1:5000"


def run_bob():
    print("📥 Bob: Initializing Quantum Receiver...")
    print("Monitoring for Basis Sifting and Noise interference...")
    print("-" * 50)

    last_processed_id = -1

    while True:
        try:
            
            state = requests.get(f"{SERVER_URL}/get_state").json()
            buffer = state.get("qubit_buffer")
            noise_map = state.get("noise_map", {})

            if buffer and buffer.get("batch_id") != last_processed_id:
                current_batch = buffer.get("data", [])
                current_route = buffer.get("route_used", [])
                last_processed_id = buffer.get("batch_id")


                path_noises = []
                if current_route:
                    for i in range(len(current_route) - 1):
                        k1 = f"{current_route[i]}-{current_route[i + 1]}"
                        k2 = f"{current_route[i + 1]}-{current_route[i]}"
                        path_noises.append(noise_map.get(k1, noise_map.get(k2, 0.1)))

                effective_noise = sum(path_noises) / len(path_noises) if path_noises else 0.1

                correct_bits = 0
                sifting_log = []


                for i, q in enumerate(current_batch):
                    bob_basis = random.choice(['Z', 'X'])  # BB84 Random Basis Selection
                    basis_match = (bob_basis == q['basis'])

                    status = "DISCARDED (Basis Mismatch)"
                    bit_value = "-"

                    if basis_match:
                        # Check for physical interference (Bit Flip)
                        if random.random() > effective_noise:
                            status = "KEPT (Success)"
                            bit_value = q['bit']
                            correct_bits += 1
                        else:
                            status = "ERROR (Noise Flip)"
                            bit_value = 1 - q['bit']

                    sifting_log.append({
                        "Bit ID": i + 1,
                        "Alice Basis": q['basis'],
                        "Bob Basis": bob_basis,
                        "Status": status,
                        "Resulting Key Bit": bit_value
                    })


                efficiency = correct_bits / len(current_batch)
                requests.post(f"{SERVER_URL}/report_bob", json={
                    "correct": correct_bits,
                    "efficiency": efficiency,
                    "sifting_log": sifting_log
                })

                print(
                    f"✅ Measured Batch #{last_processed_id} | Path Noise: {effective_noise:.2f} | Key Bits: {correct_bits}")

        except Exception as e:
            pass

        time.sleep(0.1)  # Fast polling


if __name__ == "__main__":
    run_bob()