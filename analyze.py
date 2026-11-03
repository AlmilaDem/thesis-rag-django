"""
STEP 7 - Analysis (thesis Section 2.5 step 7, Chapter 5).

Produces the tables and figures for:
  RQ1 - formatting strategies (F0, F1, F2), averaged over grounding strategies
  RQ2 - grounding strategies (G0, G1, G2), averaged over formatting strategies
  RQ3 - results per question type
plus the interaction table (F x G), objective measures, refusal results and retrieval.

Scores come from ragas_eval.py (all five criteria computed with RAGAS, Table 2.4).
Factual Correctness, Faithfulness and Response Relevancy are on a 0-1 scale; the two rubric
criteria (clarity, hallucination control) are on a 1-5 scale. Tables report every criterion on
its own scale. For the "overall" score and the bar charts, the rubric scores are rescaled to
0-1 with (score - 1) / 4, so that all criteria have the same weight.

Everything is analysed separately for each answer-generating LLM (thesis Section 2.2), and
additionally for both LLMs together.

Statistics: every question is answered under all 9 strategy combinations (paired /
repeated-measures design) and the scores are not normally distributed. Therefore the
non-parametric Friedman test is used to compare the three levels of a strategy, followed by
pairwise Wilcoxon signed-rank tests with Holm correction.

Run:  python analyze.py --set final
Output: results/<set>/tables/*.csv  and  results/<set>/figures/*.png
"""
import argparse
import itertools

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import friedmanchisquare, wilcoxon  # noqa: E402

import config  # noqa: E402
from experiment_io import results_dir  # noqa: E402

COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]   # one colour per strategy level (F0/F1/F2 or G0/G1/G2)
LABELS = {"technical_correctness": "Technical\ncorrectness", "clarity": "Clarity",
          "faithfulness": "Faithfulness", "hallucination_control": "Hallucination\ncontrol",
          "answer_relevance": "Answer\nrelevance", "overall": "Overall"}
NAMES = {"F0": "F0 baseline", "F1": "F1 short paragraph", "F2": "F2 step-by-step",
         "G0": "G0 baseline", "G1": "G1 inline citations", "G2": "G2 source-restricted"}


def holm(p_values):
    order = np.argsort(p_values)
    adjusted, running = [0.0] * len(p_values), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(p_values) - rank) * p_values[i]))
        adjusted[i] = running
    return adjusted


def mean_sd_table(df, factor, metrics):
    table = df.groupby(factor)[metrics].agg(["mean", "std"]).round(2)
    out = pd.DataFrame(index=table.index)
    for m in metrics:
        out[m] = table[(m, "mean")].map("{:.2f}".format) + " (" + table[(m, "std")].map("{:.2f}".format) + ")"
    return out


def stats_tests(df, factor, metrics):
    rows = []
    levels = sorted(df[factor].unique())
    for m in metrics:
        # one value per question and level: average over the other factor
        wide = df.groupby(["question_id", factor])[m].mean().unstack(factor).dropna()
        if len(wide) < 3 or len(levels) < 3:
            continue
        try:
            stat, p = friedmanchisquare(*[wide[lv] for lv in levels])
        except ValueError:
            stat, p = np.nan, np.nan
        pairs = list(itertools.combinations(levels, 2))
        raw = []
        for a, b in pairs:
            diff = wide[a] - wide[b]
            raw.append(1.0 if (diff == 0).all() else wilcoxon(wide[a], wide[b]).pvalue)
        adjusted = holm(raw)
        row = {"criterion": m, "n_questions": len(wide), "friedman_chi2": round(stat, 3),
               "friedman_p": round(p, 4)}
        for (a, b), p_adj in zip(pairs, adjusted):
            row[f"{a}_vs_{b}_mean_diff"] = round((wide[a] - wide[b]).mean(), 2)
            row[f"{a}_vs_{b}_p_holm"] = round(p_adj, 4)
        rows.append(row)
    return pd.DataFrame(rows)


