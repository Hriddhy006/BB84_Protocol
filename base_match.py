import pandas as pd
import numpy as np


def run_basis_check(num_bits=15, simulate_eve=False):
    """
    A professional standalone utility to validate BB84 Basis Matching.
    """
    print(f"\n{'=' * 60}")
    print(f" BB84 BASIS MATCHING VALIDATOR (Eve Presence: {simulate_eve})")
    print(f"{'=' * 60}\n")

    # 1. Alice prepares bits and bases
    alice_bits = np.random.randint(2, size=num_bits)
    alice_bases = np.random.choice(['Rectilinear (+)', 'Diagonal (x)'], size=num_bits)

    # 2. Bob chooses random bases to measure
    bob_bases = np.random.choice(['Rectilinear (+)', 'Diagonal (x)'], size=num_bits)

    # 3. Simulation of the Quantum Channel
    bob_bits = []
    for i in range(num_bits):
        if not simulate_eve:
            # Secure Channel: If bases match, Bob gets Alice's bit perfectly
            if alice_bases[i] == bob_bases[i]:
                bob_bits.append(alice_bits[i])
            else:
                bob_bits.append(np.random.randint(2))  # Random result on mismatch
        else:
            # Eve (Intercept-Resend): Eve measures in a random basis
            eve_basis = np.random.choice(['Rectilinear (+)', 'Diagonal (x)'])
            # Eve's measurement result
            if eve_basis == alice_bases[i]:
                eve_bit = alice_bits[i]
            else:
                eve_bit = np.random.randint(2)

            # Bob measures the bit Eve resent
            if bob_bases[i] == eve_basis:
                bob_bits.append(eve_bit)
            else:
                bob_bits.append(np.random.randint(2))

    # 4. Sifting Comparison (The Table)
    results = []
    for i in range(num_bits):
        match = (alice_bases[i] == bob_bases[i])
        results.append({
            "Bit": i + 1,
            "Alice Basis": alice_bases[i],
            "Bob Basis": bob_bases[i],
            "Match?": "YES" if match else "no",
            "Action": "KEPT" if match else "DISCARD",
            "Alice Bit": alice_bits[i],
            "Bob Bit": bob_bits[i],
            "Error?": "!" if match and alice_bits[i] != bob_bits[i] else ""
        })

    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    # 5. Analysis
    kept_bits = df[df['Action'] == 'KEPT']
    errors = (kept_bits['Alice Bit'] != kept_bits['Bob_Bit']).sum() if not kept_bits.empty else 0
    qber = (errors / len(kept_bits)) * 100 if len(kept_bits) > 0 else 0

    print(f"\n{'-' * 60}")
    print(f"Total Bits: {num_bits}")
    print(f"Sifted Key Length: {len(kept_bits)}")
    print(f"Quantum Bit Error Rate (QBER): {qber:.2f}%")
    print(f"{'-' * 60}")

    if simulate_eve and qber > 11:
        print("RESULT: High QBER detected. This indicates an Intercept-Resend attack.")
    elif not simulate_eve and qber <= 5:
        print("RESULT: Low QBER. The link is secure and stable.")


if __name__ == "__main__":
    # Test 1: Secure Link
    run_basis_check(num_bits=12, simulate_eve=False)

    # Test 2: Attacked Link
    run_basis_check(num_bits=12, simulate_eve=True)