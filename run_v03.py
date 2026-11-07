"""Run v0.3 synthetic numeric-input interface; values are illustrative."""
import json
from dataclasses import asdict
from models.v03 import Inputs, compare, consistency_screen

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Synthetic comparison; NOT calibrated.")
    parser.add_argument("--bacteria-count", type=int, required=True)
    parser.add_argument("--phage-count", type=int, required=True)
    parser.add_argument("--antibiotic-mol-per-liter", type=float, required=True)
    parser.add_argument("--replicates", type=int, default=5)
    parser.add_argument("--diversity", choices=("low","medium","high"), default="medium")
    parser.add_argument("--phages", choices=("single","cocktail"), default="cocktail")
    parser.add_argument("--noise-weight", type=float, default=0.0)
    args = parser.parse_args()
    inputs = Inputs(args.bacteria_count,args.phage_count,
                    args.antibiotic_mol_per_liter,args.replicates,
                    args.diversity,args.phages)
    report = compare(inputs,weights={"noise":args.noise_weight})
    values = [x["final_mean_susceptibility"] for x in report["replicates"]]
    report["consistency_screen"] = consistency_screen(values)
    print(json.dumps(report,indent=2))

if __name__ == "__main__":
    main()
