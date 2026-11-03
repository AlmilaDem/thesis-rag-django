"""
Additional statistics for Chapter 5 (added after external feedback).
Reads only existing result files; does not change any other script or result.

  1. Effect sizes: Kendall's W for each Friedman test, matched-pairs rank-biserial
     correlation (r_rb) for each pairwise Wilcoxon comparison.
  2. 95 % bootstrap confidence intervals for the mean difference between two strategies
     (resampling the questions, 10,000 resamples, seed 42).
  3. Holm correction of the Friedman p-values across the six criteria.
  4. Formatting x grounding interaction: for each question, the effect of a grounding
     strategy (G1 - G0, G2 - G0) is computed under each formatting strategy, and the
     Friedman test checks whether this effect differs between F0, F1 and F2.
  5. Sensitivity of the highest-scoring combination per question type to the weighting
     of the overall score.

Run:  python stats_extra.py --set final
Output: results/<set>/tables/extra_*.csv
"""
import argparse
import itertools

import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, rankdata, wilcoxon

import config
from experiment_io import results_dir

RUBRIC = ["clarity", "hallucination_control"]
RNG_SEED = 42
N_BOOT = 10_000


def holm(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    adj, run = np.empty_like(p), 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (len(p) - rank) * p[i]))
        adj[i] = run
    return adj


def rank_biserial(a, b):
    d = np.asarray(a) - np.asarray(b)
    d = d[d != 0]
    if len(d) == 0:
        return 0.0
    r = rankdata(np.abs(d))
    return (r[d > 0].sum() - r[d < 0].sum()) / r.sum()


def boot_ci(d, rng):
    d = np.asarray(d)
    idx = rng.integers(0, len(d), size=(N_BOOT, len(d)))
    means = d[idx].mean(axis=1)
    return np.percentile(means, [2.5, 97.5])


def factor_tests(df, factor, metrics, rng):
    levels = sorted(df[factor].unique())
    rows = []
    for m in metrics:
        wide = df.groupby(["question_id", factor])[m].mean().unstack(factor).dropna()
        n, k = len(wide), len(levels)
        chi2, p = friedmanchisquare(*[wide[lv] for lv in levels])
        row = {"criterion": m, "n_questions": n, "friedman_chi2": chi2, "friedman_p": p,
               "kendall_w": chi2 / (n * (k - 1))}
        pairs = list(itertools.combinations(levels, 2))
        raw = []
        for a, b in pairs:
            d = wide[a] - wide[b]
            raw.append(1.0 if (d == 0).all() else wilcoxon(wide[a], wide[b]).pvalue)
        for (a, b), p_adj in zip(pairs, holm(raw)):
            d = wide[a] - wide[b]
            lo, hi = boot_ci(d.values, rng)
            row[f"{a}-{b}_diff"] = d.mean()
            row[f"{a}-{b}_ci_low"] = lo
            row[f"{a}-{b}_ci_high"] = hi
            row[f"{a}-{b}_p_holm"] = p_adj
            row[f"{a}-{b}_r_rb"] = rank_biserial(wide[a], wide[b])
        rows.append(row)
    out = pd.DataFrame(rows)
    out["friedman_p_holm_across_criteria"] = holm(out["friedman_p"].values)
    return out


def interaction(df, metric):
    rows = []
    cell = df.groupby(["question_id", "formatting", "grounding"])[metric].mean().unstack(["formatting", "grounding"])
    for g in ["G1", "G2"]:
        eff = pd.DataFrame({f: cell[(f, g)] - cell[(f, "G0")] for f in ["F0", "F1", "F2"]}).dropna()
        chi2, p = friedmanchisquare(eff["F0"], eff["F1"], eff["F2"])
        rows.append({"metric": metric, "contrast": f"{g}-G0", "n_questions": len(eff),
                     "effect_under_F0": eff["F0"].mean(), "effect_under_F1": eff["F1"].mean(),
                     "effect_under_F2": eff["F2"].mean(), "friedman_chi2": chi2, "friedman_p": p,
                     "kendall_w": chi2 / (len(eff) * 2)})
    out = pd.DataFrame(rows)
    out["p_holm"] = holm(out["friedman_p"].values)
    return out


def sensitivity(df):
    scaled = {c: ((df[c] - 1) / 4 if c in RUBRIC else df[c]) for c in config.CRITERIA}
    s = pd.DataFrame(scaled)
    schemes = {
        "equal_5": {c: 1 for c in config.CRITERIA},
        "without_clarity": {c: (0 if c == "clarity" else 1) for c in config.CRITERIA},
        "support_double": {c: (2 if c in ("faithfulness", "hallucination_control") else 1) for c in config.CRITERIA},
        "correctness_double": {c: (2 if c == "technical_correctness" else 1) for c in config.CRITERIA},
    }
    rows = []
    d = df.assign(condition=df["formatting"] + "+" + df["grounding"])
    for name, w in schemes.items():
        tot = sum(w.values())
        d["score"] = sum(s[c] * w[c] for c in config.CRITERIA) / tot
        d.loc[s[config.CRITERIA].isna().any(axis=1), "score"] = np.nan
        tab = d.pivot_table(index="type", columns="condition", values="score", aggfunc="mean")
        for t, r in tab.iterrows():
            srt = r.sort_values(ascending=False)
            rows.append({"scheme": name, "type": t, "best": srt.index[0], "best_score": round(srt.iloc[0], 3),
                         "second": srt.index[1], "second_score": round(srt.iloc[1], 3)})
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="final", choices=["pilot", "final"])
    args = parser.parse_args()
    out_dir = results_dir(args.set)
    tables = out_dir / "tables"
    tables.mkdir(exist_ok=True)
    answers = pd.read_csv(out_dir / "answers.csv")
    scores = pd.read_csv(out_dir / "ragas_scores.csv")
    df = answers.merge(scores[["answer_id"] + config.CRITERIA], on="answer_id")
    for c in config.CRITERIA:
        df[f"{c}_s"] = (df[c] - 1) / 4 if c in RUBRIC else df[c]
    df["overall"] = df[[f"{c}_s" for c in config.CRITERIA]].mean(axis=1, skipna=False)
    metrics = config.CRITERIA + ["overall"]
    for tag, sub in [("all", df)] + [(llm, df[df["llm"] == llm]) for llm in sorted(df["llm"].unique())]:
        rng = np.random.default_rng(RNG_SEED)
        for factor in ["formatting", "grounding"]:
            factor_tests(sub, factor, metrics, rng).round(4).to_csv(tables / f"extra_{factor}_effects_{tag}.csv", index=False)
        pd.concat([interaction(sub, m) for m in ["overall", "faithfulness", "technical_correctness"]]).round(4) \
          .to_csv(tables / f"extra_interaction_{tag}.csv", index=False)
    sensitivity(df).to_csv(tables / "extra_weight_sensitivity.csv", index=False)
    print("Saved extra_* tables in", tables)


if __name__ == "__main__":
    main()
