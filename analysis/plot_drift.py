import json, matplotlib.pyplot as plt
import os
os.makedirs("output", exist_ok=True)
for name in ["drift_dragon_settled", "drift_dragon_falling"]:
    with open(f"../measurements/runs/{name}.json") as f:
        t = [r["TotalDuration"] for r in json.load(f)["Results"]]
    plt.plot(t, label=name, linewidth=0.8)
plt.xlabel("krok"); plt.ylabel("TotalDuration"); plt.legend()
plt.savefig("output/drift.png", dpi=150)
