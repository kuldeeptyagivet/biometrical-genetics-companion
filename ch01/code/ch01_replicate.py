"""Chapter 1 replication script: Nature and Structure of Animal Breeding Data.

Regenerates every number printed in sections 1.5, 1.7, 1.8 and the practical (1.9),
writes the input data to ../data and the results to ../output.
Run:  python ch01_replicate.py     (from this folder; needs numpy, pandas, scipy)
Step labels below match the chapter: Section 1.5 (herd sizes), practical 1.9 steps 5 and 6
(milk records), Section 1.8 and practical steps 7 to 9 (somatic cell counts), then the worked
example and the numerical problems. Change an input in the lists below and rerun to see the effect.
Each result is computed twice: by hand-written formulas (NumPy) and by a library
(SciPy / pandas). The script stops with an error if they disagree.
"""
import csv, json, math, os
import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "output")
os.makedirs(DATA, exist_ok=True); os.makedirs(OUT, exist_ok=True)

# ---- constructed inputs (Tables 1.2 and 1.4; practical 1.9) -------------------
pedigree = [(101, "S1", "D1", "F", 2019), (102, "S1", "D2", "F", 2019), (103, "S2", "D1", "F", 2020),
            (104, "S2", "D3", "F", 2020), (105, "S3", "D2", "F", 2020), (106, "S3", "0", "F", 2021),
            (107, "S2", "101", "F", 2022)]
perf = [(1, 101, "A", 2022, "Monsoon", 1, 33, 3410), (2, 101, "A", 2023, "Winter", 2, 46, 3905),
        (3, 102, "A", 2022, "Winter", 1, 31, 3120), (4, 103, "B", 2022, "Monsoon", 1, 34, 3590),
        (5, 103, "B", 2023, "Summer", 2, 47, 4010), (6, 104, "B", 2023, "Winter", 1, 33, 3350),
        (7, 105, "C", 2023, "Monsoon", 1, 32, 2980), (8, 106, "C", 2023, "Winter", 1, 30, 2870),
        (9, 106, "C", 2024, "Summer", 2, 43, 3260), (10, 107, "A", 2024, "Monsoon", 1, 32, 3180)]
scc = [45, 52, 60, 38, 71, 90, 110, 48, 66, 130, 85, 42, 55, 380, 74, 95, 160, 58, 49, 820, 68, 120, 77, 62]
# Al Kalaldeh et al. (2021), Table 1: herds and cows by herd size (1,2,...,11, 12-43)
herds = [2005, 1294, 547, 239, 78, 43, 17, 13, 11, 9, 5, 16]
cows = [2005, 2588, 1641, 956, 390, 258, 119, 104, 99, 90, 55, 258]