RUBRIC = ["clarity", "hallucination_control"]


def bar_chart(df, factor, metrics, path, title):
    means = df.groupby(factor)[metrics].mean()
    levels = list(means.index)
    x = np.arange(len(metrics))
    width = 0.8 / len(levels)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    for i, level in enumerate(levels):
        bars = ax.bar(x + (i - (len(levels) - 1) / 2) * width, means.loc[level], width * 0.92,
                      label=NAMES.get(level, level), color=COLORS[i % len(COLORS)])
        ax.bar_label(bars, fmt="%.2f", fontsize=7, padding=2, color="#52514e")
    ax.set_xticks(x, [LABELS.get(m, m) for m in metrics])
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Mean score (0-1)")
    ax.set_title(title)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e5e4e0", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=len(levels), loc="upper center", bbox_to_anchor=(0.5, -0.15))
    fig.text(0.99, 0.01, "Clarity and hallucination control (1-5) rescaled to 0-1", ha="right",
             fontsize=7, color="#52514e")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def heatmap(table, path, title):
    fig, ax = plt.subplots(figsize=(1.2 * table.shape[1] + 2, 0.6 * table.shape[0] + 1.5))
    im = ax.imshow(table.values, cmap="Blues", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(table.shape[1]), table.columns, rotation=30, ha="right")
    ax.set_yticks(range(table.shape[0]), table.index)
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            value = table.values[i, j]
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=8,
                    color="white" if value > 0.7 else "#0b0b0b")
    fig.colorbar(im, ax=ax, label="Mean overall score (0-1)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def analyse(df, tables, figures, tag, title_suffix):
    """All tables and figures for one subset of answers (one LLM or both)."""
    raw = config.CRITERIA + ["overall"]
    scaled = [f"{c}_scaled" for c in config.CRITERIA] + ["overall"]
    for factor, rq in [("formatting", "RQ1"), ("grounding", "RQ2")]:
        mean_sd_table(df, factor, raw).to_csv(tables / f"{rq}_{factor}_mean_sd_{tag}.csv")
        stats_tests(df, factor, raw).to_csv(tables / f"{rq}_{factor}_tests_{tag}.csv", index=False)
        plot_df = df[[factor] + scaled].copy()
        plot_df.columns = [factor] + config.CRITERIA + ["overall"]
        bar_chart(plot_df, factor, config.CRITERIA + ["overall"], figures / f"{rq}_{factor}_{tag}.png",
                  f"Mean scores by {factor} strategy{title_suffix}")
        print(f"\n{rq} - mean (SD) by {factor}{title_suffix}:")
        print(mean_sd_table(df, factor, raw).to_string())
    fxg = df.pivot_table(index="formatting", columns="grounding", values="overall", aggfunc="mean")
    fxg.round(3).to_csv(tables / f"interaction_FxG_overall_{tag}.csv")
    heatmap(fxg, figures / f"interaction_FxG_{tag}.png", f"Overall score: formatting x grounding{title_suffix}")
    df = df.assign(condition=df["formatting"] + "+" + df["grounding"])
    by_type = df.pivot_table(index="type", columns="condition", values="overall", aggfunc="mean")
    by_type.round(3).to_csv(tables / f"RQ3_type_x_condition_overall_{tag}.csv")
    heatmap(by_type, figures / f"RQ3_type_x_condition_{tag}.png",
            f"Overall score by question type and condition{title_suffix}")
    for factor in ["formatting", "grounding"]:
        for m in raw:
            df.pivot_table(index="type", columns=factor, values=m, aggfunc="mean").round(3) \
              .to_csv(tables / f"RQ3_type_x_{factor}_{m}_{tag}.csv")
    best = by_type.idxmax(axis=1).rename("best_condition").to_frame()
    best["best_overall"] = by_type.max(axis=1).round(3)
    best.to_csv(tables / f"RQ3_best_condition_per_type_{tag}.csv")
    print(f"\nHighest-scoring condition per question type{title_suffix} (descriptive only):")
    print(best.to_string())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="final", choices=["pilot", "final"])
    args = parser.parse_args()
    out_dir = results_dir(args.set)
    tables, figures = out_dir / "tables", out_dir / "figures"
    tables.mkdir(exist_ok=True)
    figures.mkdir(exist_ok=True)

    answers = pd.read_csv(out_dir / "answers.csv")
    if "llm" not in answers.columns:
        answers["llm"] = "single"
    scores = pd.read_csv(out_dir / "ragas_scores.csv")
    df = answers.merge(scores[["answer_id"] + config.CRITERIA], on="answer_id")
    # NaN policy (Chapter 4): a score that is still empty after two RAGAS attempts is excluded
    # only for that criterion; the overall score is computed only for answers with all 5 scores.
    missing = df.groupby("llm")[config.CRITERIA].apply(lambda d: d.isna().sum())
    missing["answers"] = df.groupby("llm").size()
    missing.loc["ALL"] = missing.sum()
    missing.to_csv(tables / "missing_scores.csv")
    print("Empty (NaN) RAGAS scores per criterion:")
    print(missing.to_string())
    for c in config.CRITERIA:
        df[f"{c}_scaled"] = (df[c] - 1) / 4 if c in RUBRIC else df[c]
    df["overall"] = df[[f"{c}_scaled" for c in config.CRITERIA]].mean(axis=1, skipna=False)
    df.to_csv(tables / "all_scores_merged.csv", index=False)
    print(f"{len(df)} answers ({df['overall'].notna().sum()} with all 5 scores), {df['question_id'].nunique()} questions, LLMs: {sorted(df['llm'].unique())}")

    for llm in sorted(df["llm"].unique()):
        analyse(df[df["llm"] == llm], tables, figures, llm, f" ({llm})")
    if df["llm"].nunique() > 1:
        analyse(df, tables, figures, "all", " (both LLMs)")
        comp = df.groupby("llm")[config.CRITERIA + ["overall"]].mean().round(3)
        comp.to_csv(tables / "llm_comparison.csv")
        print("\nMean scores per LLM:")
        print(comp.to_string())

    auto_path = out_dir / "auto_checks.csv"
    if auto_path.exists():
        auto = pd.read_csv(auto_path)
        if "llm" not in auto.columns:
            auto["llm"] = "single"
        fmt = auto.groupby(["llm", "formatting"]).agg(
            format_compliance=("format_compliant", lambda s: s.dropna().mean()),
            mean_sentences=("n_sentences", "mean"), mean_chars=("n_chars", "mean"))
        fmt.round(3).to_csv(tables / "objective_formatting.csv")
        grd = auto.groupby(["llm", "grounding"]).agg(
            answers_with_citation=("has_citation", "mean"),
            citations_valid=("citations_valid", lambda s: s.dropna().mean()),
            correct_refusal_unanswerable=("correct_refusal", lambda s: s.dropna().mean()),
            missing_info_acknowledged_unanswerable=("unanswerable_acknowledged", lambda s: s.dropna().mean()),
            false_refusal_answerable=("false_refusal", lambda s: s.dropna().mean()))
        grd.round(3).to_csv(tables / "objective_grounding.csv")
        print("\nObjective measures by LLM and grounding strategy:")
        print(grd.round(3).to_string())

    check_path = out_dir / "retrieval_check.csv"
    if check_path.exists():
        check = pd.read_csv(check_path)
        check = check[check["answerable"]]
        summary = check.groupby("type")[["page_hit", "section_hit"]].mean()
        summary.loc["ALL"] = check[["page_hit", "section_hit"]].mean()
        (summary * 100).round(1).to_csv(tables / "retrieval_hit_rate.csv")
        print("\nRetrieval hit rate (%):")
        print((summary * 100).round(1).to_string())
    print(f"\nTables saved in {tables}\nFigures saved in {figures}")


if __name__ == "__main__":
    main()
