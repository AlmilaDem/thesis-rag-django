"""
Compares the external reviewer's manual scores (1-5, Table 2.3) with the RAGAS scores
(reliability check of the automatic evaluation, thesis Section 2.4).

  - for all five criteria: Spearman correlation between manual and RAGAS scores
    (works although three RAGAS metrics are on a 0-1 scale)
  - for the two rubric criteria (clarity, hallucination control), which are on the same
    1-5 scale: exact agreement, within-one agreement and quadratic weighted Cohen's kappa

Run (after the reviewer has filled in human_scoring_form.xlsx and it is saved in the same folder):
      python agreement.py --set final
Output: results/<set>/agreement.csv
"""
import argparse

import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

import config
from experiment_io import results_dir

RUBRIC = ["clarity", "hallucination_control"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="final", choices=["pilot", "final"])
    args = parser.parse_args()
    out_dir = results_dir(args.set)
    human = pd.read_excel(out_dir / "human_scoring_form.xlsx", sheet_name="scoring")
    key = pd.read_csv(out_dir / "human_key.csv")
    ragas = pd.read_csv(out_dir / "ragas_scores.csv")
    merged = human.merge(key, on="sample_no").merge(ragas, on="answer_id", suffixes=("_human", "_ragas"))

    rows = []
    for c in config.CRITERIA:
        pair = merged[[f"{c}_human", f"{c}_ragas"]].dropna()
        if len(pair) < 3:
            continue
        h, r = pair[f"{c}_human"].astype(float), pair[f"{c}_ragas"].astype(float)
        row = {"criterion": c, "ragas_scale": "1-5" if c in RUBRIC else "0-1", "n": len(pair),
               "spearman_rho": round(spearmanr(h, r).correlation, 3)}
        if c in RUBRIC:
            h_i, r_i = h.round().astype(int), r.round().astype(int)
            row["exact_agreement_%"] = round((h_i == r_i).mean() * 100, 1)
            row["within_one_%"] = round(((h_i - r_i).abs() <= 1).mean() * 100, 1)
            row["weighted_kappa"] = round(cohen_kappa_score(h_i, r_i, weights="quadratic",
                                                            labels=[1, 2, 3, 4, 5]), 3)
        rows.append(row)
    result = pd.DataFrame(rows)
    result.to_csv(out_dir / "agreement.csv", index=False)
    print(result.to_string(index=False))
    print("\nRough reading: Spearman rho or weighted kappa < 0.40 weak, 0.40-0.60 moderate, "
          "0.60-0.80 substantial, > 0.80 very strong.")


if __name__ == "__main__":
    main()
