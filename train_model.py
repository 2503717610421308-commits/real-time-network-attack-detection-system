import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier


DATA_DIR = os.path.join("model", "data")
MODEL_PATH = os.path.join("model", "attack_detection_model.pkl")
DATASET_PATH = os.path.join(DATA_DIR, "network_traffic.csv")

os.makedirs(DATA_DIR, exist_ok=True)


rng = __import__("random")

records = []
for _ in range(1200):
    if rng.random() < 0.55:
        packet_count = rng.randint(10, 120)
        packet_size = rng.randint(50, 280)
        connection_rate = rng.randint(1, 12)
        label = 0
    else:
        packet_count = rng.randint(180, 500)
        packet_size = rng.randint(350, 2200)
        connection_rate = rng.randint(18, 60)
        label = 1

    records.append({
        "packet_count": packet_count,
        "packet_size": packet_size,
        "connection_rate": connection_rate,
        "label": label,
    })


df = pd.DataFrame(records)
df.to_csv(DATASET_PATH, index=False)

X = df[["packet_count", "packet_size", "connection_rate"]]
y = df["label"]

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    max_depth=8,
)
model.fit(X, y)

joblib.dump(model, MODEL_PATH)
print(f"Model trained and saved to {MODEL_PATH}")
print(f"Dataset saved to {DATASET_PATH}")
print(f"Dataset rows: {len(df)}")
