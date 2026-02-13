import pandas as pd
import numpy as np
import random


def generate_eye_data(samples=500):
    data = []

    for _ in range(samples):
        # 50% chance of an attack scenario
        is_attack = random.choice([0, 1])

        if is_attack == 0:
            # Scenario: Safe Link (Low noise)
            qber = random.uniform(0.01, 0.08)  # 1% to 8%
            latency = random.uniform(10, 20)  # Stable ms
            stability_score = random.uniform(0.8, 1.0)
        else:
            # Scenario: Eve Present (High noise + anomalies)
            qber = random.uniform(0.12, 0.35)  # 12% to 35%
            latency = random.uniform(15, 40)  # More jittery
            stability_score = random.uniform(0.1, 0.5)

        data.append([qber, latency, stability_score, is_attack])

    # Save to CSV
    df = pd.DataFrame(data, columns=['qber', 'latency', 'stability', 'label'])
    df.to_csv('training_data.csv', index=False)
    print(f"Successfully generated {samples} rows of training data in training_data.csv")


if __name__ == "__main__":
    generate_eye_data()