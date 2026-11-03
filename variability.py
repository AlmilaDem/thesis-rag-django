"""
Variability test (thesis Section 2.5 / 4.x): how stable are the answers when the SAME prompt
is sent several times with temperature 0 and a fixed seed?

5 answerable questions (one per question type) x 9 strategy combinations x 2 LLMs x 5 repeats
= 450 answers. The retrieval results of the main experiment (results/final/retrieved.json) are
reused, so only the generation step is repeated.

For every (question, LLM, F, G) the 5 repeats are compared:
  - n_unique          number of different answer texts (1 = always identical)
  - identical_all     True if all 5 repeats are exactly the same
  - mean_similarity   mean pairwise text similarity (difflib ratio, 0-1; 1 = identical)
  - min_similarity    lowest pairwise similarity
  - sd_chars          standard deviation of the answer length in characters

Run (after run_experiment.py --set final):   python variability.py
Can be stopped and restarted. Output: results/final/variability/
"""
import argparse
import itertools
import json
from datetime import datetime
from difflib import SequenceMatcher

import pandas as pd

import config
from experiment_io import load_questions, load_retrieved, results_dir
from rag import generate

QUESTION_IDS = ["Q01", "Q06", "Q11", "Q16", "Q21"]   # one per type: definition, how-to,
REPEATS = 5                                           # troubleshooting, configuration, api usage


def summarise(answers):
    rows = []
    keys = ["question_id", "type", "llm", "formatting", "grounding"]
    for key, group in answers.groupby(keys):
        texts = group.sort_values("repeat")["answer"].fillna("").astype(str).tolist()
        sims = [SequenceMatcher(None, a, b).ratio() for a, b in itertools.combinations(texts, 2)]
        rows.append(dict(zip(keys, key), n_repeats=len(texts), n_unique=len(set(texts)),
                         identical_all=len(set(texts)) == 1,
                         mean_similarity=round(sum(sims) / len(sims), 4) if sims else None,
                         min_similarity=round(min(sims), 4) if sims else None,
                         sd_chars=round(pd.Series([len(t) for t in texts]).std(), 1)))
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=REPEATS)
    args = parser.parse_args()

    questions = load_questions("final").set_index("id").loc[QUESTION_IDS]
    retrieved = load_retrieved("final")
    out_dir = results_dir("final") / "variability"
    out_dir.mkdir(exist_ok=True)
    answers_path = out_dir / "variability_answers.csv"
    done = set(pd.read_csv(answers_path)["run_id"]) if answers_path.exists() else set()
    combos = [(llm, f, g) for llm in config.GEN_MODELS for f in config.FORMATTING for g in config.GROUNDING]
    total = len(QUESTION_IDS) * len(combos) * args.repeats
    print(f"Variability test: {total} answers ({len(done)} already done)")

    for qid, q in questions.iterrows():
        for llm, f_code, g_code in combos:
            for rep in range(1, args.repeats + 1):
                run_id = f"{qid}_{llm}_{f_code}_{g_code}_r{rep}"
                if run_id in done:
                    continue
                answer, _, meta = generate(q["question"], retrieved[qid], f_code, g_code, config.GEN_MODELS[llm])
                row = {"run_id": run_id, "question_id": qid, "type": q["type"], "llm": llm,
                       "formatting": f_code, "grounding": g_code, "repeat": rep, "answer": answer,
                       "model": meta["model"], "completion_tokens": meta["completion_tokens"],
                       "generated_at": datetime.now().isoformat(timespec="seconds")}
                pd.DataFrame([row]).to_csv(answers_path, mode="a", index=False, header=not answers_path.exists())
                done.add(run_id)
                print(f"  [{len(done)}/{total}] {run_id}")

    answers = pd.read_csv(answers_path)
    detail = summarise(answers)
    detail.to_csv(out_dir / "variability_by_condition.csv", index=False)
    overview = detail.groupby("llm").agg(conditions=("n_unique", "size"),
                                         identical_all_pct=("identical_all", lambda s: round(s.mean() * 100, 1)),
                                         mean_n_unique=("n_unique", "mean"),
                                         mean_similarity=("mean_similarity", "mean"),
                                         min_similarity=("min_similarity", "min")).round(3)
    overview.to_csv(out_dir / "variability_summary.csv")
    print("\nVariability summary per LLM:")
    print(overview.to_string())
    (out_dir / "variability_settings.json").write_text(json.dumps(
        {"questions": QUESTION_IDS, "repeats": args.repeats, "temperature": config.TEMPERATURE,
         "seed": config.SEED, "models": config.GEN_MODELS}, indent=2))


if __name__ == "__main__":
    main()
