import json, os, sys, statistics as st
import matplotlib.pyplot as plt

names = sys.argv[1:]
W = 50
series = {}
for n in names:
    t = [r["TotalDuration"] for r in json.load(open(f"../measurements/runs/{n}.json"))["Results"]]
    series[n] = [st.median(t[i:i + W]) for i in range(0, len(t) - W + 1, W)]

ref = series[names[0]]
x = [i * W for i in range(len(ref))]
fig, (a1, a2) = plt.subplots(2, 1, sharex=True, figsize=(12, 8))
for n, s in series.items():
    a1.plot(x, s, label=n)
    a2.plot(x, [v / r for v, r in zip(s, ref)], label=f"{n} / {names[0]}")
a2.axhline(1.0, color="k", lw=0.5)
a1.set_ylabel("medián TotalDuration [ms]"); a2.set_ylabel("pomer"); a2.set_xlabel("krok")
a1.legend(); a2.legend()
os.makedirs("output", exist_ok=True)
fig.savefig("output/close_drift.png", dpi=150)

for n, s in series.items():
    if n != names[0]:
        flips = [x[i] for i in range(1, len(s)) if (s[i] - ref[i]) * (s[i - 1] - ref[i - 1]) < 0]
        print(n, "prehodenie poradia v krokoch:", flips or "žiadne")