def write_csv(name, header, rows):
    with open(os.path.join(DATA, name), "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
write_csv("pedigree.csv", ["animal", "sire", "dam", "sex", "birth_year"], pedigree)
write_csv("performance.csv", ["record", "animal", "herd", "year", "season", "parity", "age_months", "milk_305d_kg"], perf)
write_csv("scc.csv", ["scc_thousand_per_ml"], [(v,) for v in scc])
write_csv("herd_size.csv", ["cows_per_herd_class", "herds", "cows"],
          [(l, h, c) for l, h, c in zip([str(i) for i in range(1, 12)] + ["12-43"], herds, cows)])

res, checks = {}, []
def check(name, mine, lib, tol=1e-9):
    ok = abs(mine - lib) <= tol * max(1.0, abs(lib))
    checks.append((name, mine, lib, ok))
    if not ok:
        raise SystemExit(f"MISMATCH {name}: hand={mine} library={lib}")
    res[name] = mine

# ---- Section 1.5: herd-size table (published totals) ---------------------------
res["herds_total"] = sum(herds); res["cows_total"] = sum(cows)
assert res["herds_total"] == 4277 and res["cows_total"] == 8563   # published totals
res["pct_cows_in_1cow_herds"] = round(100 * cows[0] / sum(cows), 1)
res["pct_cows_in_herds_le3"] = round(100 * sum(cows[:3]) / sum(cows), 1)

# ---- Practical: 10 milk records ----------------------------------------------
y = np.array([r[7] for r in perf], float)
n = len(y); m = y.sum() / n
sd = math.sqrt(((y - m) ** 2).sum() / (n - 1))
check("milk_mean", m, float(pd.Series(y).mean()))
check("milk_sd", sd, float(pd.Series(y).std(ddof=1)))
df = pd.DataFrame(perf, columns=["rec", "animal", "herd", "year", "season", "parity", "age", "milk"])
for h, g in df.groupby("herd"):
    hand = sum(r[7] for r in perf if r[2] == h) / sum(1 for r in perf if r[2] == h)
    check(f"herd_{h}_mean", hand, float(g.milk.mean()))
    res[f"herd_{h}_n"] = len(g)
res["animals_with_two_records"] = int((df.groupby("animal").size() == 2).sum())
res["herd_season_cells"] = len({(r[2], r[4]) for r in perf})
res["herd_season_cells_single"] = int((df.groupby(["herd", "season"]).size() == 1).sum())
res["herd_year_cells"] = len({(r[2], r[3]) for r in perf})
res["herd_year_season_cells"] = len({(r[2], r[3], r[4]) for r in perf})
# pedigree key checks
ids = {str(p[0]) for p in pedigree}; birth = {str(p[0]): p[4] for p in pedigree}
assert all(str(r[1]) in ids for r in perf)                      # every animal found in pedigree
assert birth["107"] > birth["101"]                               # offspring born after parent
res["pedigree_key_check"] = "pass"

# ---- Section 1.8 and practical: SCC on three scales ---------------------------
x = np.array(scc, float)
def hand_skew(a):
    d = a - a.mean(); return (d ** 3).mean() / (d ** 2).mean() ** 1.5
scales = {"original": x, "sqrt": np.sqrt(x), "ln": np.log(x)}
for k, a in scales.items():
    check(f"scc_{k}_mean", a.mean(), float(np.mean(a)))
    check(f"scc_{k}_median", float(np.median(a)), float(pd.Series(a).median()))
    sdh = math.sqrt(((a - a.mean()) ** 2).sum() / (len(a) - 1))
    check(f"scc_{k}_sd", sdh, float(pd.Series(a).std(ddof=1)))
    check(f"scc_{k}_skew", hand_skew(a), float(stats.skew(a)))
for k in ("original", "ln"):
    a = scales[k]; s = a.std(ddof=1)
    for v in (820, 380):
        val = v if k == "original" else math.log(v)
        check(f"z_{v}_{k}", (val - a.mean()) / s, float(stats.zscore(a, ddof=1)[scc.index(v)]))
check("geometric_mean", math.exp(np.log(x).mean()), float(stats.gmean(x)))
for p in (0.1, 0.25, 0.5, 0.75, 0.9):
    res[f"angle_p{p}"] = round(math.degrees(math.asin(math.sqrt(p))), 2)
res["sqrt_of_mean_scc"] = round(math.sqrt(x.mean()), 3)
# Spreadsheet SKEW() uses the sample-adjusted skewness g1*sqrt(n(n-1))/(n-2); the chapter uses the
# plain (population) form g1. Both are given so that a spreadsheet user is not confused.
nn = len(x)
for k in ("original", "ln"):
    g1 = hand_skew(scales[k]); adj = g1 * math.sqrt(nn * (nn - 1)) / (nn - 2)
    check(f"scc_{k}_skew_spreadsheet", adj, float(stats.skew(scales[k], bias=False)))

# ---- Worked Example 1.1 (section 1.8): four counts 40, 80, 160, 320 -------------------------
w = np.array([40, 80, 160, 320], float)
check("we1_mean", w.mean(), float(np.mean(w)))
check("we1_sd", math.sqrt(((w - w.mean()) ** 2).sum() / 3), float(np.std(w, ddof=1)))
check("we1_ln_mean", np.log(w).mean(), float(np.mean(np.log(w))))
check("we1_ln_sd", math.sqrt(((np.log(w) - np.log(w).mean()) ** 2).sum() / 3), float(np.std(np.log(w), ddof=1)))
check("we1_geo", math.exp(np.log(w).mean()), float(stats.gmean(w)))
res["we1_ln_values"] = [round(v, 4) for v in np.log(w)]

# ---- Worked solution for practical steps 5 and 6 --------------------------------------------
res["milk_sum"] = float(y.sum()); res["milk_ss_dev"] = round(float(((y - y.mean()) ** 2).sum()), 1)
res["herdA_sum"] = float(sum(r[7] for r in perf if r[2] == "A"))

# ---- Numerical problems --------------------------------------------------------
t = np.array([50, 100, 200], float)
check("prob1_arith", t.mean(), float(np.mean(t)))
check("prob1_geo", math.exp(np.log(t).mean()), float(stats.gmean(t)), 1e-12)
res["prob1_ln_values"] = [round(v, 3) for v in np.log(t)]
a1, a2 = (math.degrees(math.asin(math.sqrt(p))) for p in (0.36, 0.64))
res["prob2_angles"] = [round(a1, 2), round(a2, 2)]; res["prob2_diff"] = round(a2 - a1, 2)

with open(os.path.join(OUT, "results.json"), "w") as f:
    json.dump({k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items()}, f, indent=1)
with open(os.path.join(OUT, "verification_python.txt"), "w") as f:
    f.write("Hand-written NumPy formulas vs SciPy/pandas (tolerance 1e-9 relative)\n")
    for name, a, b, ok in checks:
        f.write(f"{name}: hand={a:.6f} library={b:.6f} {'OK' if ok else 'FAIL'}\n")
    f.write("Published totals (Al Kalaldeh et al. 2021, Table 1): 4277 herds and 8563 cows reproduced: OK\n")
print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in res.items()}, indent=1))
print(len(checks), "cross-checks passed")
