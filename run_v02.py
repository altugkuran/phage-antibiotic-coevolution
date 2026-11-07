"""Generate synthetic v0.2 comparison table (20 scenarios)."""
import csv
from pathlib import Path
from models.v02 import scenarios, simulate_v02
root = Path(__file__).resolve().parent
(root / "results").mkdir(exist_ok=True)
with (root / "results" / "v02_summary.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(("scenario", "diversity", "phages", "antibiotic",
                     "final_mean_susceptibility", "final_compatibility_index"))
    for s in scenarios():
        a = simulate_v02(s)
        writer.writerow((s.name, s.diversity, s.phages, s.antibiotic,
                         float(a[-1, 7]), float(a[-1, 9])))
print("Wrote 20 synthetic v0.2 comparisons.")
