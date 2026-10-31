import json, sys
src, *picks = sys.argv[1:]
res = [r for r in json.load(open(src))["Results"] if r["Status"] == "Ok"]
SKIP = {"KERNEL_DIR", "EXTERNAL_FORCE"}

# deduplikácia podľa plnej konfigurácie
best = {}
for r in res:
    key = tuple((p["Name"], p["Value"]) for p in r["Configuration"] if p["Name"] not in SKIP)
    if key not in best or r["TotalDuration"] < best[key]["TotalDuration"]:
        best[key] = r
ranked = sorted(best.values(), key=lambda r: r["TotalDuration"])
ref = {p["Name"]: p["Value"] for p in ranked[0]["Configuration"]}

if not picks:
    t0 = ranked[0]["TotalDuration"]
    for i, r in enumerate(ranked[:15]):
        diff = {p["Name"]: p["Value"] for p in r["Configuration"]
                if p["Name"] not in SKIP and ref.get(p["Name"]) != p["Value"]}
        print(f"{i:2d}  {r['TotalDuration']:7.2f} ms  +{100 * (r['TotalDuration'] / t0 - 1):5.1f} %  {diff}")
else:
    for i in map(int, picks):
        out = f"../measurements/configs/close_{i}.json"
        json.dump(ranked[i]["Configuration"], open(out, "w"), indent=2)
        print("wrote", out)
